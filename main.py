from games.black import blackgak
from scripts.initing import init_db
from author import login
from games.lucky import luck
from games.rule import play_slots
from games.tower import TowerGame
from val import val
import sqlite3


def main():
    init_db()
    print(
        "Добро пожаловать в PYTHON CASINO!\nГде каждый может испытать свою удачу!\nДля начала игры нужно пройти авторизацию\n")
    login()
    while True:
        conn = sqlite3.connect('db/project.db')
        cursor = conn.cursor()
        cursor.execute("SELECT coins FROM users where inset = 1")
        balance = [i[0] for i in cursor.fetchall()][0]
        print(f"\n💰 Ваш баланс: {balance} фишек")
        game = input('В какую игры вы хотите сыграть (выберете из предложенного)\n'
                     '(Блэкджек/Lucky_Dice/Слоты/Башня)\n'
                     'для пополнения баланса напишите "value" без кавычек\n'
                     'для выхода напишите "stop" без кавычек ').strip()
        if game == 'Блэкджек':
            blackgak()
        elif game == 'Lucky_Dice':
            luck()
        elif game == 'Слоты':
            play_slots()
        elif game == 'Башня':
            game = TowerGame()
            game.main_loop()
        elif game == 'stop':
            break
        elif game == 'value':
            val()
        else:
            print('Неверный формат ввода.')


main()
