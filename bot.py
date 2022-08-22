import os
import asyncio
from telethon import TelegramClient, events
from datetime import datetime
import time
from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
import random
import requests
import json

############################### Bot ############################################
server = 'https://telegram-lottery-default-rtdb.firebaseio.com/'


def start_message(name):
    return 'Hi {}.\nWelcome to Eta Eta! A classic game that offers 50/50 chance of winning.'.format(name)


def start(update, context):
    current_balance = 1000
    bet_size = 50
    user_choice = ''
    drawn_choice = ''
    #print(update.message.chat_id)
    r = requests.get(server + 'users/' + str(update.message.chat_id) + '.json')
    r2 = requests.get(server + 'users/' + str(update.message.chat_id) + '/current_balance.json')
    #print(r2.json())
    if (str(requests.get(server + 'users/' + str(update.message.chat_id) + '.json').json()) == 'None'):
        #print('registering')
        
        requests.put(server + 'users/' + str(update.message.chat_id) + '.json',
                     json={'chat_id': update.message.chat_id, 'current_balance': 1000, 'bet_size': 50,'name':update.message.chat.first_name,'phone_number':'x','chance':10})
        update.message.reply_text('You have recieved bonus of 1000 coins (10 Birr) for registering')   
        context.bot.send_message(chat_id='5010656317', text=str(update.message.chat_id)+ ' has started bot')
                     
    else:
        #print('recovering')
        current_balance = int(
            requests.get(server + 'users/' + str(update.message.chat_id) + '/current_balance.json').json())
        bet_size = int(requests.get(server + 'users/' + str(update.message.chat_id) + '/bet_size.json').json())

    #print(r.json())
    update.message.reply_text(start_message(update.message.chat.first_name))
    
    update.message.reply_text(main_menu_message(drawn_choice, bet_size, current_balance),
                              reply_markup=main_menu_keyboard())


def conv(inp):
    if (inp == 'heads'):
        return 1
    if (inp == 'tails'):
        return 0
    if (inp == 'cbs'):
        return 2
    if (inp == 'back'):
        return 4
    if (inp == 'deposit'):
        return 5
    if (inp == 'withdraw'):
        return 6


def setwinprob(prob):
    ch = random.randint(1, 100)
    if (ch <= prob):
        return 1
    else:
        return 0


def altch(drawn_choice):
    if (drawn_choice == 'heads'):
        return 'tails'
    else:
        return 'heads'


def All_queries_handler(update, context):
    query = update.callback_query
    #print('chatid: '+str(query.message.chat_id))
    query.answer()
    current_balance = int(
        str(requests.get(server + 'users/' + str(query.message.chat_id) + '/current_balance.json').json()))
    bet_size = int(str(requests.get(server + 'users/' + str(query.message.chat_id) + '/bet_size.json').json()))
    chance = int(str(requests.get(server + 'users/' + str(query.message.chat_id) + '/chance.json').json()))
    print("chance b "+str(chance))
    # withamt=int(str(requests.get(server + 'users/' + str(update.message.chat_id) + '/active_withdraw.json').json()))
    # phone_number=str(requests.get(server + 'users/' + str(update.message.chat_id) + '/phone_number.json').json())
    #print(int(str(requests.get(server + 'users/' + str(query.message.chat_id) + '/current_balance.json').json())))
    user_choice = ''
    drawn_choice = ''
    # cn = random.randint(0, 1)
    #if(bet_size<100): cn = setwinprob(52)
    #else: cn = setwinprob(50)
    cn = setwinprob(random.randint(40,50))
    # print('result: '+str(cn) +query.data+ ' '+altch(query.data))
    #if (query.data != ''):
       # print(query.data)
    if (cn == 0):
        drawn_choice = altch(query.data)
    else:
        drawn_choice = query.data

    #  query.message.reply_text(text=main_menu_message(drawn_choice,bet_size,current_balance),reply_markup=main_menu_keyboard())
    # print(query.data+'\n')
    if (query.data == 'deposit'):  # deposit
        uid = random.randint(136374, 9585634)
        requests.put(server + 'deposits/' + str(uid) + '.json',
                     json={'chat_id': query.message.chat_id, 'current_balance': current_balance
                           })

        query.edit_message_text('Your transfer id is : '+ str(uid) +'\n\nSend message to @headsandtails24:\n\nAmount:__\nTransfer id:__\n\nThe person may ask you more information.',
                                reply_markup=backtomain_keyboard())

    if (query.data == 'withdraw'):  # withdraw
        uid = random.randint(136374,9585634)
        requests.put(server + 'withdraws/' + str(uid) + '.json',
                     json={'chat_id': query.message.chat_id, 'current_balance': current_balance
                           })

        query.edit_message_text('Your transfer id is : '+ str(uid) +'\n\nSend message to @headsandtails24:\n\nAmount:__\nTransfer id:__\nPhone number or Account number:__\n\nThe person may ask you more information.',
                                reply_markup=backtomain_keyboard())

    if (query.data == 'backto_main'):  # back button to main
        query.edit_message_text(text=main_menu_message(drawn_choice, bet_size, current_balance),
                                reply_markup=main_menu_keyboard())

    if (query.data == 'cbs'):  # change bet size
        query.edit_message_text('Choose bet size in coins', reply_markup=bet_choice_keyboard())
        #print('change-bet-size')

    if (conv(query.data) == 1 or conv(query.data) == 0):  # head or tail

        #print('heads or tails')

        if (current_balance < bet_size):  # low balance
            query.edit_message_text('You don\'t have enough balance.', reply_markup=balance_low_keyboard())
        if(chance==0): #no more chance
            query.edit_message_text('You have used all your chances today. Try again tommorrow.', reply_markup=main_menu_keyboard())
        if(current_balance>bet_size and chance>0):  # enough balance
            # if (conv(query.data) == cn):  # won
            chance=chance-1;
            print("chance a "+str(chance))
            if (cn == 1):
         #       print('won')
                current_balance += bet_size
                  
                # requests.put(server + 'users/' + str(update.message.chat_id) + '/current_balance.json',current_balance)

                requests.put(server + 'users/' + str(query.message.chat_id) + '.json',
                             json={'chat_id': query.message.chat_id, 'current_balance': current_balance,
                                   'bet_size': bet_size,'chance': chance})
           
                query.edit_message_text(won_message(drawn_choice, bet_size, current_balance))
                query.message.reply_text(text=main_menu_message(drawn_choice, bet_size, current_balance),
                                         reply_markup=main_menu_keyboard())

            else:  # lost
          #      print('lost')
                current_balance -= bet_size
                # requests.put(server + 'users/' + str(update.message.chat_id) + '/current_balance.json',current_balance)
                requests.put(server + 'users/' + str(query.message.chat_id) + '.json',
                             json={'chat_id': query.message.chat_id, 'current_balance': current_balance,
                                   'bet_size': bet_size,'chance': chance})

                query.edit_message_text(lost_message(drawn_choice, bet_size, current_balance))
                query.message.reply_text(text=main_menu_message(drawn_choice, bet_size, current_balance),
                                         reply_markup=main_menu_keyboard())

    if (query.data[0:7] == 'c9000c_'):  # change bet size

        bet_size = int(query.data[7:len(query.data)])
        # requests.put(server + 'users/' + str(query.message.chat_id) + '/bet_size.json',int(query.data))
        requests.put(server + 'users/' + str(query.message.chat_id) + '.json',
                     json={'chat_id': query.message.chat_id, 'current_balance': current_balance, 'bet_size': bet_size})
        query.edit_message_text('Bet size is changed to ' + query.data[7:len(query.data)] + ' coins.')
        query.message.reply_text(text=main_menu_message(drawn_choice, bet_size, current_balance),
                                 reply_markup=main_menu_keyboard())









