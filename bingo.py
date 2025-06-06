import random
from collections import defaultdict


class BingoGame:
    def __init__(self, num_players=1):
        self.players = [BingoPlayer() for _ in range(num_players)]
        self.drawn_numbers = []
        self.remaining_numbers = list(range(1, 76))
        random.shuffle(self.remaining_numbers)
        self.winners = []

    def draw_number(self):
        if not self.remaining_numbers:
            return None
        number = self.remaining_numbers.pop()
        self.drawn_numbers.append(number)
        return number

    def check_winners(self):
        if self.winners:
            return self.winners

        for i, player in enumerate(self.players):
            if player.has_won(self.drawn_numbers):
                self.winners.append(i)
        return self.winners

    def play(self):
        print("=== НАЧАЛО ИГРЫ В БИНГО ===")
        for i, player in enumerate(self.players, 1):
            print(f"\nКарточка игрока {i}:")
            player.print_card()

        while self.remaining_numbers and not self.winners:
            input("\nНажмите Enter, чтобы вытянуть следующее число...")
            number = self.draw_number()
            print(f"\nВыпало число: {number}")

            for i, player in enumerate(self.players, 1):
                if player.mark_number(number):
                    print(f"Игрок {i} отметил число {number} на карточке")

            winners = self.check_winners()
            if winners:
                print("\n=== БИНГО! ===")
                for winner in winners:
                    print(f"Игрок {winner + 1} выиграл!")
                return

        print("\nВсе числа вытянуты, игра окончена!")
        if not self.winners:
            print("Никто не выиграл.")


class BingoPlayer:
    def __init__(self):
        self.card = self.generate_card()
        self.marked_numbers = set()

    def generate_card(self):
        card = defaultdict(list)
        ranges = {
            'B': (1, 15),
            'I': (16, 30),
            'N': (31, 45),
            'G': (46, 60),
            'O': (61, 75)
        }

        for letter, (start, end) in ranges.items():
            card[letter] = random.sample(range(start, end + 1), 5)

        # Центральная клетка - свободная
        card['N'][2] = 'FREE'
        return card

    def print_card(self):
        print(" B   I   N   G   O")
        print("------------------")
        for row in range(5):
            line = []
            for letter in ['B', 'I', 'N', 'G', 'O']:
                num = self.card[letter][row]
                if num in self.marked_numbers:
                    line.append(" X ")
                elif num == 'FREE':
                    line.append("FREE")
                else:
                    line.append(f"{num:3}")
            print(" ".join(line))

    def mark_number(self, number):
        for letter in self.card:
            if number in self.card[letter]:
                self.marked_numbers.add(number)
                return True
        return False

    def has_won(self, drawn_numbers):
        # Проверяем строки
        for row in range(5):
            row_complete = True
            for letter in ['B', 'I', 'N', 'G', 'O']:
                num = self.card[letter][row]
                if num != 'FREE' and num not in drawn_numbers:
                    row_complete = False
                    break
            if row_complete:
                return True

        # Проверяем столбцы
        for letter in self.card:
            col_complete = True
            for num in self.card[letter]:
                if num != 'FREE' and num not in drawn_numbers:
                    col_complete = False
                    break
            if col_complete:
                return True

        # Проверяем диагонали
        diag1 = all(
            self.card[letter][i] == 'FREE' or
            self.card[letter][i] in drawn_numbers
            for i, letter in enumerate(['B', 'I', 'N', 'G', 'O'])
        )

        diag2 = all(
            self.card[letter][4 - i] == 'FREE' or
            self.card[letter][4 - i] in drawn_numbers
            for i, letter in enumerate(['B', 'I', 'N', 'G', 'O'])
        )

        return diag1 or diag2


# Запуск игры
print("Добро пожаловать в игру Бинго!")
num_players = int(input("Введите количество игроков: "))
game = BingoGame(num_players)
game.play()