import telebot
from urllib.request import Request, urlopen
import json
import matplotlib.pyplot as plt

url='https://api.coincap.io/v2/assets'
r = Request(url, headers={"User-Agent": "Mozilla/5.0"})
data = urlopen(r).read().decode()
res = json.loads(data)
list_of_currency=list(res['data'][i]['name'] for i in range(len(res['data'])))
list_of_currency=list(i.lower() for i in list_of_currency)

def price(reply):
    for i in range(len(res['data'])):
        if reply == list_of_currency[i]:
            return f"{res['data'][i]['name']} costs {round(float(res['data'][i]['priceUsd']),3)}$ ({round(float(res['data'][i]['changePercent24Hr']),2)}%)."
    else:
        return 'Incorrect request. Try again.'

def scedule(reply,dur):
    dick={'year':'d1','month':'h1','day':'m1'}   
    url=f'https://api.coincap.io/v2/assets/{reply.lower()}/history?interval={dick[dur]}'
    r = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urlopen(r).read().decode()
    res = json.loads(data)
    prices=list(float(res['data'][i]['priceUsd']) for i in range(len(res['data'])))

    if dick[dur]=='d1':
        prices=prices[len(res['data'])-366:]
    elif dick[dur]=='h1' or dick[dur]=='m30':   
        pass

    plt.figure(figsize=(10,10))
    if(prices[0]<prices[-1]):
        plt.plot(prices,'g')
    elif(prices[0]>prices[-1]):
        plt.plot(prices,'r')
    else:
        plt.plot(prices)
    plt.ylabel('Price, USD')
    plt.title(f'{reply.capitalize()} Scedule for {dur}:')
    plt.savefig('plot.png')

bot=telebot.TeleBot('1458884343:AAHMyem3cVWjUgCLxG0SvdFawDXhJQqq81Q')

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Hi, I'm Lowrence - cryptocurrency bot, and I'd like to help you. Chose the command.")

@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.chat.id, "I can send you current crypto prices and make different scedules. Chose the command. ")

@bot.message_handler(commands=['price'])
def about_price(message):
	bot.send_message(message.chat.id, "Enter cryptocurrency.")

@bot.message_handler(commands=['scedule'])
def about_scedules(message):
	bot.send_message(message.chat.id, "Enter cryptocurrency and period like: 'Bitcoin day' for day scedule, 'Etherium month' for month scedule, and 'Litecoin year' for year scedule.")

@bot.message_handler(content_types=['text'])
def main(message):
    mes=message.text.lower()
    if len(mes.split(' '))==2:
        if(mes.split(' ')[1] in 'dayyearmonth' and mes.split(' ')[0] in list_of_currency):
            scedule(mes.split(' ')[0],mes.split(' ')[1])
            photo=open('plot.png','rb')
            bot.send_photo(message.chat.id,photo)
        else:
            bot.send_message(message.chat.id, 'Incorrect request. Try again.')
    else:
        bot.send_message(message.chat.id, price(mes))  

bot.polling(none_stop=True)
