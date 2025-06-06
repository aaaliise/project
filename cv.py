import random
import time
import threading

class CrashGame:
    def __init__(self):
        self.crashed = False
        self.multiplier = 1.0
        self.cashout = False
        self.lock = threading.Lock()
        self.thread = None

    def simulate_crash_point(self):
        return round(random.expovariate(1/2) + 1, 2)

    def grow_multiplier(self):
        while not self.crashed and not self.cashout:
            time.sleep(0.2)
            with self.lock:
                self.multiplier = round(self.multiplier + 0.1 + self.multiplier * 0.01, 2)
                print(f"📈 Коэффициент: {self.multiplier}x")
                time.sleep(1)
                if self.multiplier >= self.crash_point:
                    self.crashed = True
                    print(f"💥 КРАШ на {self.multiplier}x! Вы проиграли {self.bet_amount} монет.")


    def start_game(self, bet_amount):
        self.bet_amount = bet_amount
        self.crash_point = self.simulate_crash_point()
        self.crashed = False
        self.cashout = False
        self.multiplier = 1.0

        print(f"🎮 Игра началась! Возможный краш: {self.crash_point}x")
        self.thread = threading.Thread(target=grow_multiplier(self))
        self.thread.start()





    def try_cashout(self, bet_amount):
        with self.lock:
            if self.crashed:
                print("❌ Слишком поздно! Игра уже завершилась.")
                return 0
            elif self.cashout:
                print("⚠️ Вы уже вывели.")
                return 0
            else:
                self.cashout = True
                winnings = round(bet_amount * self.multiplier, 2)
                print(f"✅ Вы вывели на {self.multiplier}x! Выигрыш: {winnings} монет.")
                return winnings


# --- Главный цикл ---
if __name__ == "__main__":
    game = CrashGame()
    try:
        bet = float(input("💰 Введите ставку: "))
    except ValueError:
        print("❗ Ошибка: нужно ввести число.")
        exit(1)

    game.start_game(bet)

    while True:
        action = input("✋ Введите 'вывести' для остановки, или Enter для продолжения: ").strip().lower()
        if action == "вывести":
            winnings = game.try_cashout(bet)
            break
        if game.crashed:
            break

    # Дождаться завершения потока (гарантированно выводится финал)
    game.thread.join()