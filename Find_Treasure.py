import random
import os


class TreasureMap:
    # Инициализация координат сокровища
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    # Метод для генерации коорадинат сокровища в пределах поля 10*10
    # Возращает координаты X и Y целочыми числами от 0 до 9
    def generate_treasure(self):
        self.x = random.randint(0, 9)
        self.y = random.randint(0, 9)
        return self.x, self.y

    # Метод создает несколько сокровищ с помощью generate_treasure() и возвращает список treasures, состоящий из
    # координат сокровищ (X, Y).
    @staticmethod
    def multiple_treasures(number):
        treasures = []
        for i in range(number):
            new = TreasureMap().generate_treasure()
            if new in treasures:
                pass
            else:
                treasures.append(TreasureMap().generate_treasure())
        return treasures

    # Метод для проверки координат сокровища с введеными. Возвращает True, при совпадении и False, если - нет.
    def treasure_check(self, player_x, player_y):
        if self.x == player_x and self.y == player_y:
            return True
        else:
            return False

    # Метод возращает True если координаты игрока находятся в зоне сокровища 3*3, где центер - это соровище
    # Возращает False в противном случае
    def get_hint(self, player_x, player_y):
        if (((abs(self.x - player_x) == 1 and abs(self.y - player_y) == 1)
             or (abs(self.x - player_x) == 1 and abs(self.y - player_y) == 0)) or
                (abs(self.x - player_x) == 0 and abs(self.y - player_y) == 1)):
            return True
        else:
            return False


class Player:
    # Инициализация координат и переменной, хронящией колличество попыток
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
        self.trys = 0

    # Метод возвращает введенные координаты пользователя. Поднимает ошибку, если пользователь ввел не цифры от 0 до 9.
    def choose_position(self):
        while True:
            self.x = int(input(f"Введите X кординату числом от 0 до 9: "))
            self.y = int(input(f"Введите Y кординату числом от 0 до 9: "))
            if 0 <= self.x <= 9 and 0 <= self.y <= 9:
                return self.x, self.y
            else:
                raise ValueError


# Функция выводит сообщение в консоль связанное с определенным событием.
def notice(message, trys=None, hint=None, quantety=None):
    if message == "start":
        return (
            f"Добро пожаловать в игру «Поиск сокровища»! На игровом поле размером 10x10 спрятано {quantety} сокровище."
            f"\nВаша задача — найти его за минимальное количество попыток. Координаты вводятся в формате «x, y»,"
            f"\nгде x — горизонтальная координата, y — вертикальная координата. Удачи!\n")
    elif message == "found":
        return "Поздравляем! Вы нашли сокровище."
    elif message == "win":
        return f"Поздравляем! Игра завершена. Сокровище найдено. Попыток: [{trys}]. Ваш промокод SUPER100"
    elif message == "lose":
        return "Количество попыток исчерпано. Сокровище не найдено."
    elif message == "founded_treasure":
        return "Здесь уже было найдено сокровище. Ты только что потратил поптытку :V"
    elif message == "hint":
        if hint:
            return f"Вы близко к сокровищу!"
        elif quantety is not None:
            return f'Осталось {quantety} сокровищ.\nОсталось {9 - trys} из 10.'
        else:
            return f"Сокровище где-то в другом месте..."
    else:
        raise NotImplementedError("Непредсказуемая переменная для notice()!")


# Функция выводит в консоль игровое поле в виде сетки 10*10 и возвращает массив из строк grid.
# Так же функуия принимает переменную grid для внесения изменений и вывода обновленного поля в связи с новыми вводными.
def game_field(grid=None, check=None, treasure=None, player=None):
    # index используется для подсчета рядов, чтобы сравнить ряд выбранный игроком и ряд, идущий в цикле для изменения
    # элемента.
    # ANSI_RED, ANSI_BLUE и ANSI_RESET переменные необходимые для окраски элементов на поле.
    index = 0

    ANSI_RESET = "\033[0m"
    ANSI_GREEN = "\033[32m"
    ANSI_RED = "\033[31m"

    if grid is None or len(grid) == 0:
        grid = [['[0]'.rjust(3)] * 10 for _ in range(10)]
        return grid
    for row in grid:
        if index == player[1] and check is not True:
            tmp = f"{ANSI_RED}X{ANSI_RESET}"
            row[player[0]] = f'[{tmp}]'
        elif index == treasure[1] and check is True:
            tmp = f"{ANSI_GREEN}V{ANSI_RESET}"
            row[treasure[0]] = f'[{tmp}]'
        index += 1
    return grid


