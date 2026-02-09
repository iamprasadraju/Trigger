# Trigger - Price & Content Monitor

A Python-based automation tool that monitors web pages for price drops and keyword appearances, sending instant Telegram notifications when conditions are met.

## ✨ Features

- 🛒 **Price Monitoring**: Track product prices across e-commerce sites
- 🔍 **Keyword Detection**: Get notified when specific keywords appear on web pages
- 🤖 **Automated Execution**: Runs every 6 hours via GitHub Actions
- 📱 **Telegram Alerts**: Instant notifications via Telegram bot
- ⚡ **Async Processing**: Fast concurrent page scraping with aiohttp
- 🚀 **Multiple Triggers**: Scheduled, manual, or JSON-based triggers

## 📋 Prerequisites

- Python 3.13+
- Telegram Bot Token & Chat ID
- GitHub account (for automation)

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone <repo-url>
cd Trigger

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
export CHAT_ID="your_chat_id"
```

### 3. Configure Monitoring

Edit `urls.json` to add URLs to monitor:

```json
{
  "urls": [
    {
      "description": "Product Price Tracker",
      "url": "https://example.com/product",
      "value": 599
    },
    {
      "description": "News Keyword Alert",
      "url": "https://news.example.com",
      "keyword": "breaking"
    }
  ]
}
```

### 4. Run Locally

```bash
python src/main.py
```

## 🔧 Configuration

### urls.json Structure

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| description | string | Yes | Alert message prefix |
| url | string | Yes | Target URL to monitor |
| value | string | No | Exact text to detect (price/value) |
| keyword | string | No | Case-insensitive keyword to search |

**Note**: Use either `value` (exact match) or `keyword` (case-insensitive), not both.

## 🔄 GitHub Actions Automation

The workflow triggers on:
- ⏰ **Schedule**: Every 6 hours (`0 */6 * * *`)
- 📝 **Push**: Changes to `urls.json` on `github-workflow` branch
- 👆 **Manual**: Via GitHub Actions UI

### Branching Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Local development & testing |
| `github-workflow` | Production automation branch |

### Required Secrets

Configure these in GitHub Settings → Secrets:

- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token
- `CHAT_ID` - Your Telegram chat ID

## 📁 Project Structure

```
Trigger/
├── .github/workflows/run.yaml  # GitHub Actions workflow
├── src/
│   └── main.py                 # Main application
├── urls.json                   # URLs to monitor
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Project metadata
└── README.md                  # Documentation
```

## 🛠️ Development

### Running Tests

```bash
# Add tests here when implemented
pytest tests/
```

### Code Style

```bash
# Format code
black src/
ruff check src/
```

## 🐛 Troubleshooting

- **Telegram not receiving messages**: Verify `TELEGRAM_BOT_TOKEN` and `CHAT_ID`
- **Scraping failures**: Some sites may block automated requests
- **Timeout errors**: Increase timeout in `aiohttp.ClientSession()`

## 📄 License

MIT License
