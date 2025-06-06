import sqlite3
import random


def val():
    value_password = 'dfgsa' + str(random.randint(100, 100000)) + '12sg45d'
    conn = sqlite3.connect('db/project.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET new_pas = ? WHERE inset = 1", (value_password,))
    conn.commit()
    n = input('Введите пароль для пополнения баланса: ')
    if n == value_password:
        cursor.execute("SELECT coins FROM users where inset = 1")
        balance = [i[0] for i in cursor.fetchall()][0]

        while True:
            try:
                m = input('Введите сумму, на которую хотите пополнить баланс: ')
                break
            except ValueError:
                print("❌ Введите число.")
                continue

        cursor.execute("UPDATE users SET coins = ? WHERE inset = 1", (int(m) + balance,))
        conn.commit()