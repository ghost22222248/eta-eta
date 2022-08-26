import os
import asyncio

import telegram
from telethon import TelegramClient, events
from datetime import datetime
import time
from telegram.ext import *
from telegram.ext import MessageHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Update
import random
import requests
import json

############################### Bot ############################################
server = 'https://telegram-lottery-default-rtdb.firebaseio.com/'
TOKEN = '5473836960:AAHesr86uOZFGlFgrNd8IIvPO0VjYdDOqA8'

#server = 'https://frantic-architect.firebaseio.com/'
#TOKEN = '5713462327:AAE9k5Lvqil1Y-2g6hajHXQYZH5rz14SMV8'


def start_message(name):
    return 'Hi {}.\nWelcome to Eta Eta! A classic game that offers 50/50 chance of winning.'.format(name)


def start(update, context):
    current_balance = 1000
    bet_size = 50
    user_choice = ''
    drawn_choice = ''
    # print(update.message.chat_id)
    r = requests.get(server + 'users/' + str(update.message.chat_id) + '.json')
    r2 = requests.get(server + 'users/' + str(update.message.chat_id) + '/current_balance.json')
    # print(r2.json())
    if (str(requests.get(server + 'users/' + str(update.message.chat_id) + '.json').json()) == 'None'):
        # print('registering')
        na = ''
        us = ''
        t = int(time.time())
        if (update.message.chat.first_name != None):
            na = na + update.message.chat.first_name
        if (update.message.chat.last_name != None):
            na = na + ' ' + update.message.chat.last_name

        if (update.message.chat.username != None):
            us = update.message.chat.username
        requests.put(server + 'users/' + str(update.message.chat_id) + '.json',
                     json={'chat_id': update.message.chat_id, 'current_balance': 1000, 'bet_size': 50, 'name': na,
                           'phone_number': 'x', 'username': us, 'last_time': '0', 'chance': 10, 'time_joined': t})
        update.message.reply_text('You have recieved bonus of 1000 coins (10 Birr) for registering')
        context.bot.send_message(chat_id='5010656317', text=str(update.message.chat_id) + ' has started bot')

    else:
        # print('recovering')
        current_balance = int(
            requests.get(server + 'users/' + str(update.message.chat_id) + '/current_balance.json').json())
        bet_size = int(requests.get(server + 'users/' + str(update.message.chat_id) + '/bet_size.json').json())

    # print(r.json())
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
    # print('chatid: '+str(query.message.chat_id))
    query.answer()
    current_balance = int(
        str(requests.get(server + 'users/' + str(query.message.chat_id) + '/current_balance.json').json()))
    bet_size = int(str(requests.get(server + 'users/' + str(query.message.chat_id) + '/bet_size.json').json()))
    chance = int(str(requests.get(server + 'users/' + str(query.message.chat_id) + '/chance.json').json()))
    last_t = 0
    t = 0
    phone = str(requests.get(server + 'users/' + str(query.message.chat_id) + '/phone_number.json').json())

    na = ''
    us = ''
    if (query.message.chat.first_name != None):
        na = na + query.message.chat.first_name
    if (query.message.chat.last_name != None):
        na = na + ' ' + query.message.chat.last_name

    if (query.message.chat.username != None):
        us = query.message.chat.username

    #print("chance b " + str(chance))
    # withamt=int(str(requests.get(server + 'users/' + str(update.message.chat_id) + '/active_withdraw.json').json()))
    # phone_number=str(requests.get(server + 'users/' + str(update.message.chat_id) + '/phone_number.json').json())
    # print(int(str(requests.get(server + 'users/' + str(query.message.chat_id) + '/current_balance.json').json())))
    user_choice = ''
    drawn_choice = ''
    # cn = random.randint(0, 1)
    # if(bet_size<100): cn = setwinprob(52)
    # else: cn = setwinprob(50)
    cn = setwinprob(random.randint(40, 50))
    # print('result: '+str(cn) +query.data+ ' '+altch(query.data))
    # if (query.data != ''):
    # print(query.data)
    if (cn == 0):
        drawn_choice = altch(query.data)
    else:
        drawn_choice = query.data

        #  query.message.reply_text(text=main_menu_message(drawn_choice,bet_size,current_balance),reply_markup=main_menu_keyboard())
        # print(query.data+'\n')
    if (query.data == 'pwf'):
        query.edit_message_text('Host a game or join using code: ', reply_markup=host_or_join_keyboard())
    if (query.data == 'deposit'):  # deposit
        uid = random.randint(136374, 9585634)
        requests.put(server + 'deposits/' + str(uid) + '.json',
                     json={'chat_id': query.message.chat_id, 'current_balance': current_balance
                           })

        query.edit_message_text('Your transfer id is : ' + str(
            uid) + '\n\nSend message to @headsandtails24:\n\nAmount:__\nTransfer id:__\n\nThe person may ask you more information.',
                                reply_markup=backtomain_keyboard())

    if (query.data == 'withdraw'):  # withdraw
        uid = random.randint(136374, 9585634)
        requests.put(server + 'withdraws/' + str(uid) + '.json',
                     json={'chat_id': query.message.chat_id, 'current_balance': current_balance
                           })

        query.edit_message_text('Your transfer id is : ' + str(
            uid) + '\n\nSend message to @headsandtails24:\n\nAmount:__\nTransfer id:__\nPhone number or Account number:__\n\nThe person may ask you more information.',
                                reply_markup=backtomain_keyboard())

    if (query.data == 'backto_main'):  # back button to main
        query.edit_message_text(text=main_menu_message(drawn_choice, bet_size, current_balance),
                                reply_markup=main_menu_keyboard())

    if (query.data == 'cbs'):  # change bet size
        query.edit_message_text('Choose bet size in coins', reply_markup=bet_choice_keyboard())
        # print('change-bet-size')

    if (conv(query.data) == 1 or conv(query.data) == 0):  # head or tail

        # print('heads or tails')

        if (current_balance < bet_size):  # low balance
            query.edit_message_text('You don\'t have enough balance.', reply_markup=balance_low_keyboard())
        if (chance == 0):  # no more chance
            query.edit_message_text('You have used all your chances today. Try again tommorrow.',
                                    reply_markup=backtomain_keyboard())
        if (current_balance > bet_size and chance > 0):  # enough balance
            # if (conv(query.data) == cn):  # won
            chance = chance - 1
            #print("chance a " + str(chance))
            if (cn == 1):
                #       print('won')
                current_balance += bet_size

                # requests.put(server + 'users/' + str(update.message.chat_id) + '/current_balance.json',current_balance)

                requests.put(server + 'users/' + str(query.message.chat_id) + '.json',
                             json={'chat_id': query.message.chat_id, 'current_balance': current_balance,
                                   'bet_size': bet_size, 'name': na, 'phone_number': phone, 'username': us,
                                   'last_time': last_t, 'chance': chance, 'time_joined': t})

                query.edit_message_text(won_message(drawn_choice, bet_size, current_balance))
                query.message.reply_text(text=main_menu_message(drawn_choice, bet_size, current_balance),
                                         reply_markup=main_menu_keyboard())

            else:  # lost
                #      print('lost')
                current_balance -= bet_size
                # requests.put(server + 'users/' + str(update.message.chat_id) + '/current_balance.json',current_balance)
                requests.put(server + 'users/' + str(query.message.chat_id) + '.json',
                             json={'chat_id': query.message.chat_id, 'current_balance': current_balance,
                                   'bet_size': bet_size, 'name': na, 'phone_number': phone, 'username': us,
                                   'last_time': last_t, 'chance': chance, 'time_joined': t})

                query.edit_message_text(lost_message(drawn_choice, bet_size, current_balance))
                query.message.reply_text(text=main_menu_message(drawn_choice, bet_size, current_balance),
                                         reply_markup=main_menu_keyboard())

    if (query.data[0:7] == 'c9000c_'):  # change bet size

        bet_size = int(query.data[7:len(query.data)])
        # requests.put(server + 'users/' + str(query.message.chat_id) + '/bet_size.json',int(query.data))
        requests.put(server + 'users/' + str(query.message.chat_id) + '.json',
                     json={'chat_id': query.message.chat_id, 'current_balance': current_balance, 'bet_size': bet_size,
                           'name': na, 'phone_number': phone, 'username': us, 'last_time': last_t, 'chance': chance,
                           'time_joined': t})
        query.edit_message_text('Bet size is changed to ' + query.data[7:len(query.data)] + ' coins.')
        query.message.reply_text(text=main_menu_message(drawn_choice, bet_size, current_balance),
                                 reply_markup=main_menu_keyboard())

        # multi player query handler

    if (query.data == 'backto_main_multi'):
        r = str(requests.get(server + 'users/' + str(query.message.chat_id) + '/multi_code.json').json())
        requests.delete(server + 'multi_player/' + r + '.json')
        requests.patch(server + 'users/' + str(query.message.chat_id) + '/.json', json={'multi_code': 'None'})
        query.edit_message_text(main_menu_message(drawn_choice, bet_size, current_balance),
                                reply_markup=main_menu_keyboard())
                                
                                
    if (query.data == 'cbs_m'):
        query.edit_message_text('Choose bet size: ', reply_markup=bet_choice_multi_keyboard())
    if (query.data[0:7] == 'c9001c_'):  # change multi bet size

        bet_size = int(query.data[7:len(query.data)])

        r = 'cd' + str(random.randint(1123253, 9999999))
        t = time.time()
        requests.put(server + 'multi_player/' + r + '.json',
                     json={'chat_id_h': query.message.chat_id,
                           'bet_size': bet_size, 'name_h': na, 'code': r, 'time_created': t, 'host_turn': 0,
                           'size': 1, 'chosen': 'none'
                           })

        requests.patch(server + 'users/' + str(query.message.chat_id) + '.json', json={'multi_code': r})
        query.edit_message_text(str(r))
        query.message.reply_text('👆👆👆👆👆\nYour invitation code is: ' + str(
            r) + '\nTell your friend to enter this code in his device and send it to the bot.\n\nWaiting for player to join...')

    if (query.data == 'host'):  # create game
        query.edit_message_text('Choose bet size: ', reply_markup=bet_choice_multi_keyboard())

    if (query.data == 'join'):
        query.edit_message_text('Enter invitation code: ',reply_markup=backtomain_keyboard())

    if (query.data == 'head_m' or query.data == 'tail_m'):
        r = str(requests.get(server + 'users/' + str(query.message.chat_id) + '/multi_code.json').json())


        if (str(requests.get(server + 'multi_player/' + r + '/.json').json()) != 'None'):
        
         tc=float(str(requests.get(server + 'multi_player/' + r + '/time_created.json').json()))
         tn=float(time.time())
         if(tn-tc<6*3600):
            updater = Updater(TOKEN, use_context=True)
            chat_id_h = str(requests.get(server + 'multi_player/' + r + '/chat_id_h.json').json())
            chat_id_j = str(requests.get(server + 'multi_player/' + r + '/chat_id_j.json').json())
            name_j = str(requests.get(server + 'multi_player/' + r + '/name_j.json').json())
            name_h = str(requests.get(server + 'multi_player/' + r + '/name_h.json').json())
            bet_size = int(str(requests.get(server + 'multi_player/' + r + '/bet_size.json').json()))

            if (chat_id_h == str(query.message.chat_id)):  # is host
                host_turn = int(str(requests.get(server + 'multi_player/' + r + '/host_turn.json').json()))
                current_balance_h = int(
                    str(requests.get(server + 'users/' + chat_id_h + '/current_balance.json').json()))
                if (current_balance_h >= bet_size):
                    if (host_turn == 0):  # prediction
                        chosen = str(requests.get(server + 'multi_player/' + r + '/chosen.json').json())
                        if (chosen != 'None' and query.data == chosen):
                            query.edit_message_text(won_message_multi(bet_size))
                            current_balance_h = current_balance_h + bet_size
                            requests.patch(server + 'users/' + str(query.message.chat_id) + '.json',
                                           json={'current_balance': current_balance_h})
                            updater.bot.send_message(chat_id=chat_id_j, text=lost_message_multi(bet_size))
                        if (chosen != 'None' and query.data != chosen):
                            query.edit_message_text(lost_message_multi(bet_size))
                            current_balance_h = current_balance_h - bet_size
                            requests.patch(server + 'users/' + str(query.message.chat_id) + '.json',
                                           json={'current_balance': current_balance_h})
                            updater.bot.send_message(chat_id=chat_id_j, text=won_message_multi(bet_size))
                        requests.patch(server + 'multi_player/' + r + '.json', json={'host_turn': 1})
                        updater.bot.send_message(chat_id=str(query.message.chat_id),
                                                 text=multiplayer_status_text(name_j, bet_size, current_balance_h))
                        query.message.reply_text('Make your choice and your opponent will try to guess it.',
                                                 reply_markup=heads_or_tails_multi_keyboard())
                        updater.bot.send_message(chat_id=chat_id_j,
                                                 text='Waiting for opponent to make a choice...\nThen you will guess it.')
                    else:

                        query.edit_message_text('Waiting for opponent to guess your choice...')
                        requests.patch(server + 'multi_player/' + r + '.json', json={'chosen': query.data})
                        updater.bot.send_message(chat_id=chat_id_j,
                                                 text='Your opponent has made a choice. Can you guess what it is?',
                                                 reply_markup=heads_or_tails_multi_keyboard())
                else:
                    query.edit_message_text('Not enough balance.')
            if (chat_id_j == str(query.message.chat_id)):  # is joined
                host_turn = int(str(requests.get(server + 'multi_player/' + r + '/host_turn.json').json()))
                current_balance_j = int(
                    str(requests.get(server + 'users/' + chat_id_j + '/current_balance.json').json()))
                if (current_balance_j >= bet_size):
                    if (host_turn == 1):  # prediction
                        chosen = str(requests.get(server + 'multi_player/' + r + '/chosen.json').json())
                        if (chosen != 'None' and query.data == chosen):
                            query.edit_message_text(won_message_multi(bet_size))
                            current_balance_j = current_balance_j + bet_size
                            requests.patch(server + 'users/' + str(query.message.chat_id) + '.json',
                                           json={'current_balance': current_balance_j})
                            updater.bot.send_message(chat_id=chat_id_h, text=lost_message_multi(bet_size))
                        if (chosen != 'None' and query.data != chosen):
                            query.edit_message_text(lost_message_multi(bet_size))
                            current_balance_j = current_balance_j - bet_size
                            requests.patch(server + 'users/' + str(query.message.chat_id) + '.json',
                                           json={'current_balance': current_balance_j})
                            updater.bot.send_message(chat_id=chat_id_h, text=won_message_multi(bet_size))
                        requests.patch(server + 'multi_player/' + r + '.json', json={'host_turn': 0})
                        updater.bot.send_message(chat_id=str(query.message.chat_id),
                                                 text=multiplayer_status_text(name_j, bet_size, current_balance_j))
                        query.message.reply_text('Make your choice and your opponent will try to guess it.',
                                                 reply_markup=heads_or_tails_multi_keyboard())
                        updater.bot.send_message(chat_id=chat_id_h,
                                                 text='Waiting for opponent to make a choice...\nThen you will guess it.')
                    else:

                        query.edit_message_text('Waiting for opponent to guess your choice...')
                        requests.patch(server + 'multi_player/' + r + '.json', json={'chosen': query.data})
                        updater.bot.send_message(chat_id=chat_id_h,
                                                 text='Your opponent has made a choice. Can you guess what it is?',
                                                 reply_markup=heads_or_tails_multi_keyboard())

                else:
                    query.edit_message_text('Not enough balance')
         else:
           query.edit_message_text('Session has expired.')
        else:
            query.edit_message_text('Session has expired.')


