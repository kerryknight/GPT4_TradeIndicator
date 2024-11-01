# Option Alpha Webhook Integration with OpenAI GPT

This script serves as a webhook for an Option Alpha trading bot. It uses OpenAI's GPT API to analyze major world events and determine if market conditions are favorable for trading. Designed for use with an iron condor trading strategy, the script triggers either a "Trade" or "No Trade" action based on the predicted market stability, pausing trades if volatility is expected.

## Features

- **World Event Analysis**: Queries OpenAI’s GPT-4 model for recent significant world events and assesses their potential impact on the S&P 500 (SPX).
- **Automated Trade Control**: Decides to either enable or pause trading based on potential market volatility.
- **Secure API Key and URL Handling**: Retrieves the OpenAI API key and Option Alpha webhook URLs from secure files stored outside the codebase.

## Setup

### Prerequisites

- Python 3.7 or later
- Required Python packages:
  - `Flask` (for the web server)
  - `requests` (for API requests)
- Access to an OpenAI API key with GPT-4 model access
- Access to your Option Alpha webhook URLs for trade management

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Nathan-Strodtbeck/GPT4_TradeIndicator.git
   cd option_alpha_webhook
   ```

2. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up API Key and Webhook URLs**:
   - Create a secure directory to store your secrets:
     ```bash
     sudo mkdir -p /etc/secrets
     sudo chmod 700 /etc/secrets
     ```

   - **Save the OpenAI API Key**:
     - Create a file `/etc/secrets/IndicatorKey.txt` and paste your API key into it.
     - Ensure that the file has restricted permissions:
       ```bash
       echo "your_openai_api_key_here" | sudo tee /etc/secrets/IndicatorKey.txt > /dev/null
       sudo chmod 600 /etc/secrets/IndicatorKey.txt
       ```

   - **Save the Option Alpha Webhook URLs**:
     - Create a file `/etc/secrets/WebhookURLs.txt` with the following content:
       ```plaintext
       TRADE_URL=https://app.optionalpha.com/hook/your_trade_url_here
       NO_TRADE_URL=https://app.optionalpha.com/hook/your_no_trade_url_here
       ```
     - Set the file permissions:
       ```bash
       sudo chmod 600 /etc/secrets/WebhookURLs.txt
       ```

     **Important**: Replace `your_trade_url_here` and `your_no_trade_url_here` with your actual Option Alpha webhook URLs.

4. **Verify File Permissions**:
   - Ensure that both `/etc/secrets/IndicatorKey.txt` and `/etc/secrets/WebhookURLs.txt` are only readable by the application (permissions set to `600`).

## Usage

1. **Run the Web Server**:
   ```bash
   python3 option_alpha_webhook.py
   ```
   This starts a Flask web server on port 5000.

2. **Trigger the Webhook**:
   - You can set up a cron job or external scheduler to make a request to `http://yourserver:5000/option_alpha_trigger` every 15 minutes or at another desired interval.

3. **Sample Cron Job** (for Linux):
   - To trigger the webhook every 15 minutes, add the following to your crontab:
     ```bash
     */15 * * * * curl -X POST http://localhost:5000/option_alpha_trigger
     ```

## How It Works

1. **World Events Query**: The webhook queries GPT-4 with a prompt to summarize major world events from the past 24 hours.
2. **Impact Analysis**: Based on these events, GPT is asked if the SPX is likely to experience volatility exceeding 1.5 basis points.
3. **Trade Decision**:
   - If GPT predicts stability, the script triggers the **Trade URL** to enable trading.
   - If volatility is expected, it triggers the **No Trade URL** to pause trading.

## Secure Configuration

This script retrieves sensitive information (OpenAI API key and webhook URLs) from secure files stored outside the codebase:

- **OpenAI API Key**: Stored in `/etc/secrets/IndicatorKey.txt`.
- **Webhook URLs**: Stored in `/etc/secrets/WebhookURLs.txt`, with `TRADE_URL` and `NO_TRADE_URL` as key-value pairs.

Both files should have restrictive permissions (`chmod 600`) to ensure that only the application can read them.

## File Structure for Secrets

```
/etc/secrets/
├── IndicatorKey.txt       # Contains the OpenAI API key
└── WebhookURLs.txt        # Contains TRADE_URL and NO_TRADE_URL
```

## Dependencies

List of required packages (also in `requirements.txt`):
- `Flask`
- `requests`

Install dependencies with:
```bash
pip install -r requirements.txt
```

## Troubleshooting

1. **API Key Not Found**: Ensure `/etc/secrets/IndicatorKey.txt` exists and contains only the API key.
2. **Webhook URLs Not Found**: Ensure `/etc/secrets/WebhookURLs.txt` exists and contains `TRADE_URL` and `NO_TRADE_URL`.
3. **Permission Errors**: Verify that `/etc/secrets/IndicatorKey.txt` and `/etc/secrets/WebhookURLs.txt` have restrictive permissions (`chmod 600`).

## Contributing

Feel free to submit issues or pull requests if you encounter bugs or have feature suggestions.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