def bet_choice_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('50', callback_data='c9000c_50'),
            InlineKeyboardButton('100', callback_data='c9000c_100'),
            InlineKeyboardButton('300', callback_data='c9000c_200'),
            InlineKeyboardButton('500', callback_data='c9000c_500')
        ],

        [
            InlineKeyboardButton('1000', callback_data='c9000c_1000'),
            InlineKeyboardButton('2000', callback_data='c9000c_2000'),
            InlineKeyboardButton('3000', callback_data='c9000c_3000'),
            InlineKeyboardButton('5000', callback_data='c9000c_5000')
        ],

        
        [
            InlineKeyboardButton('Go back', callback_data='backto_main')
        ],

    ]
    return InlineKeyboardMarkup(keyboard)


def keyboards():
    keyboard = [
        [
            KeyboardButton('Play', callback_data='play')
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def backtomain_keyboard():
    keyboard = [

        [
            InlineKeyboardButton('Go back to main menu', callback_data='backto_main')
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Heads', callback_data='heads'),
            InlineKeyboardButton('Tails', callback_data='tails')
        ],
        [
            InlineKeyboardButton('Deposit', callback_data='deposit'),
            InlineKeyboardButton('Withdraw', callback_data='withdraw')
        ],
        [InlineKeyboardButton('Change bet size', callback_data='cbs')],
    ]
    return InlineKeyboardMarkup(keyboard)


def balance_low_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Deposit', callback_data='deposit'),
            InlineKeyboardButton('Change Bet size', callback_data='cbs')
        ],
        [InlineKeyboardButton('Go back', callback_data='back')],
    ]
    return InlineKeyboardMarkup(keyboard)


def won_message(drawn_choice, bet_size, current_balance):
    return '*\n*\nCongratulations!! You have won ' + str(
        bet_size) + ' coins. Coin landed on ' + drawn_choice + '. Your balance is ' + str(
        current_balance) + ' coins.\n*\n*'


def lost_message(drawn_choice, bet_size, current_balance):
    return '*\n*\nOops... you have lost ' + str(
        bet_size) + ' coins. Coin landed on ' + drawn_choice + '. Your balance is ' + str(
        current_balance) + ' coins.\n*\n*'


def main_menu_message(drawn_choice, bet_size, current_balance):
    return 'Heads or Tails?   Bet size: ' + str(bet_size) + ' coins\n\n(1 Birr = 100 coins)\n\nCurrent balance: ' + str(
        current_balance) + ' coins or ' + str(
        current_balance / 100) + ' Birr'


def main():
    TOKEN = '5473836960:AAHesr86uOZFGlFgrNd8IIvPO0VjYdDOqA8'
    # PORT=process.env.PORT

    updater = Updater('5473836960:AAHesr86uOZFGlFgrNd8IIvPO0VjYdDOqA8', use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(All_queries_handler))

    #updater.start_polling()
    
    PORT=int(os.environ.get("PORT",8443))
    #print("EXEC 7")
    #print("port "+str(PORT))
    updater.start_webhook(listen="0.0.0.0",port=PORT,url_path=TOKEN,webhook_url='https://etaeta24.herokuapp.com/' + TOKEN)
    #updater.idle()
    #updater.bot.setWebhook('https://etaeta24.herokuapp.com/' + TOKEN)
    print("done")


main()




