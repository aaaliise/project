import random
import sqlite3


class TowerGame:
    def __init__(self):
        conn = sqlite3.connect('db/project.db')
        cursor = conn.cursor()
        cursor.execute("SELECT coins FROM users where inset = 1")
        self.balance = [i[0] for i in cursor.fetchall()][0]
        self.current_floor = 0  # Текущий этаж
        self.bet_amount = 0  # Текущая ставка
        self.multiplier = 1.0  # Множитель выигрыша
        self.game_active = False  # Идет ли игра
        self.floor_options = ['A', 'B', 'C', 'D']  # Варианты дверей


    def display_header(self):
        """Выводит заголовок игры"""
        print("=== ИГРА 'БАШНЯ' ===")
        print(f"\n💰 Ваш баланс: {self.balance} фишек")
        if self.game_active:
            print(f"Текущий этаж: {self.current_floor}")
            print(f"Множитель выигрыша: {self.multiplier:.1f}x")
        print("======================")

    def display_rules(self):
        """Показывает правила игры"""
        print("=== ПРАВИЛА ИГРЫ 'БАШНЯ' ===")
        print("1. Вы делаете ставку.")
        print("2. На каждом этаже вы выбираете дверь (A, B, C или D).")
        print("3. Если угадываете — поднимаетесь выше, множитель растёт.")
        print("4. Можно забрать выигрыш в любой момент (команда 'Q').")
        print("5. Если ошибаетесь — теряете ставку.")
        print("6. Максимум можно подняться до 5 этажа (множитель x3.5).")
        print("\nЧем выше этаж — тем больше выигрыш, но и риск выше!")
        input("\nНажмите Enter, чтобы вернуться...")

    def place_bet(self):
        """Размещение ставки"""
        while True:
            try:
                bet = float(input(f"Сделайте ставку: "))
                if bet <= 0:
                    print("Минимальная ставка — 1!")
                elif bet > self.balance:
                    print("У вас недостаточно средств!")
                else:
                    self.bet_amount = bet
                    self.balance -= bet # &&&
                    self.game_active = True
                    self.current_floor = 0
                    self.multiplier = 1.0
                    break
            except ValueError:
                print("Ошибка! Введите число.")

    def play_floor(self):
        """Игровой процесс (выбор дверей)"""
        correct_option = random.choice(self.floor_options)

        while True:
            self.display_header()
            print(f"\nЭтаж {self.current_floor + 1}")
            print("Выберите дверь, чтобы подняться выше:")
            print("A    B    C    D")

            guess = input("Ваш выбор (A/B/C/D) или 'Q' чтобы забрать деньги: ").upper()

            if guess == 'Q':
                self.cash_out()
                return

            if guess not in self.floor_options:
                print("Ошибка! Выберите A, B, C или D.")
                continue

            if guess == correct_option:
                # Правильный выбор — переход на следующий этаж
                self.current_floor += 1
                self.multiplier = 1.0 + (self.current_floor * 0.5)
                correct_option = random.choice(self.floor_options)

                self.display_header()
                print("\nВерно! Поднимаемся выше...")

                # Проверка, дошел ли игрок до вершины (5 этаж)
                if self.current_floor >= 5:
                    print("\nПоздравляем! Вы достигли вершины башни!")
                    self.cash_out()
                    return
            else:
                # Неправильный выбор — проигрыш
                self.display_header()
                print(f"\nНеверно! Правильная дверь — {correct_option}.")
                print("Вы проиграли ставку!")
                self.game_active = False
                self.bet_amount = 0
                return

    def cash_out(self):
        """Забрать деньги (завершить игру)"""
        if not self.game_active:
            return

        winnings = self.bet_amount * self.multiplier
        self.balance += winnings
        self.display_header()
        print(f"\nВы забрали деньги на этаже {self.current_floor + 1}!")
        print(f"Ваш выигрыш: {winnings:.2f} (множитель: {self.multiplier:.1f}x)")
        self.game_active = False
        self.bet_amount = 0

    def main_loop(self):
        """Главный игровой цикл"""
        while True:
            self.display_header()

            if self.balance <= 0:
                print("\n💸 Увы, у вас закончились деньги. Игра окончена.\n")
                break

            print("\n1. Играть в 'Башню'")
            print("2. Правила игры")
            print("3. Выйти")

            choice = input("Выберите действие: ")

            if choice == '1':
                self.place_bet()
                self.play_floor()
            elif choice == '2':
                self.display_rules()
            elif choice == '3':
                print("\nСпасибо за игру! До свидания!")
                conn = sqlite3.connect('db/project.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET coins = ? WHERE inset = 1", (self.balance,))
                conn.commit()
                break
            else:
                print("Неверный выбор. Попробуйте снова.")


