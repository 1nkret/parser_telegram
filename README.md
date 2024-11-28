
# Telegram Parser

This project includes a script for parsing data from Telegram channels with sorting and export capabilities.

## Features

- **Telegram Channel Parser**:
  - Extracts and sorts data from channel posts.
  - Exports results in a user-friendly format.
  - Notifies users if the parser cannot identify a project name in a post.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/1nkret/parser_telegram.git
   cd parser_telegram
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the `.env` file:

   Create a `.env` file in the root directory and specify the following parameters:
   ```
   API_ID="id"
   API_HASH="hash"
   PHONE_NUMBER="+XXX-ph-one-numb"
   API_KEY_AI="api_key_google_ai"
   ENTITY="https://t.me/target_channel"
   CHATS="chat_to_parse"
   BOT_TOKEN="TOKENBOT"
   BOT_ADMINS="admin1_id,admin2_id,admin3_id..."
   ```

## Usage

Run the script:

```bash
python main.py
```

## Technologies Used
- Python
- Aiogram 3
- Telethon
- MongoDB
- Google AI

## Notes

- Ensure you have access to the Telegram API. Learn more about creating an application [here](https://core.telegram.org/api/obtaining_api_id).
- The script includes client-specific logic but can be adapted for other use cases.

## Support

For questions or issues, feel free to open a new Issue in the repository.
