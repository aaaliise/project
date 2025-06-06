import random
import sqlite3


def spin_slots(symbols):
    return [random.choice(symbols) for _ in range(3)]


def evaluate_spin(spin):
    if spin.count(spin[0]) == 3:
        return "jackpot"
    elif spin.count(spin[0]) == 2 or spin.count(spin[1]) == 2:
        return "two_match"
    else:
        return "no_match"


def confirm_consent():
    print("=" * 50)
    print("🎰 ПРАВИЛА ИГРЫ В СЛОТЫ")
    print("=" * 50)
    print("""
1. Игра использует 8 случайных символов: 🍒, 🍋, 🔔, ⭐, 🍀, 💎, 7️⃣, 👑.
2. В каждом спине выпадает 3 символа.

🎉 Выигрышные комбинации:
 - 3 одинаковых символа → Джекпот (ставка x50)
 - 2 одинаковых символа → Вторая попытка:
     - 3 одинаковых → Джекпот (x50)
     - 2 одинаковых → Ставка x5
     - 0 совпадений → Проигрыш
     - Выход → x2

🙁 0 совпадений с первой попытки → Проигрыш
""")
    print("=" * 50)

    consent = input("Вы ознакомились с правилами и хотите начать игру? (y/n): ").strip().lower()
    if consent in ["да", "yes", "y"]:
        print("✅ Подтверждено. Приступаем к игре!")
        return True
    else:
        print("🚫 Игра отменена. Возвращайтесь позже!")
        return False


def play_slots():
    conn = sqlite3.connect('db/project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT coins FROM users where inset = 1")
    balance = [i[0] for i in cursor.fetchall()][0]

    print("🎲 Добро пожаловать в Рулетка со ставками!\n")

    n = confirm_consent()
    print(f"\n💰 Ваш баланс: {balance} фишек")

    symbols = ['🍒', '🍋', '🔔', '⭐', '🍀', '💎', '7️⃣', '👑']

    while balance > 0 and n:
        try:
            bet = int(input("Сделайте ставку: "))
            if bet <= 0 or bet > balance:
                print("❌ Неверная сумма ставки.")
                continue
        except ValueError:
            print("❌ Введите число.")
            continue

        print("\n🎰 Первая попытка:")
        spin = spin_slots(symbols)
        print(" | ".join(spin))
        result = evaluate_spin(spin)

        if result == "jackpot":
            print("🎉 Джекпот! Все символы совпали!")
            balance += bet * 50

        elif result == "two_match":
            re = input('Хочешь выйти со ставкой x2 или продолжить со ставкой x5. Напиши (y/n) ')
            if re != 'y':
                print("🔄 Повторная попытка! Выпало 2 одинаковых символа.")
                print("\n🎰 Вторая попытка:")
                spin2 = spin_slots(symbols)
                print(" | ".join(spin2))
                result2 = evaluate_spin(spin2)

                if result2 == "jackpot":
                    print("🎉 Джекпот во второй попытке! Все символы совпали!")
                    balance += bet * 50
                elif result2 == "two_match":
                    print("🙂 Снова 2 одинаковых. Ставка возвращается с коэффициентом 5.")
                    balance += bet * 5
                else:
                    print("🙁 Повтор не принес удачи. Вы проиграли.")
                    balance -= bet
            else:
                print("🙂 Ставка возвращается с коэффициентом 2.")
                balance += bet * 2
        else:
            print("🙁 Не повезло. Нет совпадений.")
            balance -= bet
        print(f"\n💰 Ваш баланс: {balance} фишек")
        cursor.execute("UPDATE users SET coins = ? WHERE inset = 1", (balance,))
        conn.commit()
        choice = input("Хотите сделать еще одну ставку? (y/n): ").lower()
        if choice != 'y':
            break
    if balance <= 0:
        print("\n💸 Увы, у вас закончились деньги. Игра окончена.\n")
