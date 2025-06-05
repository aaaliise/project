import getpass
import re
import sqlite3
from scripts.initing import init_db


def is_password_strong(password):
    """Проверяет, соответствует ли пароль требованиям сложности"""
    if len(password) < 8:
        print("Пароль должен содержать минимум 8 символов!")
        return False
    if not re.search(r"[A-Za-z]", password):
        print("Пароль должен содержать буквы!")
        return False
    if not re.search(r"\d", password):
        print("Пароль должен содержать цифры!")
        return False
    return True


def register():
    print("\nРегистрация нового пользователя")

    conn = sqlite3.connect('db/project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users")
    users = [i[0] for i in cursor.fetchall()]
    print(users)

    while True:
        username = input("Придумайте имя пользователя: ").strip()

        if username in users:
            print("Это имя уже занято. Попробуйте другое.")
            continue

        while True:
            password = input("Придумайте пароль, в нём должны быть буквы и цифры, \n"
                             "а также его длина должна быть не менее 8 символов: ").strip()
            if not is_password_strong(password):
                continue  # Пароль не прошёл проверку

            confirm_password = input("Подтвердите пароль: ").strip()

            if password != confirm_password:
                print("Ошибка: пароли не совпадают. Попробуйте ещё раз.")
            else:
                cursor.execute(
                    "insert into users (name, coins, password, inset) values (?, 100, ?, 1)",
                    (username, password))
                conn.commit()
                print(f"Пользователь {username} успешно зарегистрирован!")
                return username


def login():
    print("Добро пожаловать в систему авторизации!")
    conn = sqlite3.connect('db/project.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET inset = 0;")
    conn.commit()

    while True:
        username = input("\nВведите имя пользователя: ").strip()

        cursor.execute("SELECT name FROM users")
        users = [i[0] for i in cursor.fetchall()]
        print(users)

        if username not in users:
            answer = input("Такого пользователя нет. Хотите зарегистрироваться? (y/n): ").strip().lower()
            if answer == "y":
                username = register()
                print(f"Добро пожаловать, {username}! Теперь вы можете войти.")
                continue
            else:
                print("Продолжить без регистрации нельзя. Попробуйте снова.")
                continue

        password = input("Введите пароль: ").strip()

        cursor.execute("SELECT password FROM users where name = ?", (username,))

        real_password = [i[0] for i in cursor.fetchall()]
        print(real_password)

        if real_password[0] == password:
            cursor.execute("UPDATE users SET inset = 1 WHERE name = ?", (username,))
            conn.commit()
            print(f"Авторизация успешна! Добро пожаловать, {username}!")
            return True
        else:
            print("Ошибка: неверный пароль. Попробуйте снова.")




