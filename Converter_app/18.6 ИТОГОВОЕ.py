import telebot
from config import token, keys
from extensions import ExchangeException, Exchange

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Привет! Я бот-помощник, сконвертирую для Тебя валюту:  \n- Показать список доступных валют через команду /values \
\n- Чтобы сконвертировать валюту введи <имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n \
PS: важно при введении нецелого числа использовать точку вместо запятой, например: биткоин busd 0.15 \n \
- Помощь /help'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n  - '.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ExchangeException('Введите 3 параметра или воспользуйтесь помощью /help')

        quote, base, amount = values
        total_base = Exchange.get_price(quote, base, amount)
        if float(amount) <= 0:
            raise ExchangeException('Количество валюты должно быть больше нуля \n'
                                    'Попробуй еще раз')
    except ExchangeException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    else:
        text = f'Переводим {quote} в {base}\n{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()