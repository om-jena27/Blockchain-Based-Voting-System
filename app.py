from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db, get_db_connection, get_full_chain_data, get_latest_block, add_block_to_db
from blockchain import Blockchain, Block
from datetime import datetime
import hashlib
import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize DB
init_db()

# Reconstruct blockchain in memory for validation purposes
def get_blockchain():
    chain_data = get_full_chain_data()
    bc = Blockchain()
    bc.load_chain(chain_data)
    return bc

@app.route('/')
def index():
    if 'voter_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handling fallback for any existing forms, redirect to metamask login
        pass
    return render_template('login.html')

@app.route('/auth/metamask', methods=['POST'])
def auth_metamask():
    data = request.get_json()
    wallet_address = data.get('wallet_address')
    
    if not wallet_address:
        return jsonify({'error': 'No wallet address provided'}), 400
        
    admin_wallet = os.getenv('ADMIN_WALLET', '').lower()
    is_admin = wallet_address.lower() == admin_wallet
    
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE voter_id = ?", (wallet_address.lower(),)).fetchone()
    
    if not user:
        # Create user
        conn.execute("INSERT INTO users (voter_id, password_hash, is_admin) VALUES (?, ?, ?)",
                     (wallet_address.lower(), 'metamask_login_no_password', is_admin))
        conn.commit()
        user = conn.execute("SELECT * FROM users WHERE voter_id = ?", (wallet_address.lower(),)).fetchone()
    else:
        # Update admin status if it has changed in .env
        if user['is_admin'] != is_admin:
            conn.execute("UPDATE users SET is_admin = ? WHERE id = ?", (is_admin, user['id']))
            conn.commit()
            
    conn.close()
    
    session['user_id'] = user['id']
    session['voter_id'] = user['voter_id']
    session['is_admin'] = is_admin
    session['has_voted'] = user['has_voted']
    
    if is_admin:
        return jsonify({'redirect': url_for('admin')})
    return jsonify({'redirect': url_for('dashboard')})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'voter_id' not in session:
        return redirect(url_for('login'))
        
    from database import get_setting
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],)).fetchone()
    candidates = conn.execute("SELECT * FROM candidates").fetchall()
    
    # Vote counts based on blockchain
    chain_data = get_full_chain_data()
    total_votes = sum(1 for block in chain_data if block.get('candidate_id') is not None)
            
    conn.close()
    
    session['has_voted'] = user['has_voted']
    
    election_start = get_setting('election_start')
    election_end = get_setting('election_end')
    now = datetime.now().isoformat()
        
    return render_template('dashboard.html', user=user, candidates=candidates, total_votes=total_votes,
                           election_start=election_start, election_end=election_end, now=now)

@app.route('/vote', methods=['POST'])
def vote():
    if 'voter_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    candidate_id = request.form.get('candidate_id')
    if not candidate_id:
        return jsonify({'error': 'No candidate selected'}), 400
        
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],)).fetchone()
    if user['has_voted']:
        conn.close()
        return jsonify({'error': 'You have already voted'}), 400
        
    from database import get_setting
    election_start = get_setting('election_start')
    election_end = get_setting('election_end')
    now = datetime.now().isoformat()
    
    if election_start and now < election_start:
        conn.close()
        return jsonify({'error': 'Voting has not started yet'}), 400
    if election_end and now > election_end:
        conn.close()
        return jsonify({'error': 'Voting has ended'}), 400
        
    # Get latest block
    previous_block = get_latest_block()
    
    # Hash the voter ID for privacy
    voter_id_hash = hashlib.sha256(user['voter_id'].encode()).hexdigest()
    
    # Create the new block logic manually using Blockchain wrapper isn't strictly necessary for single add, but let's do it cleanly
    bc = get_blockchain()
    new_block = bc.add_block(voter_id_hash, int(candidate_id), previous_block)
    
    # Submit hash to Ethereum Network
    from eth_integration import submit_hash_to_ethereum
    eth_tx_hash = submit_hash_to_ethereum(new_block.hash)
    new_block.eth_tx_hash = eth_tx_hash
    
    # Save block
    add_block_to_db(new_block)
    
    # Update user voted status
    conn.execute("UPDATE users SET has_voted = 1 WHERE id = ?", (user['id'],))
    conn.commit()
    conn.close()
    
    session['has_voted'] = True
    return jsonify({'success': 'Vote successfully cast on the blockchain!'})

@app.route('/admin')
def admin():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    candidates = conn.execute("SELECT * FROM candidates").fetchall()
    conn.close()
    
    chain_data = get_full_chain_data()
    bc = get_blockchain()
    is_valid = bc.is_chain_valid()
    
    from database import get_setting
    election_start = get_setting('election_start')
    election_end = get_setting('election_end')
    
    return render_template('admin.html', candidates=candidates, chain=chain_data, is_valid=is_valid,
                           election_start=election_start, election_end=election_end)

@app.route('/admin/settings', methods=['POST'])
def update_settings():
    if not session.get('is_admin'):
        return redirect(url_for('dashboard'))
        
    from database import set_setting
    start = request.form.get('election_start')
    end = request.form.get('election_end')
    if start:
        set_setting('election_start', start)
    if end:
        set_setting('election_end', end)
        
    flash("Election timers updated!")
    return redirect(url_for('admin'))

@app.route('/admin/add_candidate', methods=['POST'])
def add_candidate():
    if not session.get('is_admin'):
        return redirect(url_for('dashboard'))
        
    name = request.form['name']
    conn = get_db_connection()
    conn.execute("INSERT INTO candidates (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/admin/delete_candidate/<int:candidate_id>', methods=['POST'])
def delete_candidate(candidate_id):
    if not session.get('is_admin'):
        return redirect(url_for('dashboard'))
        
    conn = get_db_connection()
    conn.execute("DELETE FROM candidates WHERE id = ?", (candidate_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/api/turnout')
def api_turnout():
    if 'voter_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    chain_data = get_full_chain_data()
    total_votes = sum(1 for block in chain_data if block.get('candidate_id') is not None)
            
    return jsonify({'total_votes': total_votes})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