def multiplayer_status_text(other_player_name, bet_size, current_balance):
    text = 'Playing with: ' + other_player_name + '\n' + 'Bet size: '
    if (bet_size == 0):
        text = text + 'free'
    else:
        text = text + str(bet_size)

    text = text + '\nYour balance: ' + str(current_balance)
    return text


def won_message_multi(bet_size):
    text = '✅\n✅\nCongratulations!! You have won'
    if (bet_size == 0):
        text = text + '.'
    else:
        text = text + ' ' + str(bet_size)
    text=text+' coins.\n✅\n✅'
    # text=text+ 'You have correctly guessed the opponent\'s choice.'
    return text


def lost_message_multi(bet_size):
    text = '⛔️\n⛔️\nOops!! You have lost'
    if (bet_size == 0):
        text = text + '.'
    else:
        text = text + ' ' + str(bet_size)

    text=text+' coins.\n✅\n✅'
    # text=text+ 'You have incorrectly guessed the opponent\'s choice.'
    return text


def All_messages_handler(update, context):
    message = update.message.text
    if (message[0:2] == 'cd'):
        r = message
        if (str(requests.get(server + 'multi_player/' + r + '.json').json()) != 'None'):
         chat_id_h = str(requests.get(server + 'multi_player/' + r + '/chat_id_h.json').json())
         print(chat_id_h+' '+str(update.message.chat_id))
         if(chat_id_h!=str(update.message.chat_id)):
            #print('not equal')
            if (int(str(requests.get(server + 'multi_player/' + r + '/size.json').json())) != 2):
                na = ''
                if (update.message.chat.first_name != None):
                    na = na + update.message.chat.first_name
                if (update.message.chat.last_name != None):
                    na = na + ' ' + update.message.chat.last_name
                #print(na)

                name_h = str(requests.get(server + 'multi_player/' + r + '/name_h.json').json())
                t = time.time()
                bet_size_default = 50
                requests.patch(server + 'multi_player/' + r + '.json', json={'name_j': str(na)})
                requests.patch(server + 'multi_player/' + r + '.json', json={'chat_id_j': str(update.message.chat_id)})
                requests.patch(server + 'multi_player/' + r + '.json', json={'size': 2})

                requests.patch(server + 'users/' + str(update.message.chat_id) + '.json', json={'multi_code': r})
                current_balance_j = int(
                    str(requests.get(server + 'users/' + str(update.message.chat_id) + '/current_balance.json').json()))
                current_balance_h = int(
                    str(requests.get(server + 'users/' + str(chat_id_h) + '/current_balance.json').json()))
                bet_size = int(str(requests.get(server + 'multi_player/' + r + '/bet_size.json').json()))

                updater = Updater(TOKEN, use_context=True)
                # print(chat_id_h)
                # updater.bot.send_message(chat_id=str(chat_id_h),text='You are now playing with '+na)
                updater.bot.send_message(chat_id=str(chat_id_h), text='You are now playing with ' + na)

                updater.bot.send_message(chat_id=str(update.message.chat_id), text='You are now playing with ' + name_h)
                updater.bot.send_message(chat_id=str(update.message.chat_id),
                                         text=multiplayer_status_text(name_h, bet_size, current_balance_j),
                                         reply_markup=heads_or_tails_multi_keyboard())
                updater.bot.send_message(chat_id=str(chat_id_h),
                                         text=multiplayer_status_text(na, bet_size, current_balance_h))
                updater.bot.send_message(chat_id=str(chat_id_h),
                                         text='Waiting for ' + na + ' to choose head or tail...')

                updater.stop()

            else:
                update.message.reply_text('Players full')

         else:
             update.message.reply_text('You can not join your own invitation.')
        else:
            update.message.reply_text('wrong code')


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
        [InlineKeyboardButton('Play with friends', callback_data='pwf')],

    ]
    return InlineKeyboardMarkup(keyboard)


