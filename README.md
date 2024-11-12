# Telegram Message Forwarding Bot

## Overview
This project is a Python-based Telegram bot built using the **Telethon** library. The bot forwards messages from specific Telegram channels to designated target channels, processing messages and applying specific parsing logic. The code includes functionality for reading environment variables, handling new message events, and forwarding messages with custom logic.

## Features
- **Forwarding messages** from specific source channels to target channels.
- **Processing media and text** messages.
- **Custom parsing logic** to handle message content.
- **Environment configuration** using `.env` files.
- **Prompts** for generating titles and categories using AI.

## Requirements
- Python 3.8 or higher
- Telethon library
- Python-dotenv library

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/1nkret/parser_telegram
   cd parser_telegram
   ```

2. **Create and configure a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the root directory and add the following environment variables:
   ```env
   API_ID=<your_api_id>
   API_HASH=<your_api_hash>
   PHONE_NUMBER=<your_phone_number>
   API_KEY_AI=<api_key_google_ai>
   ENTITY=<https://t.me/target_channel>
   ```

## Usage
1. **Run the bot**:
   ```bash
   python main.py
   ```
2. **Input password** if prompted during startup.
3. The bot will listen for new messages in specified source channels and forward them to the target channels based on your configuration.

## Code Structure
- **`main.py`**: The main script that initializes the `TelegramClient`, loads environment variables, and handles new message events.
- **`apps/modules/forwarder.py`**: Contains the `parser` function that processes incoming messages and forwards them with specified logic.
- **`apps/utils/json_loader.py`**: Functions for loading JSON configurations for destination channels and allow lists.
- **`apps/utils/read_prompt.py`**: Functions for reading prompts for generating message titles and categories.

## How It Works
1. The bot starts by creating a `TelegramClient` using API credentials from the `.env` file.
2. It listens for new messages in specific channels defined by chat IDs.
3. When a new message event is detected, it processes the message using the `parser` function.
4. The message is forwarded to target channels if it matches the criteria specified in the allow list.
5. If the message includes media, it is downloaded and sent to the target channel with additional processing logic.

## Configuration
### Environment Variables
- **`API_ID`**: Your Telegram API ID.
- **`API_HASH`**: Your Telegram API hash.
- **`PHONE_NUMBER`**: Your phone number associated with the Telegram account.

### JSON Configuration
- **Destination channels** and **allow lists** are loaded from JSON files using `get_dest_channels()` and `get_allow_list()` functions.

## Notes
- Ensure that your Telegram account has access to the channels you want to forward messages from.
- Add appropriate error handling as needed for production use.
- Modify prompts and parsing logic according to your specific requirements.

## Dependencies
- **Telethon**: For connecting to Telegram and handling message events.
- **dotenv**: For loading environment variables from a `.env` file.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contribution
Feel free to contribute by opening issues or submitting pull requests. Ensure that any new features or changes are well-documented.

