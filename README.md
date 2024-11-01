# OptionAlpha Webhook Integration with OpenAI GPT

This script serves as a webhook for an Option Alpha trading bot. It uses OpenAI's GPT API to analyze major world events and determine if the market conditions are favorable for trading. Designed for use with an iron condor trading strategy, the script triggers either a "Trade" or "No Trade" action based on the predicted market stability, pausing trades if volatility is expected.

## Features

- **World Event Analysis**: Queries OpenAI’s GPT-4 model for recent significant world events and assesses their potential impact on the S&P 500 (SPX).
- **Automated Trade Control**: Decides to either enable or pause trading based on potential market volatility.
- **Secure API Key Handling**: Retrieves the OpenAI API key from a secure file location to avoid hardcoding sensitive information in the script.

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

3. **Set Up API Key**:
   - Save your OpenAI API key in a file at `/etc/secrets/IndicatorKey.txt`.
   - Make sure the file has restricted permissions:
     ```bash
     chmod 600 /etc/secrets/IndicatorKey.txt
     ```

4. **Configure Webhook URLs**:
   - Update the `TRADE_URL` and `NO_TRADE_URL` variables in the script with the appropriate Option Alpha webhook URLs for enabling and pausing trades.

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

## Environment Security

This script securely retrieves the OpenAI API key from a file (`/etc/secrets/IndicatorKey.txt`) instead of hardcoding it in the code. Ensure the file has restricted read permissions for enhanced security.

## File Structure

```
.
├── option_alpha_webhook.py       # Main script
├── requirements.txt              # Python dependencies
└── README.md                     # This README file
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
2. **Webhook Not Triggering**: Check the logs to ensure that the correct URLs are set for `TRADE_URL` and `NO_TRADE_URL`.
3. **Permission Errors**: Verify that `/etc/secrets/IndicatorKey.txt` has restrictive permissions (`chmod 600`).

## Contributing

Feel free to submit issues or pull requests if you encounter bugs or have feature suggestions.
