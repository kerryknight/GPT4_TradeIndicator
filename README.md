# Option Alpha Webhook Integration with OpenAI GPT

This script serves as a webhook for an Option Alpha trading bot, using OpenAI’s GPT-4o model to assess real-time news and evaluate market conditions for an iron condor trading strategy. It determines whether market conditions are favorable for trading by analyzing recent global events and their potential impact on the S&P 500 (SPX), pausing trades if volatility is anticipated.

## Features

- **Real-Time News Analysis**: Fetches breaking news from `newsapi.org` and passes it to GPT-4o for analysis of market impact.
- **Automated Trade Control**: Decides to enable or pause trading based on potential market volatility.
- **Secure API Key and URL Handling**: Stores OpenAI API key, `newsapi.org` key, and Option Alpha webhook URLs in secure files outside the codebase.
- **Confidence-Based Volatility Assessment**: GPT assigns a confidence level (`High` or `Low`) to its volatility predictions, pausing trades only for high-confidence volatility events.

## Setup

### Prerequisites

- **Python 3.7 or later**
- Required Python packages:
  - `Flask` (for the web server)
  - `requests` (for API requests)
- **OpenAI API Key** with access to GPT-4 model or GPT-4-turbo
- **NewsAPI.org API Key** for real-time news access
- **Option Alpha Webhook URLs** for trade management

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Nathan-Strodtbeck/GPT4_TradeIndicator.git
   cd GPT4_TradeIndicator
   ```

2. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

   **`requirements.txt` should include:**
   ```
   Flask
   requests
   ```

### Setting Up API Keys and Webhook URLs

#### On Windows

1. **Create a Secure Directory**:
   Open Command Prompt and create a directory for storing API keys and webhooks:
   ```cmd
   mkdir C:\secrets
   ```

2. **Store the OpenAI API Key**:
   - Create a text file `C:\secrets\IndicatorKey.txt` and paste your OpenAI API key.

3. **Store the NewsAPI Key**:
   - Create a text file `C:\secrets\NewsKey.txt` and paste your `newsapi.org` key.

4. **Store the Option Alpha Webhook URLs**:
   - Create a text file `C:\secrets\WebhookURLs.txt` with the following content:
     ```
     TRADE_URL=https://app.optionalpha.com/hook/your_trade_url_here
     NO_TRADE_URL=https://app.optionalpha.com/hook/your_no_trade_url_here
     ```
   - Replace `your_trade_url_here` and `your_no_trade_url_here` with your actual Option Alpha webhook URLs.

#### On Linux

1. **Create a Secure Directory**:
   ```bash
   sudo mkdir -p /etc/secrets
   sudo chmod 700 /etc/secrets
   ```

2. **Save the OpenAI API Key**:
   ```bash
   echo "your_openai_api_key_here" | sudo tee /etc/secrets/IndicatorKey.txt > /dev/null
   sudo chmod 600 /etc/secrets/IndicatorKey.txt
   ```

3. **Save the NewsAPI Key**:
   ```bash
   echo "your_news_api_key_here" | sudo tee /etc/secrets/NewsKey.txt > /dev/null
   sudo chmod 600 /etc/secrets/NewsKey.txt
   ```

4. **Save the Option Alpha Webhook URLs**:
   - Create a file `/etc/secrets/WebhookURLs.txt` and add the following:
     ```
     TRADE_URL=https://app.optionalpha.com/hook/your_trade_url_here
     NO_TRADE_URL=https://app.optionalpha.com/hook/your_no_trade_url_here
     ```
   - Set permissions:
     ```bash
     sudo chmod 600 /etc/secrets/WebhookURLs.txt
     ```

### Verify File Permissions

Ensure that both `IndicatorKey.txt` and `WebhookURLs.txt` are only readable by the application (permissions set to 600 on Linux).

## Usage

### Run the Web Server

1. **Start the Flask Server**:
   On Windows:
   ```cmd
   cd C:\GPT4_TradeIndicator
   python option_alpha_webhook.py
   ```

   On Linux:
   ```bash
   python3 option_alpha_webhook.py
   ```

2. **Access the Webhook Endpoint**:
   The server will run on `http://127.0.0.1:5000/`. You can use `curl` or an external scheduler to trigger the endpoint periodically.

### Triggering the Webhook

To automate, you can set up a scheduler to call `http://127.0.0.1:5000/option_alpha_trigger` every 15 minutes or another desired interval.

#### Example Cron Job (Linux):

To trigger every 15 minutes, add to crontab:
```bash
*/15 * * * * curl -X POST http://localhost:5000/option_alpha_trigger
```

### How It Works

1. **Fetches Breaking News**: The webhook uses `newsapi.org` to fetch recent world events.
2. **GPT Analysis**: GPT-4o evaluates the news for potential SPX volatility, based on historical impact and investor sentiment.
3. **Trade Decision**:
   - **Trade**: If GPT predicts stability or assigns low confidence to volatility, the bot triggers the Trade URL to enable trading.
   - **No Trade**: If high-confidence volatility is expected, the bot triggers the No Trade URL to pause trading.

### Secure Configuration

- **OpenAI API Key**: Stored in `C:\secrets\IndicatorKey.txt` (Windows) or `/etc/secrets/IndicatorKey.txt` (Linux).
- **NewsAPI Key**: Stored in `C:\secrets\NewsKey.txt` (Windows) or `/etc/secrets/NewsKey.txt` (Linux).
- **Webhook URLs**: Stored in `C:\secrets\WebhookURLs.txt` (Windows) or `/etc/secrets/WebhookURLs.txt` (Linux) with `TRADE_URL` and `NO_TRADE_URL` as key-value pairs.

Ensure restrictive permissions on all files to prevent unauthorized access.

## File Structure for Secrets

**On Windows:**
```
C:\secrets\
├── IndicatorKey.txt       # Contains the OpenAI API key
├── NewsKey.txt            # Contains the NewsAPI key
└── WebhookURLs.txt        # Contains TRADE_URL and NO_TRADE_URL
```

**On Linux:**
```
/etc/secrets/
├── IndicatorKey.txt       # Contains the OpenAI API key
├── NewsKey.txt            # Contains the NewsAPI key
└── WebhookURLs.txt        # Contains TRADE_URL and NO_TRADE_URL
```

## Dependencies

List of required packages (also in `requirements.txt`):

```
Flask
requests
```

Install dependencies with:
```bash
pip install -r requirements.txt
```

## Troubleshooting

- **API Key Not Found**: Ensure `IndicatorKey.txt` and `NewsKey.txt` exist in the correct directory and contain the API keys.
- **Webhook URLs Not Found**: Ensure `WebhookURLs.txt` exists and includes both `TRADE_URL` and `NO_TRADE_URL`.
- **Permission Errors**: Verify that API key and webhook files have restrictive permissions (chmod 600 on Linux).

## Contributing

Feel free to submit issues or pull requests for bugs or feature suggestions.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
