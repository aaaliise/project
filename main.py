#from scripts import db_session
from games.black import blackgak
from scripts.initing import init_db
from author import login
import sqlite3

def main():
    init_db()
    print("Добро пожаловать в PYTHON CASINO!\nГде каждый может испытать свою удачу!\nДля начала игры нужно пройти авторизацию\n")
    login()
    game = ''
    while game != 'stop':
        game = input('В какую игры вы хотите сыграть (выберете из предложенного)\n'
                 '(Блэкджек/Lucky Dice)\n'
                 'для выхода напишите "stop" без кавычек ').strip()
        if game == 'Блэкджек':
            blackgak()
        elif game == 'Lucky Dice':
            blackgak()
        else:
            print('Неверный формат ввода.')


main()


