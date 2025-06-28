Here's your complete Markdown-formatted README, ready to copy and paste directly into VSCode:

markdown
Copy
Edit
# 🦍 Mountain Gorilla Command Center (MGCC)

*A comprehensive ETH investment and bot management system with Silverback-style automation, terminal-first design, and security-first architecture.*

---

## 🚀 Overview

The **Mountain Gorilla Command Center (MGCC)** is a terminal-first ETH investment platform that combines traditional investment account features with advanced bot automation. Built with a security-first approach, MGCC provides a complete solution for managing portfolios, deploying trading bots, and monitoring market conditions—all through an intuitive CLI interface.

---

## 🎯 Core Features

### 🧠 Investment Account Layer (Vanguard Equivalent)
- **Portfolio Management**: View current asset allocations (tokens, ETH, NFTs)
- **Real-time Balances**: Live ETH & token balances from connected wallets
- **Trade History**: Complete transaction history and performance tracking
- **Yield Tracking**: Monitor staking returns and yield-bearing tokens
- **Order Management**: Track open limit orders and DCA positions
- **Watchlists**: Custom token and project tracking

### 🪙 ETH-Specific Functionality
- **Token Swaps**: Simple token exchanges via aggregator APIs
- **Staking Integration**: Stake into protocols (Lido, EigenLayer)
- **Liquidity Provision**: Manage LP positions
- **Yield Farming**: View APYs and deposit into yield protocols
- **NFT Management**: Track holdings, floor prices, and rarity
- **Gas Optimization**: Monitor fees and optimal transaction windows
- **Multi-wallet Support**: Manage multiple ETH wallets

### 🦍 Silverback Bot Deployment Layer
- **Bot Deployment**: Deploy trading bots with various strategies
- **Lifecycle Management**: Start, stop, pause, and resume bots
- **Configuration**: Adjust risk levels, intervals, and parameters
- **Market Scanning**: Run strategy-based signal analysis
- **Backtesting**: Simulate bot performance with historical data
- **Real-time Monitoring**: Live bot status and execution logs

### 📊 Terminal Dashboard UI
- **Live Price Tickers**: Real-time cryptocurrency prices
- **Portfolio Dashboard**: Position tracking and PnL monitoring
- **Bot Status Monitor**: Live bot execution status
- **Gas Fee Tracker**: Network fee monitoring and optimization
- **Interactive Charts**: Portfolio growth and performance visualization

### 🛡️ Security & Safety Features
- **Secure Vault**: Encrypted private key storage
- **Transaction Signing**: Explicit approval for all transactions
- **Read-only Mode**: Safe exploration without execution
- **Backup & Restore**: Encrypted system backups
- **Security Audits**: Contract approval monitoring and risk assessment
- **Multi-signature Support**: Institutional-grade security

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- pip package manager

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/mountain-gorilla.git
cd mountain-gorilla
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run MGCC**
```bash
python main.py
```

---

## 🧑‍💻 Usage Guide

### Basic Commands

#### Main Menu Navigation
```bash
python main.py
# Navigate through the interactive menu
```

#### Bot Management
```bash
# Deploy a new DCA bot
python main.py bots deploy --name dca_bot_1 --strategy eth-dca

# List all bots
python main.py bots list

# Start a bot
python main.py bots start dca_bot_1

# View bot logs
python main.py bots log dca_bot_1

# Configure bot parameters
python main.py bots config dca_bot_1 --risk-level high --max-position 0.2
```

#### Market Analysis
```bash
# Run market scan
python main.py bots market-scan --strategy rsi

# Test bot strategy
python main.py bots test dca_bot_1 --dry-run
```

#### Security & Vault
```bash
# Store private key securely
python main.py vault store --name main_wallet --key 0x123... --description "Main trading wallet"

# List stored wallets
python main.py vault list

# Create encrypted backup
python main.py backup create --include-vault --password mypassword

# Run security audit
python main.py audit
```

#### Transaction Management
```bash
# Create transaction for approval
python main.py sign create --wallet main_wallet --to 0x123... --value 0.1

# List pending transactions
python main.py sign pending

# Approve transaction
python main.py sign approve --tx-id abc12345
```

### Interactive Dashboard

Launch the live terminal dashboard for real-time monitoring:
```bash
# From main menu, select option 7
# Or run directly:
python -c "from mountain_gorilla.dashboard import TerminalDashboard; TerminalDashboard().run()"
```

---

## 🦍 Bot Strategies

### Available Strategies

1. **ETH-DCA (Dollar Cost Averaging)**
   - Automated periodic ETH purchases
   - Configurable intervals and amounts
   - Gas optimization for cost efficiency