def balance_low_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Deposit', callback_data='deposit'),
            InlineKeyboardButton('Change Bet size', callback_data='cbs')
        ],
        [InlineKeyboardButton('Go back', callback_data='backto_main')],
    ]
    return InlineKeyboardMarkup(keyboard)


def won_message(drawn_choice, bet_size, current_balance):
    return '✅\n✅\nCongratulations!! You have won ' + str(
        bet_size) + ' coins. Coin landed on ' + drawn_choice + '. Your balance is ' + str(
        current_balance) + ' coins.\n✅\n✅'


def lost_message(drawn_choice, bet_size, current_balance):
    return '⛔️\n⛔️\nOops... you have lost ' + str(
        bet_size) + ' coins. Coin landed on ' + drawn_choice + '. Your balance is ' + str(
        current_balance) + ' coins.\n⛔️\n⛔️'


def main_menu_message(drawn_choice, bet_size, current_balance):
    return 'Heads or Tails?   Bet size: ' + str(bet_size) + ' coins\n\n(1 Birr = 100 coins)\n\nCurrent balance: ' + str(
        current_balance) + ' coins or ' + str(
        current_balance / 100) + ' Birr'


def host_or_join_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Invite a friend', callback_data='host'),
            InlineKeyboardButton('Join ( Enter code )', callback_data='join'),
        ],
        [
            InlineKeyboardButton('Back to main menu', callback_data='backto_main')
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def heads_or_tails_multi_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Head', callback_data='head_m'),
            InlineKeyboardButton('Tail', callback_data='tail_m'),
        ],
        [
            InlineKeyboardButton('Go back to main menu', callback_data='backto_main_multi')
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def bet_choice_multi_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Free', callback_data='c9001c_0')
        ],
        [
            InlineKeyboardButton('50', callback_data='c9001c_50'),
            InlineKeyboardButton('100', callback_data='c9001c_100'),
            InlineKeyboardButton('300', callback_data='c9001c_200'),
            InlineKeyboardButton('500', callback_data='c9001c_500')
        ],

        [
            InlineKeyboardButton('1000', callback_data='c9001c_1000'),
            InlineKeyboardButton('2000', callback_data='c9001c_2000'),
            InlineKeyboardButton('3000', callback_data='c9001c_3000'),
            InlineKeyboardButton('5000', callback_data='c9001c_5000')
        ],

        [
            InlineKeyboardButton('Go back', callback_data='backto_main')
        ],

    ]
    return InlineKeyboardMarkup(keyboard)


def main():
    
    # PORT=process.env.PORT

    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(All_queries_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, All_messages_handler))


    #updater.start_polling()
    
    PORT=int(os.environ.get("PORT",8443))
    #print("EXEC 7")
    #print("port "+str(PORT))
    updater.start_webhook(listen="0.0.0.0",port=PORT,url_path=TOKEN,webhook_url='https://etaeta24.herokuapp.com/' + TOKEN)
    #updater.idle()
    #updater.bot.setWebhook('https://etaeta24.herokuapp.com/' + TOKEN)
    print("done")

main()
