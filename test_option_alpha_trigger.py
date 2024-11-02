import unittest
from unittest.mock import patch, Mock
import requests
from option_alpha_webhook import (
    ask_gpt,
    fetch_world_events,
    analyze_impact,
    is_trade_recommended,
    trigger_option_alpha,
)

class TestOptionAlphaTrigger(unittest.TestCase):

    @patch('option_alpha_webhook.requests.post')
    def test_ask_gpt_success(self, mock_post):
        # Mock the response from OpenAI API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {"content": "Test response from GPT-4"}
            }]
        }
        mock_post.return_value = mock_response

        # Call the function
        response = ask_gpt("Test prompt")

        # Assertions
        self.assertEqual(response, "Test response from GPT-4")
        mock_post.assert_called_once_with(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4",
                "messages": [{"role": "user", "content": "Test prompt"}],
                "max_tokens": 150,
            },
            timeout=10
        )

    @patch('option_alpha_webhook.requests.post')
    def test_ask_gpt_timeout(self, mock_post):
        # Simulate a timeout
        mock_post.side_effect = requests.exceptions.Timeout

        # Call the function and assert Exception is raised
        with self.assertRaises(Exception) as context:
            ask_gpt("Test prompt")

        self.assertIn("Request to OpenAI API timed out.", str(context.exception))
        mock_post.assert_called_once()

    @patch('option_alpha_webhook.ask_gpt')
    def test_fetch_world_events(self, mock_ask_gpt):
        # Mock the ask_gpt function
        mock_ask_gpt.return_value = "Mocked world events."

        # Call the function
        events = fetch_world_events()

        # Assertions
        self.assertEqual(events, "Mocked world events.")
        mock_ask_gpt.assert_called_once_with("What major world events have occurred in the last 24 hours?")

    @patch('option_alpha_webhook.ask_gpt')
    def test_analyze_impact_success(self, mock_ask_gpt):
        # Mock the ask_gpt function
        mock_response = '{"impact": "No", "explanation": "No significant events."}'
        mock_ask_gpt.return_value = mock_response

        # Call the function
        impact_analysis = analyze_impact("Mocked events.")

        # Assertions
        self.assertEqual(impact_analysis, {"impact": "No", "explanation": "No significant events."})
        mock_ask_gpt.assert_called_once()

    @patch('option_alpha_webhook.ask_gpt')
    def test_analyze_impact_json_error(self, mock_ask_gpt):
        # Mock the ask_gpt function with invalid JSON
        mock_response = 'Invalid JSON response'
        mock_ask_gpt.return_value = mock_response

        # Capture printed output
        with patch('builtins.print') as mock_print:
            # Call the function
            impact_analysis = analyze_impact("Mocked events.")

            # Assertions
            self.assertEqual(impact_analysis, {
                "impact": "Unknown",
                "explanation": "Unable to parse ChatGPT JSON response."
            })
            mock_print.assert_called_once()
            self.assertIn("Failed to parse GPT response as JSON.", mock_print.call_args[0][0])

    def test_is_trade_recommended(self):
        # Test cases
        test_cases = [
            ({"impact": "No", "explanation": "No significant events."}, True),
            ({"impact": "Yes", "explanation": "Significant events detected."}, False),
            ({"impact": "Unknown", "explanation": "Unable to parse response."}, False),
            ({}, False),
        ]

        for impact_analysis, expected in test_cases:
            with self.subTest(impact_analysis=impact_analysis):
                result = is_trade_recommended(impact_analysis)
                self.assertEqual(result, expected)

    @patch('option_alpha_webhook.requests.post')
    def test_trigger_option_alpha_success(self, mock_post):
        # Mock the response from the webhook
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Call the function
        result = trigger_option_alpha("http://example.com/webhook")

        # Assertions
        self.assertTrue(result)
        mock_post.assert_called_once_with("http://example.com/webhook", timeout=10)

    @patch('option_alpha_webhook.requests.post')
    def test_trigger_option_alpha_failure(self, mock_post):
        # Mock the response from the webhook with a bad status code
        mock_response = Mock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        # Call the function
        result = trigger_option_alpha("http://example.com/webhook")

        # Assertions
        self.assertFalse(result)
        mock_post.assert_called_once_with("http://example.com/webhook", timeout=10)

    @patch('option_alpha_webhook.requests.post')
    def test_trigger_option_alpha_timeout(self, mock_post):
        # Simulate a timeout
        mock_post.side_effect = requests.exceptions.Timeout

        # Capture printed output
        with patch('builtins.print') as mock_print:
            # Call the function
            result = trigger_option_alpha("http://example.com/webhook")

            # Assertions
            self.assertFalse(result)
            mock_print.assert_called_once_with("Request to Option Alpha API timed out.")
            mock_post.assert_called_once_with("http://example.com/webhook", timeout=10)

if __name__ == '__main__':
    unittest.main()