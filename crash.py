import random
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading


class CrashGame:
    def __init__(self):
        self.multiplier = 1.0
        self.crashed = False
        self.players = {}
        self.game_history = []
        self.current_round = 0
        self.round_start_time = time.time()
        self.round_duration = 0
        self.max_multiplier = 0

    def start_new_round(self):
        self.multiplier = 1.0
        self.crashed = False
        self.current_round += 1
        self.round_start_time = time.time()
        self.round_duration = 0
        self.max_multiplier = 0
        print(f"\n=== Начало раунда {self.current_round} ===")

    def run_round(self):
        self.start_new_round()

        # Генерируем точку краша (по алгоритму, используемому в реальных казино)
        crash_point = self.generate_crash_point()

        # Запускаем таймер раунда
        start_time = time.time()
        last_update = start_time

        while not self.crashed:
            current_time = time.time()
            elapsed = current_time - start_time
            self.round_duration = elapsed

            # Обновляем множитель (экспоненциальный рост с небольшими колебаниями)
            if elapsed < 1.0:
                # Медленный рост в первые секунды
                self.multiplier = 1.0 + (elapsed * 0.5)
            else:
                # Ускоряем рост со временем
                growth_rate = min(0.1 + (elapsed * 0.01), 0.5)
                self.multiplier = self.multiplier * (1.0 + growth_rate * (current_time - last_update))

            # Добавляем небольшие случайные колебания
            self.multiplier *= (1.0 + (random.random() * 0.02 - 0.01))

            self.max_multiplier = max(self.max_multiplier, self.multiplier)

            # Проверяем, не настал ли краш
            if self.multiplier >= crash_point:
                self.crashed = True
                self.multiplier = 0.0
                print(f"\n💥 КРАШ на множителе {crash_point:.2f}x! 💥")
                self.game_history.append({
                    'round': self.current_round,
                    'crash_point': crash_point,
                    'duration': elapsed
                })
                self.payout_players()
                break

            # Обновляем дисплей каждые 0.1 секунды
            if current_time - last_update >= 0.1:
                print(f"\rМножитель: {self.multiplier:.2f}x", end="", flush=True)
                last_update = current_time

            time.sleep(0.01)

        # Пауза перед новым раундом
        time.sleep(5)
        self.run_round()

    def generate_crash_point(self):
        # Алгоритм генерации точки краша (аналогичный используемому в реальных казино)
        e = 2 ** 32
        h = random.getrandbits(32)
        crash_point = (100 * e - h) / (e - h)
        crash_point = max(1.0, crash_point / 100)
        return crash_point

    def add_player(self, player_id, bet_amount):
        if player_id not in self.players:
            self.players[player_id] = {
                'bet': bet_amount,
                'cashed_out': False,
                'cashout_multiplier': 0.0
            }
            print(f"Игрок {player_id} сделал ставку: ${bet_amount:.2f}")

    def cash_out(self, player_id):
        if player_id in self.players and not self.players[player_id]['cashed_out']:
            self.players[player_id]['cashed_out'] = True
            self.players[player_id]['cashout_multiplier'] = self.multiplier
            print(f"Игрок {player_id} забрал выигрыш на множителе {self.multiplier:.2f}x")

    def payout_players(self):
        for player_id, data in self.players.items():
            if data['cashed_out']:
                win_amount = data['bet'] * data['cashout_multiplier']
                print(
                    f"Игрок {player_id} выиграл ${win_amount:.2f} (ставка: ${data['bet']:.2f}, множитель: {data['cashout_multiplier']:.2f}x)")
            else:
                print(f"Игрок {player_id} проиграл ставку ${data['bet']:.2f}")
        self.players = {}


# Пример использования
if __name__ == "__main__":
    game = CrashGame()

    # Запускаем игру в отдельном потоке
    game_thread = threading.Thread(target=game.run_round)
    game_thread.daemon = True
    game_thread.start()

    # Симуляция игроков (в реальной игре это бы делалось через интерфейс)
    time.sleep(1)
    game.add_player("Player1", 10.0)
    game.add_player("Player2", 5.0)

    # Игрок 1 забирает выигрыш через 2 секунды
    time.sleep(2)
    game.cash_out("Player1")

    # Игрок 2 не успевает забрать и проигрывает при краше