class Game(TreasureMap, Player):
    game_initialized = 0

    def __init__(self, x=None, y=None):
        super().__init__(x, y)
        self.treasure = TreasureMap
        self.player = Player

    @staticmethod
    def multiple_hints(treasures, player):
        for treasure in treasures:
            tmp = TreasureMap(treasure[0], treasure[1])
            print(notice("hint", hint=tmp.get_hint(player[0], player[1])))

    # Метод создает, записывет или дозаписывает ходы игрока в файл log.txt.
    @staticmethod
    def get_log(player_info=None, game_initialized=None):
        try:
            if os.path.isfile('./log.txt') is False and game_initialized == 0:
                with open("log.txt", "a") as fw:
                    fw.write(f"{player_info[0], player_info[1]}\n")
                    Game.game_initialized = 1
            elif os.path.isfile('./log.txt') is True and game_initialized == 0:
                with open("log.txt", "w") as fw:
                    fw.write(f"{player_info[0], player_info[1]}\n")
                    Game.game_initialized = 1
            elif os.path.isfile('./log.txt') is True and game_initialized == 1:
                with open("log.txt", "a") as fw:
                    fw.write(f"{player_info[0], player_info[1]}\n")
        except TypeError as p:
            print(p)

    # Метод инициализирует игру и собирает все объекты и вместе.
    def start_game(self):
        # Создание объектов игрока и сокровища
        treasure = TreasureMap()
        player = Player()
        succsesful_guesses = []

        # Создание нексольких сокровищ. Создается список с кординатами (Х, У)
        generated_treasure = self.treasure.multiple_treasures(number=2)

        # Вывод сообщения о старте игры, вывод игрового поля в консоль и начало игрового цикла.
        print(notice("start", quantety=len(generated_treasure)))
        game_grid = game_field()
        for row in list(reversed(game_grid)):
            print(*row)

        while True:

            # Ввод координат игрока, записть их в log.txt и проверка совпадания координат игрока и сокровища
            try:
                print("Введите координаты, чтобы проверить, содержится ли сокровище в этой клетке.")
                player_coordinats = tuple(player.choose_position())
            except ValueError or TypeError:
                print("Ошибка! Введите координаты целыми числами от 0 до 9. Например: X:3 и Y:8.\n")
                continue

            Game.get_log(player_coordinats, Game.game_initialized)
            check = player_coordinats in generated_treasure

            if check is True:
                # Нахождение сокровища: создание нового игрового поля с отмеченным найдемнным сокровищем
                # Вывод оповищения о нахождении сокровища
                # Добавления координат успешной попытки для сохрания изменений на игровом поле
                # Удаления координат сокровища из спикска generated_treasure
                # Оповещение игрока о близости с сокровищем
                game_grid = game_field(game_grid, bool(check), player_coordinats, player_coordinats)
                for row in list(reversed(game_grid)):
                    print(*row)
                print(notice("found"))
                succsesful_guesses.append(player_coordinats)
                generated_treasure.remove(player_coordinats)
                Game.multiple_hints(generated_treasure, player_coordinats)
                if len(generated_treasure) == 0:
                    # Конец игры: вывод оповещения о нахождении всех сокровищь и последующие окончание цикла
                    print(notice("win", trys=player.trys))
                    break
            elif player.trys > 9:
                # Конец игры: вывод оповещения о истощении попыток и последующие окончание цикла
                print(notice("lose"))
                break
            else:
                # Вывод сообщения подсказки о близости нахождения сокровища
                # Уыеличения счетчика попыток
                # Обнавление поля с добавлением выбранных координат неудачной попытки игрока
                if player_coordinats in succsesful_guesses:
                    print(notice("founded_treasure"))
                else:
                    Game.multiple_hints(generated_treasure, player_coordinats)
                    print(notice("hint",trys=player.trys, quantety=len(generated_treasure)))
                    game_grid = game_field(game_grid, check, player_coordinats, player_coordinats)
                    for row in list(reversed(game_grid)):
                        print(*row)
                player.trys += 1


if __name__ == "__main__":
    game = Game()
    Game.start_game(game)
