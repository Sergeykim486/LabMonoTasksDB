import config, buttons, telebot, functions, os
from AccessDatabase import AccessDB
from datetime import datetime
script_dir = os.path.dirname(os.path.abspath(__file__))
AbsPathDir = script_dir + '/DataBase/'
db = AccessDB(AbsPathDir + 'Database.accdb')
ActiveUser = {}
bot = telebot.TeleBot(config.TOKEN)

def conftext(message):
    global ActiveUser
    mestext = 'Подтвердите правильность введенной информации.\n'
    mestext = mestext + 'Ваш id:' + ActiveUser[message.chat_id]['id'] + '\n'
    mestext = mestext + 'Имя:' + ActiveUser[message.chat_id]['FirstName'] + '\n'
    mestext = mestext + 'Фамилия:' + ActiveUser[message.chat_id]['LastName'] + '\n'
    mestext = mestext + 'Телефон:' + ActiveUser[message.chat_id]['PhoneNumber'] + '\n'
    return mestext

@bot.message_handler(commands=['start'])

def send_welcome(message):
    global ActiveUser
    ActiveUser[message.chat_id] = {'id': message.chat_id}
    if db.find_record("Users", "id", message.chat_id) == None:
        bot.send_message(message.chat_id, 'Вам нужно пройти регистрацию', reply_markup=Buttons(['Регистрация']))
        bot.register_next_step_handler(message, register.reg1)
    
@bot.message_handler(content_types=['text'])

class register:
    
    def reg1(message):
        if message.text == 'Регистрация':
            bot.send_message(message.chat_id, 'Как Вас зовут (укажите имя)', reply_markup='')
            bot.register_next_step_handler(message, register.reg2)
        else:
            bot.send_message(message.chat_id, 'Пожалуйста зарегистрируйтесь.', reply_markup=buttons.Buttons(['Регистрация']))
            bot.register_next_step_handler(message, register.reg1)
    
    def reg2(message):
        global ActiveUser
        ActiveUser[message.chat_id]['FirstName'] = message.text
        bot.send_message(message.chat_id, 'Укажите Вашу фамилию.', reply_markup='')
        bot.register_next_step_handler(message, register.reg3)
    
    def reg3(message):
        global ActiveUser
        ActiveUser[message.chat_id]['LastName'] = message.text
        bot.send_message(message.chat_id, 'Введите Ваш номер телефона в формате (+998 00 000 0000).', )
        bot.register_next_step_handler(message, register.reg4)
    
    def reg4(message):
        global ActiveUser
        ActiveUser[message.chat_id]['PhoneNumber'] = message.text
        bot.send_message(message.chat_id, conftext(message), reply_markup=buttons.Buttons(['Да', 'Нет']))
        bot.register_next_step_handler(message, register.reg5)
    
    def reg5(message):
        global ActiveUser
        if message.text == 'Да':
            valuedict = {'id': ActiveUser[message.chat_id]['id'], 'FirstName': ActiveUser[message.chat_id]['FirstName'], 'LastName': ActiveUser[message.chat_id]['LastName'], 'PhoneNumber': ActiveUser[message.chat_id]['PhoneNumber']}
            db.add_record('Users', valuedict)
            bot.send_message(message.chat_id, 'Поздравляем Вы успешно зарегистрировались!', reply_markup=buttons.Buttons(['Главное меню']))
            bot.register_next_step_handler(message, MainMenu.Main1)
        elif message.text == 'Нет':
            bot.send_message(message.chat_id, 'Введите данные повторно.', reply_markup='')
            bot.register_next_step_handler(message, register.reg1)
        else:
            bot.send_message(message.chat_id, 'Вы не подтвердили информацию!\n' + conftext(message), reply_markup=buttons.Buttons(['Да', 'Нет']))
            bot.register_next_step_handler(message, register.reg5)

class MainMenu:
    def Main1(message):
        global ActiveUser
        ActiveUser[message.chat_id].clear()
        bot.send_message(message.chat_id, 'Добро пожаловать в систему. Что вы хотите сделать.', reply_markup=buttons.Buttons(['Новая заявка', 'Список заявок', 'Написать всем']))
        bot.register_next_step_handler(message, MainMenu.Main2)
    
    def Main2(message):
        if message.text == 'Новая заявка':
            bot.send_message(message.chat_id, 'Добавление заявки.', reply_markup='')
            bot.register_next_step_handler(message, NewTask.nt1)
        else:
            bot.send_message(message.chat_id, 'Не верная команда!', reply_markup=buttons.Buttons(['Новая заявка', 'Список заявок', 'Написать всем']))
            bot.register_next_step_handler(message, MainMenu.Main2)
            
class NewTask:
    def nt1(message):
        global ActiveUser
        ActiveUser[message.chat_id]['date'] = datetime.now()
        bot.send_message(message.chat_id, 'Укажите ИНН контрагента или выберите из списка.', reply_markup=buttons.Buttons(functions.ListGen(['id', 'CompanyName'])))
        bot.register_next_step_handler(NewTask.nt2)
    
    def nt2(message):
        global ActiveUser
        mes = message.text.split()
        cont = db.find_record('Contragents', 'id', int(mes[0]))
        if cont['id'] != None:
            bot.send_message(message.chat_id, f'')

bot.polling(none_stop=True, interval=0)