2. **Momentum Trading**
   - Technical indicator-based signals
   - RSI, MACD, and moving average analysis
   - Risk management with stop-loss/take-profit

3. **Yield Farming**
   - Automated yield protocol deposits
   - APY monitoring and rebalancing
   - Gas-efficient compound strategies

### Custom Strategy Development

Create custom strategies by extending the base strategy class:
```python
from mountain_gorilla.bot_manager import BotConfig

# Deploy custom strategy
bot_manager.deploy_bot(
    name="my_custom_bot",
    strategy="custom_momentum",
    risk_level="medium",
    intervals="15m",
    gas_budget=0.02
)
```

---

## 🛡️ Security Features

### Vault Management
- **Encrypted Storage**: All private keys encrypted with Fernet
- **Access Control**: Explicit user confirmation required
- **Audit Trail**: Complete access logging
- **Secure Deletion**: Permanent key removal

### Transaction Safety
- **Approval Workflow**: All transactions require explicit approval
- **Transaction Review**: Detailed transaction details before signing
- **Batch Operations**: Group multiple transactions for efficiency
- **Gas Optimization**: Automatic gas estimation and optimization

### Backup & Recovery
- **Encrypted Backups**: Password-protected system backups
- **Selective Backup**: Include/exclude sensitive data
- **Automated Scheduling**: Regular backup creation
- **Quick Recovery**: One-command system restoration

---

## 📊 Dashboard Features

### Live Price Ticker
- Real-time cryptocurrency prices
- 24-hour price changes
- Market sentiment indicators
- Custom token support

### Portfolio Overview
- Current position values
- Unrealized PnL tracking
- Asset allocation breakdown
- Performance metrics

### Bot Status Monitor
- Live bot execution status
- Trade count and PnL
- Error monitoring and alerts
- Performance analytics

### Gas Fee Tracker
- Current network gas prices
- Optimal transaction timing
- Gas fee predictions
- Cost optimization recommendations

---

## 🔧 Configuration

### Environment Variables
```bash
# Database configuration
MGCC_DB_PATH=./data/mgcc.db

# API endpoints
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY
ETHERSCAN_API_KEY=your_etherscan_key

# Security settings
MGCC_VAULT_PATH=./.vault
MGCC_BACKUP_PATH=./backups
```

### Bot Configuration
```yaml
# Example bot configuration
name: eth_dca_bot
strategy: eth-dca
risk_level: medium
intervals: 1h
gas_budget: 0.01
max_position_size: 0.1
stop_loss: 0.05
take_profit: 0.15
token_list: ["ETH", "USDC", "WETH"]
```

---

## 🚀 Advanced Features

### API Integration
- **Web3.py**: Full Ethereum blockchain interaction
- **Price APIs**: Real-time market data feeds
- **DEX Aggregators**: Best swap route finding
- **Yield Protocols**: Automated yield optimization

### Automation
- **Event-driven Bots**: Respond to on-chain events
- **Scheduled Tasks**: Time-based execution
- **Conditional Logic**: Complex decision trees
- **Risk Management**: Automatic position sizing

### Monitoring & Alerts
- **Performance Tracking**: Real-time PnL monitoring
- **Risk Alerts**: Position size and drawdown warnings
- **Network Monitoring**: Gas fee and congestion alerts
- **Bot Health**: Execution status and error reporting

---

## 🔮 Future Roadmap

### Planned Features
- **AI-Powered Analysis**: Machine learning signal generation
- **Cross-chain Support**: Multi-chain portfolio management
- **Institutional Features**: Multi-signature and compliance tools
- **Mobile Integration**: Companion mobile app
- **Social Trading**: Copy successful strategies
- **Advanced Analytics**: Portfolio optimization algorithms

### Integration Partners
- **DEX Aggregators**: 1inch, 0x Protocol
- **Yield Protocols**: Aave, Compound, Yearn
- **Data Providers**: CoinGecko, CoinMarketCap
- **Security Tools**: OpenZeppelin, ConsenSys Diligence

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone with submodules
git clone --recursive https://github.com/yourusername/mountain-gorilla.git

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
flake8 mountain_gorilla/
```

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

## ⚠️ Disclaimer

This software is for educational and research purposes. Cryptocurrency trading involves substantial risk of loss. Always:
- Start with small amounts
- Understand the strategies you're using
- Never invest more than you can afford to lose
- Consider consulting with a financial advisor

---

## ✨ Acknowledgements

- **ApeWorX**: Inspiration for the Silverback bot framework
- **Rich**: Beautiful terminal UI components
- **Web3.py**: Ethereum blockchain interaction
- **Cryptography**: Secure key management

---

🦍 **Happy Trading with Mountain Gorilla!** 🦍