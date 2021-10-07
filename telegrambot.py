import requests
import config


# Refer to this site on how these tokens and chatID's work
# https://medium.com/@ManHay_Hong/how-to-create-a-telegram-bot-and-send-messages-with-python-4cf314d9fa3e
def telegram_bot_sendtext(bot_message):

    bot_token = config.bot_token

    bot_chatID = config.bot_chatID

    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()
