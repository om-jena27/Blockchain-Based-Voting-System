# Blockchain-Based Secure Voting System

A secure, decentralized voting application built with Python (Flask) and integrated with the Ethereum blockchain (Sepolia testnet) for immutable verification.

## Features

- **MetaMask Authentication:** Users authenticate securely via their MetaMask wallet address. No passwords required.
- **Ethereum Integration:** Every vote securely records a hash of the transaction to the Ethereum Sepolia Testnet, providing a fully transparent and immutable public ledger.
- **Privacy-Preserving Verification:** Individual votes are associated with hashed wallet IDs. The public ledger proves the vote happened without revealing the specific voter's candidate choice publicly.
- **Admin Dashboard:**
  - Securely add and remove candidates.
  - Set global election start and end timers.
  - View full blockchain ledger of all votes with direct links to Etherscan.
- **Real-Time Turnout Metrics:** Voters and admins alike can view the *Total Votes Cast* and a live countdown timer during the election, without exposing individual candidate standings until the election firmly concludes.

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/om-jena27/Blockchain-Based-Voting-System.git
   cd Blockchain-Based-Voting-System
   ```

2. **Set up Environment Variables:**
   Create a `.env` file in the root directory and add the following context:
   ```env
   ADMIN_WALLET=your_metamask_wallet_address_here
   ETH_RPC_URL=your_infura_or_alchemy_rpc_url_here
   ETH_PRIVATE_KEY=your_metamask_private_key_here
   ```

3. **Start the Application (Windows):**
   Simply execute `start_voting_app.bat`. This interactive script will:
   - Create a Python virtual environment.
   - Install all required dependencies from `requirements.txt`.
   - Compile and deploy the Ethereum smart contract (if not already deployed).
   - Start the local Flask web server automatically.

4. **Verify the Network:**
   Ensure your MetaMask is set to the **Sepolia test network** to cast votes natively.

## License
MIT License
