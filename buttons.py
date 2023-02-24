import telebot, config
bot = telebot.TeleBot(config.TOKEN)

def Buttons(buttons):
    markup = telebot.types.ReplyKeyboardRemove()
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(*buttons)
    return markup

def date(dd = 1, mm = 1, yy = 2022):
    ib1 = telebot.types.InlineKeyboardButton('+', callback_data='d+')
    ib2 = telebot.types.InlineKeyboardButton('+', callback_data='m+')
    ib3 = telebot.types.InlineKeyboardButton('+', callback_data='y+')
    ib4 = telebot.types.InlineKeyboardButton(dd, callback_data=dd)
    ib5 = telebot.types.InlineKeyboardButton(mm, callback_data=mm)
    ib6 = telebot.types.InlineKeyboardButton(yy, callback_data=yy)
    ib7 = telebot.types.InlineKeyboardButton('-', callback_data='d-')
    ib8 = telebot.types.InlineKeyboardButton('-', callback_data='m-')
    ib9 = telebot.types.InlineKeyboardButton('-', callback_data='y-')
    mark = telebot.types.InlineKeyboardMarkup()
    mark.row(ib1, ib2, ib3)
    mark.row(ib4, ib5, ib6)
    mark.row(ib7, ib8, ib9)
    return mark