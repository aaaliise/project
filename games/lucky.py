import random
import sqlite3


def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)


def luck():
    conn = sqlite3.connect('db/project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT coins FROM users where inset = 1")
    balance = [i[0] for i in cursor.fetchall()][0]

    print("🎲 Добро пожаловать в 'Lucky Dice'!")
    print(f"Казино выигрывает при 7.")

    while balance > 0:
        print(f"\n💰 Ваш баланс: {balance} фишек")
        print("Варианты ставок:")
        print("1 - Точное значение (2–12), выплата 8:1")
        print("2 - Чет / Нечет (выплата 1.5:1, 7 — проигрыш)")
        print("3 - Больше 7 / Меньше 7 (1.5:1, 7 — проигрыш)")
        print("4 - Двойняшки (дубль), выплата 10:1")
        print("5 - Выйти")

        choice = input("Выберите режим (1–5): ")
        if choice == '5':
            print("Спасибо за игру!")
            break

        bet = int(input("Введите ставку в фишках: "))
        if bet > balance or bet <= 0:
            print("Недопустимая ставка.")
            continue

        dice = roll_dice()
        total = sum(dice)


        win = False
        payout = 0

        if total == 7:
            print("Казино выигрывает при 7. Вы проиграли.")
            balance -= bet
            continue

        if choice == '1':
            target = int(input("На какое точное число ставите (2–12)? "))
            if total == target:
                payout = bet * 8
                win = True
        elif choice == '2':
            parity = input("Ставите на чет или нечет? (ч/н): ").lower()
            if (total % 2 == 0 and parity == 'ч') or (total % 2 == 1 and parity == 'н'):
                payout = int(bet * 1.5)
                win = True
        elif choice == '3':
            direction = input("Ставите на больше 7 (б) или меньше 7 (м)? ").lower()
            if (total < 7 and direction == 'м') or (total > 7 and direction == 'б'):
                payout = int(bet * 1.5)
                win = True
        elif choice == '4':
            if dice[0] == dice[1]:
                if dice[0] == 1:
                    print("🐍 Выпали змеиные глаза (1-1). Теряете двойную ставку!")
                    balance -= bet * 2
                    continue
                payout = bet * 10
                win = True

        print(f"🎲 Выпали кости: {dice[0]} и {dice[1]} (сумма: {total})")

        if win:
            print(f"🎉 Вы выиграли {payout} фишек!")
            balance += payout
        else:
            print("😞 Вы проиграли. В следующий раз вам обязательно повезет больше!")
            balance -= bet
        print("-" * 40)
        print(f"💰 Ваш баланс: {balance} фишек")
        cursor.execute("UPDATE users SET coins = ? WHERE inset = 1", (balance,))
        conn.commit()
        choice = input("Хотите сделать еще одну ставку? (y/n): ").lower()
        if choice != 'y':
            break

    if balance <= 0:
        print("\n💸 Увы, у вас закончились деньги. Игра окончена.\n")

