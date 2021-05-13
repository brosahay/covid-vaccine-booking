import os
from telegram.client import Telegram
from utils import get_saved_user_info, save_user_info


def create_tg_client_config(tg_config_file: str = "tg-config.json"):
    api_id = input("Enter the Telegram API ID: ")
    api_hash = input("Enter the Telegram API hash: ")
    phone = input("Enter your mobile number registered with Telegram: ")
    encryption_key = input("Enter database secret key: ")
    tg_config = {
        'api_id': api_id,
        'api_hash': api_hash,
        'phone': phone,
        'encryption_key': encryption_key
    }
    save_user_info(tg_config_file, tg_config)
    return tg_config


def read_tg_client_config(tg_config_file: str = "tg-config.json"):
    client_details = None
    if os.path.exists(tg_config_file):
        client_details = get_saved_user_info(tg_config_file)
    else:
        client_details = create_tg_client_config()
    return client_details


def initialize_tg_client(tg_config_file: str = "tg-config.json"):
    client_config = read_tg_client_config(tg_config_file)
    client = Telegram(
        api_id=client_config.get("api_id"),
        api_hash=client_config.get("api_hash"),
        phone=client_config.get("phone"),
        database_encryption_key=client_config.get("encryption_key")
    )
    return client


def new_message_handler(update):
    # we want to process only text messages
    message_content = update['message']['content'].get('text', {})
    message_text = message_content.get('text', '').lower()

    if message_text == 'ping':
        chat_id = update['message']['chat_id']
        print(f'Ping has been received from {chat_id}')
    return


def main():
    tg_client = initialize_tg_client()
    tg_client.login()
    tg_client.add_message_handler(new_message_handler)
    tg_client.idle()
    return


if __name__ == '__main__':
    main()
