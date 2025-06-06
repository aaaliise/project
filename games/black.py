import random
import sqlite3


def deal_card():
    """Возвращает случайную карту из колоды"""
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4 # 10 для J, Q, K
    return random.choice(cards)

def calculate_score(hand):
    """Подсчет очков с учётом туза"""
    score = sum(hand)
    while 11 in hand and score > 21:
        hand[hand.index(11)] = 1
        score = sum(hand)
    return score

def get_payout_multiplier(score):
    """Возвращает коэффициент выплаты на основе очков"""
    if score == 21:
        return 2.0
    elif score == 20:
        return 1.8
    elif score == 19:
        return 1.6
    elif score == 18:
        return 1.4
    elif score == 17:
        return 1.2
    else:
        return 1.0

def display_hand(name, hand):
    print(f"{name} карты: {hand} | Сумма: {calculate_score(hand)}") # можно ли добавить стикеры?????

def print_rules():
    print("🃏 Правила Блэкджека со ставками:")
    print("- Цель: набрать сумму ближе к 21, не превышая.")
    print("- Вы ставите фишки в начале каждого раунда.")
    print("- Чем ближе вы к 21 при победе — тем больше выигрыш:")
    print("  - 21: ×2.0 | 20: ×1.8 | 19: ×1.6 | 18: ×1.4 | 17: ×1.2 | ≤16: ×1.0")
    print("- При проигрыше — теряете ставку.")
    print("- Дилер берёт карты до 17 включительно.")
    print("- Побеждает тот, у кого сумма ближе к 21.\n")


def blackgak():
    conn = sqlite3.connect('db/project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT coins FROM users where inset = 1")
    balance = [i[0] for i in cursor.fetchall()][0]

    print("🎲 Добро пожаловать в Блэкджек со ставками!\n")
    print_rules()

    while balance > 0:
        print(f"\n💰 Ваш баланс: {balance} фишек")
        try:
            bet = int(input("Сделайте ставку: "))
            if bet <= 0 or bet > balance:
                print("❌ Неверная сумма ставки.")
                continue
        except ValueError:
            print("❌ Введите число.")
            continue

        player_hand = [deal_card(), deal_card()]
        dealer_hand = [deal_card(), deal_card()]
        game_over = False

        # Ход игрока
        while not game_over:
            display_hand("Игрок", player_hand)
            print(f"Карта дилера: [{dealer_hand[0]}, ?]")

            if calculate_score(player_hand) > 21:
                print("\n💥 Перебор! Вы проиграли. В следующий раз вам обязательно повезет больше!\n")
                balance -= bet
                game_over = True
                break

            action = input("Взять карту (в) или остановиться (с)? ").lower()
            if action == 'в':
                player_hand.append(deal_card())
            elif action == 'с':
                game_over = True
            else:
                print("❗️ Некорректный ввод.")

        if game_over and calculate_score(player_hand) <= 21:
            # Ход дилера
            while calculate_score(dealer_hand) < 17:
                dealer_hand.append(deal_card())

            print("\n🃑 Конечные руки:")
            display_hand("Игрок", player_hand)
            display_hand("Дилер", dealer_hand)

            player_score = calculate_score(player_hand)
            dealer_score = calculate_score(dealer_hand)

            if dealer_score > 21 or player_score > dealer_score:
                multiplier = get_payout_multiplier(player_score)
                winnings = int(bet * multiplier)
                print(f"\n🎉 Победа! Вы выиграли {winnings} фишек (×{multiplier})\n")
                balance += winnings
            elif player_score < dealer_score:
                print("\n😞 Вы проиграли. В следующий раз вам обязательно повезет больше!\n")
                balance -= bet
            else:
                print("\n🤝 Ничья. Ставка возвращена.\n")
        print("-" * 40)
        print(f"💰 Ваш баланс: {balance} фишек")
        cursor.execute("UPDATE users SET coins = ? WHERE inset = 1", (balance,))
        conn.commit()
        choice = input("Хотите сделать еще одну ставку? (y/n): ").lower()
        if choice != 'y':
            break

    if balance <= 0:
        print("\n💸 Увы, у вас закончились деньги. Игра окончена.\n")
