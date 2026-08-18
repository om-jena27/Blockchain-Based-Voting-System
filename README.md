# 🗳️ Blockchain-Based Secure Voting System

<div align="center">

![Blockchain Voting](https://img.shields.io/badge/Blockchain-Voting%20System-3C3C3D?style=for-the-badge&logo=ethereum&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Ethereum](https://img.shields.io/badge/Ethereum-Sepolia%20Testnet-3C3C3D?style=flat-square&logo=ethereum&logoColor=white)](https://sepolia.etherscan.io/)
[![Web3.py](https://img.shields.io/badge/Web3.py-F16822?style=flat-square&logo=web3dotjs&logoColor=white)](https://web3py.readthedocs.io/)
[![MetaMask](https://img.shields.io/badge/MetaMask-Auth-E2761B?style=flat-square&logo=metamask&logoColor=white)](https://metamask.io/)

> **A secure, decentralized voting application built with Python (Flask) and integrated with the Ethereum blockchain (Sepolia testnet) for immutable, transparent vote verification.**

</div>

---

## ✨ Features

- 🦊 **MetaMask Authentication** — Users authenticate via their MetaMask wallet address. No passwords required — trustless by design.
- ⛓️ **Ethereum Integration** — Every vote records a transaction hash to the Ethereum Sepolia Testnet, providing a fully transparent and immutable public ledger.
- 🔏 **Privacy-Preserving** — Individual votes are associated with hashed wallet IDs. The ledger proves a vote happened without revealing which candidate was chosen.
- 👑 **Admin Dashboard**
  - Add and remove candidates securely
  - Set global election start and end timers
  - View full blockchain ledger with direct Etherscan links
- 📊 **Real-Time Metrics** — Live vote count and countdown timer visible to all users without exposing candidate standings until the election ends
- 🗃️ **PostgreSQL Database** — Stores voter registry, candidates, and local vote records alongside the blockchain ledger

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3, Flask |
| **Blockchain** | Ethereum (Sepolia Testnet), Web3.py, Solidity Smart Contract |
| **Database** | PostgreSQL |
| **Auth** | MetaMask Wallet (no passwords) |
| **Frontend** | HTML5, CSS3, Jinja2 Templates |

---

## 📁 Project Structure

```
Blockchain-Based-Voting-System/
├── app.py                  # Flask main application & routes
├── blockchain.py           # Custom blockchain implementation
├── database.py             # PostgreSQL DB models & helpers
├── eth_integration.py      # Ethereum / Web3.py integration
├── contract_abi.json       # Voting smart contract ABI
├── contracts/              # Solidity smart contract source
├── static/                 # CSS, JS assets
├── templates/              # HTML Jinja2 templates
├── requirements.txt        # Python dependencies
└── start_voting_app.bat    # One-click Windows launcher
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10+
- PostgreSQL
- MetaMask browser extension
- Sepolia testnet ETH (get from [Sepolia Faucet](https://sepoliafaucet.com/))
- Infura / Alchemy API key (for Ethereum node access)

### Installation

```bash
# Clone the repository
git clone https://github.com/om-jena27/Blockchain-Based-Voting-System.git
cd Blockchain-Based-Voting-System

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create a .env file with:
# DATABASE_URL=postgresql://user:password@localhost:5432/voting
# INFURA_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID
# CONTRACT_ADDRESS=0xYourDeployedContractAddress
# ADMIN_WALLET=0xYourAdminWalletAddress

# Run the application
python app.py
```

### Windows Quick Start

```bash
# Just double-click:
start_voting_app.bat
```

---

## 🔄 How It Works

```
User connects MetaMask
        ↓
Wallet address verified & hashed
        ↓
User casts vote in the UI
        ↓
Flask backend records vote in PostgreSQL
        ↓
Transaction hash submitted to Ethereum Sepolia
        ↓
Vote is permanently recorded on the blockchain ✅
        ↓
Admin can verify via Etherscan link
```

---

## 🌐 Blockchain Architecture

- **Smart Contract** (Solidity) — Deployed on Ethereum Sepolia Testnet
- **On-chain data** — Transaction hashes, vote counts
- **Off-chain data** — Voter identities (hashed), candidate info (PostgreSQL)
- **Privacy model** — Wallet → SHA-256 hash → stored on chain (voter ID never exposed)

---

## 👨‍💻 Author

**Om Prakash Jena** — B.Tech CSE (AI & ML), Centurion University

[![GitHub](https://img.shields.io/badge/GitHub-om--jena27-181717?style=flat-square&logo=github)](https://github.com/om-jena27)

---

## 📄 License

Open-source project. Built for educational purposes.
