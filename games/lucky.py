import random
import sqlite3
import time


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
        print("5 - Крэпс выплата 1:1")
        print("6 - Выйти")

        choice = input("Выберите режим (1–6): ")
        if choice == '6':
            print("Спасибо за игру!")
            break

        bet = int(input("Введите ставку в фишках: "))
        if bet > balance or bet <= 0:
            print("Недопустимая ставка.")
            continue

        if choice == '5':
            balance += craps(bet)
            print("-" * 40)
            print(f"💰 Ваш баланс: {balance} фишек")
            cursor.execute("UPDATE users SET coins = ? WHERE inset = 1", (balance,))
            conn.commit()
            choice = input("Хотите сделать еще одну ставку? (y/n): ").lower()
            if choice != 'y':
                break
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



        time.sleep(1)
        print("\nБросаем кости...")
        time.sleep(2)
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


def throw_dice():
    d1, d2 = roll_dice()
    total = d1 + d2
    print(f"🎲 Выпало: {d1} и {d2} (сумма: {total})")
    return d1, d2, total


def craps(bet):
    print("\n=== 🎲 Добро пожаловать в Крэпс! ===")
    print(f"Ставка: {bet} фишек")
    print("\nВыберите тип ставки:")
    print("1. Pass Line (1:1)")
    print("2. Don't Pass (1:1, 12 - возврат)")
    print("3. Field (2:1 для 2, 3:1 для 12, 1:1 для 3,4,9,10,11)")
    print("4. Any Seven (4:1)")
    print("5. Any Craps (7:1)")
    print("6. Hard Ways (дубль) (8:1)")

    bet_type = input("> ")

    # Pass Line (ставка на проход)
    if bet_type == '1':
        print("\n=== Ставка: Pass Line (1:1) ===")
        print("Первый бросок (Come-Out Roll)...")
        time.sleep(3)
        d1, d2, total = throw_dice()

        if total in (7, 11):
            print("✅ Выигрыш! (7 или 11)")
            return bet * 1
        elif total in (2, 3, 12):
            print("❌ Проигрыш! (Craps)")
            return -bet
        else:
            point = total
            print(f"🔄 Установлена точка: {point}. Бросаем снова...")
            while True:
                time.sleep(1)
                d1, d2, total = throw_dice()

                if total == 7:
                    print("❌ Проигрыш! Выпало 7")
                    return -bet
                elif total == point:
                    print(f"✅ Выигрыш! Выпала точка {point}")
                    return bet * 1
                else:
                    print(f"🔄 Выпало {total}. Продолжаем...")

    # Don't Pass (ставка против прохода)
    elif bet_type == '2':
        print("\n=== Ставка: Don't Pass (1:1, 12 - возврат) ===")
        print("Первый бросок (Come-Out Roll)...")
        time.sleep(3)
        d1, d2, total = throw_dice()

        if total in (2, 3):
            print("✅ Выигрыш! (2 или 3)")
            return bet * 1
        elif total in (7, 11):
            print("❌ Проигрыш! (7 или 11)")
            return -bet
        elif total == 12:
            print("➖ Ничья! (12) - ставка возвращается")
            return 0
        else:
            point = total
            print(f"🔄 Установлена точка: {point}. Бросаем снова...")
            while True:
                time.sleep(1)
                d1, d2, total = throw_dice()

                if total == 7:
                    print("✅ Выигрыш! Выпало 7")
                    return bet * 1
                elif total == point:
                    print("❌ Проигрыш! Выпала точка")
                    return -bet
                else:
                    print(f"🔄 Выпало {total}. Продолжаем...")

    # Field (ставка на поле)
    elif bet_type == '3':
        print("\n=== Ставка: Field ===")
        print("Бросаем кости...")
        time.sleep(3)
        d1, d2, total = throw_dice()

        if total in (2, 3, 4, 9, 10, 11, 12):
            if total == 2:
                print("🎉 Супер выигрыш! 2 (3:1)")
                return bet * 3
            elif total == 12:
                print("🎉 Супер выигрыш! 12 (2:1)")
                return bet * 2
            else:
                print(f"✅ Выигрыш! {total} (1:1)")
                return bet * 1
        else:
            print("❌ Проигрыш!")
            return -bet

    # Any Seven (любая семерка)
    elif bet_type == '4':
        print("\n=== Ставка: Any Seven (4:1) ===")
        print("Бросаем кости...")
        time.sleep(3)
        d1, d2, total = throw_dice()

        if total == 7:
            print("🎉 Выигрыш! Выпало 7")
            return bet * 4
        else:
            print("❌ Проигрыш!")
            return -bet

    # Any Craps (любой крэпс)
    elif bet_type == '5':
        print("\n=== Ставка: Any Craps (7:1) ===")
        print("Бросаем кости...")
        time.sleep(3)
        d1, d2, total = throw_dice()

        if total in (2, 3, 12):
            print(f"🎉 Выигрыш! Craps ({total})")
            return bet * 7
        else:
            print("❌ Проигрыш!")
            return -bet

    # Hard Ways (дубль)
    elif bet_type == '6':
        print("\n=== Ставка: Hard Ways (8:1) ===")
        print("Бросаем кости...")
        time.sleep(3)
        d1, d2, total = throw_dice()

        if d1 == d2:
            print(f"🎉 Выигрыш! Дубль {d1}-{d2}")
            return bet * 8
        else:
            print("❌ Проигрыш! Не дубль")
            return -bet

    else:
        print("⚠️ Неверный выбор. Ставка возвращается.")
        return 0