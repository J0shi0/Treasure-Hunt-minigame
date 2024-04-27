from Find_Treasure import *
import unittest.mock
from io import StringIO
from unittest.mock import patch


class TestTreasureMap(unittest.TestCase):
    def setUp(self):
        print("\nRunning setUp method...")
        self.treasure_1 = TreasureMap()
        self.treasure_2 = TreasureMap(5, 5)

    def tearDown(self):
        print("Running tearDown method...")

    def test_generate_treasure_returns_tuple(self):
        result = self.treasure_1.generate_treasure()
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert all(0 <= coord <= 9 for coord in result)

    def test_multiple_treasures_returns_empty_list(self):
        result = self.treasure_1.multiple_treasures(0)
        assert isinstance(result, list)
        assert len(result) == 0

    def test_returns_list_of_length_number_when_number_is_greater_than_0(self):
        result = self.treasure_1.multiple_treasures(5)
        assert isinstance(result, list)
        assert len(result) == 5

    def test_returns_true_when_coordinates_match(self):
        player_x = 5
        player_y = 5

        # Act
        result = self.treasure_2.treasure_check(player_x, player_y)

        # Assert
        assert result is True

    def test_returns_false_when_coordinates_are_none(self):
        player_x = None
        player_y = 5

        # Act
        result = self.treasure_2.treasure_check(player_x, player_y)

        # Assert
        assert result is False

    def test_returns_false_when_coordinates_are_not_integers(self):
        player_x = "5"
        player_y = 5.5

        # Act
        result = self.treasure_2.treasure_check(player_x, player_y)

        # Assert
        assert result is False

    def test_returns_true_if_player_is_adjacent_to_treasure(self):
        assert self.treasure_2.get_hint(4, 4) is True
        assert self.treasure_2.get_hint(4, 5) is True
        assert self.treasure_2.get_hint(4, 6) is True
        assert self.treasure_2.get_hint(5, 4) is True
        assert self.treasure_2.get_hint(5, 6) is True
        assert self.treasure_2.get_hint(6, 4) is True
        assert self.treasure_2.get_hint(6, 5) is True
        assert self.treasure_2.get_hint(6, 6) is True

    def test_returns_false_if_player_is_on_same_coordinates_as_treasure(self):
        assert self.treasure_2.get_hint(5, 5) is False

    def test_returns_false_if_player_is_more_than_one_square_away_from_treasure(self):
        assert self.treasure_2.get_hint(3, 3) is False
        assert self.treasure_2.get_hint(3, 5) is False
        assert self.treasure_2.get_hint(3, 7) is False
        assert self.treasure_2.get_hint(5, 3) is False
        assert self.treasure_2.get_hint(5, 7) is False
        assert self.treasure_2.get_hint(7, 3) is False
        assert self.treasure_2.get_hint(7, 5) is False
        assert self.treasure_2.get_hint(7, 7) is False


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player()

    def test_choose_position_valid_input(self):
        expected_x = 3
        expected_y = 8

        # Mock user input using patch
        with unittest.mock.patch('builtins.input', side_effect=["3", "8"]):
            x, y = self.player.choose_position()

        self.assertEqual(x, expected_x)
        self.assertEqual(y, expected_y)

    def test_choose_position_invalid_input_not_number(self):
        # Mock user input with non-numeric values
        with unittest.mock.patch('builtins.input', side_effect=["abc", "def"]):
            with self.assertRaises(ValueError):
                self.player.choose_position()

    def test_choose_position_invalid_input_x_too_small(self):
        with unittest.mock.patch('builtins.input', side_effect=["-1", "1"]):
            with self.assertRaises(ValueError):
                self.player.choose_position()

    def test_choose_position_invalid_input_x_too_large(self):
        with unittest.mock.patch('builtins.input', side_effect=["10", "5"]):
            with self.assertRaises(ValueError):
                self.player.choose_position()

    def test_choose_position_invalid_input_y_too_small(self):
        with unittest.mock.patch('builtins.input', side_effect=["3", "-1"]):
            with self.assertRaises(ValueError):
                self.player.choose_position()

    def test_choose_position_invalid_input_y_too_large(self):
        with unittest.mock.patch('builtins.input', side_effect=["3", "10"]):
            with self.assertRaises(ValueError):
                self.player.choose_position()


class TestNotice(unittest.TestCase):

    #  returns a welcome message when message is "start"
    def test_welcome_message(self):
        result = notice("start", quantety=5)
        expected = ("Добро пожаловать в игру «Поиск сокровища»! На игровом поле размером 10x10 спрятано 5 сокровище.\n"
                    "Ваша задача — найти его за минимальное количество попыток. Координаты вводятся в формате «x, y»,"
                    "\nгде x — горизонтальная координата, y — вертикальная координата. Удачи!\n")
        assert result == expected

    #  returns a congratulatory message when message is "found"
    def test_congratulatory_message_found(self):
        result = notice("found")
        expected = "Поздравляем! Вы нашли сокровище."
        assert result == expected

    #  returns a congratulatory message with number of tries when message is "win"
    def test_congratulatory_message_win(self):
        result = notice("win", trys=8)
        expected = "Поздравляем! Игра завершена. Сокровище найдено. Попыток: [8]. Ваш промокод SUPER100"
        assert result == expected

    #  returns a failure message when message is "lose"
    def test_failure_message_lose(self):
        result = notice("lose")
        expected = "Количество попыток исчерпано. Сокровище не найдено."
        assert result == expected

    #  returns a message indicating that the treasure has already been found when message is "founded_treasure"
    def test_message_treasure_found(self):
        result = notice("founded_treasure")
        expected = "Здесь уже было найдено сокровище. Ты только что потратил поптытку :V"
        assert result == expected

    #  returns an empty string when message is not recognized
    def test_empty_string_unrecognized_message(self):
        with self.assertRaises(NotImplementedError):
            notice("unknown")

    #  returns a message indicating that the player is close to the treasure when hint is provided
    def test_message_player_close_to_treasure(self):
        result = notice("hint", hint="You're close to the treasure!")
        expected = "Вы близко к сокровищу!"
        assert result == expected

    #  returns a message indicating the number of treasures left when quantety is provided
    def test_message_treasures_left(self):
        result = notice("hint", quantety=3)
        expected = "Осталось 3 сокровищ."
        assert result == expected

    # returns a message indicating that the player is close to the treasure when hint is provided, even if quantety
    # is also provided
    def test_message_player_close_to_treasure_with_quantety(self):
        result = notice("hint", hint="You're close to the treasure!", quantety=2)
        expected = "Вы близко к сокровищу!"
        assert result == expected


class TestGameField:

    #  should print the default game field if no arguments are passed
    def test_default_game_field(self):
        result = game_field()
        assert result == [['[0]'.rjust(3)] * 10 for _ in range(10)]

    #  should print the game field with the player's position marked in red if check is False and player is not None
    def test_player_position_marked_in_red(self):
        # Arrange
        grid = [['[0]'.rjust(3)] * 10 for _ in range(10)]
        player = (5, 5)
        treasure = (3, 7)

        # Act
        result = game_field(grid, False, treasure, player)

        # Assert
        assert result[player[1]][player[0]] == '[\033[31mX\033[0m]'

    # should print the game field with the treasure's position marked in green if check is True and treasure is not None
    def test_treasure_position_marked_in_green(self):
        # Arrange
        grid = [['[0]'.rjust(3)] * 10 for _ in range(10)]
        player = (5, 5)
        treasure = (3, 7)

        # Act
        result = game_field(grid, True, treasure, player)

        # Assert
        assert result[treasure[1]][treasure[0]] == '[\033[32mV\033[0m]'

    #  should return the modified grid
    def test_return_modified_grid(self):
        # Arrange
        grid = [['[0]'.rjust(3)] * 10 for _ in range(10)]
        player = (5, 5)
        treasure = (3, 7)

        # Act
        result = game_field(grid, False, treasure, player)

        # Assert
        assert result is grid

    #  should print the default game field if an empty list is passed as grid
    def test_empty_list_as_grid(self):
        # Arrange
        grid = []

        # Act
        result = game_field(grid)

        # Assert
        assert result == [['[0]'.rjust(3)] * 10 for _ in range(10)]


class TestGetLog(unittest.TestCase):

    #  writes player info to log file if game_initialized is 0 and log file does not exist
    def test_writes_player_info_to_log_file_if_game_initialized_is_0_and_log_file_does_not_exist(self):
        file_path = './log.txt'
        player_info = (3, 5)
        game_initialized = 0
        Game.get_log(player_info, game_initialized)
        assert os.path.isfile(file_path)
        with open("log.txt", "r") as fr:
            content = fr.read()
            assert content == f"{player_info[0], player_info[1]}\n"
        if os.path.exists(file_path):
            os.remove(file_path)

    #  overwrites log file with player info if game_initialized is 0 and log file exists
    def test_overwrites_log_file_with_player_info_if_game_initialized_is_0_and_log_file_exists(self):
        file_path = './log.txt'
        player_info = (3, 5)
        game_initialized = 0
        with open("log.txt", "w") as fw:
            fw.write("Previous content")
        Game.get_log(player_info, game_initialized)
        assert os.path.isfile(file_path)
        with open("log.txt", "r") as fr:
            content = fr.read()
            assert content == f"{player_info[0], player_info[1]}\n"
        if os.path.exists(file_path):
            os.remove(file_path)

    #  appends player info to log file if game_initialized is not 0 and log file exists
    def test_appends_player_info_to_log_file_if_game_initialized_is_not_0_and_log_file_exists(self):
        file_path = './log.txt'
        player_info = (3, 5)
        game_initialized = 1
        with open("log.txt", "w") as fw:
            fw.write("Previous content\n")
        Game.get_log(player_info, game_initialized)
        assert os.path.isfile(file_path)
        with open("log.txt", "r") as fr:
            content = fr.read()
            assert content == f"Previous content\n{player_info[0], player_info[1]}\n"
        if os.path.exists(file_path):
            os.remove(file_path)


class TestGame(unittest.TestCase):
    ANSI_RESET = "\033[0m"
    ANSI_GREEN = "\033[32m"
    ANSI_RED = "\033[31m"

    def setUp(self):
        self.game = Game()  # Create a Game instance
        self.game.player = Player()
        self.game.treasure = TreasureMap()
        self.captured_output = StringIO()  # Capture console output

    def tearDown(self):
        print(self.captured_output.getvalue())  # Print captured output after test

    def test_start_game_welcome_message(self):
        # Redirect console output to captured_output
        with patch('sys.stdout', self.captured_output):
            self.game.start_game()

        # Assert welcome message is displayed with number of treasures
        self.assertIn("Добро пожаловать в игру «Поиск сокровища»!", self.captured_output.getvalue())
        self.assertIn("На игровом поле размером 10x10 спрятано 2 сокровище.", self.captured_output.getvalue())

    def test_start_game_initial_field(self):
        ANSI_RESET = "\033[0m"
        # Simulate player input (avoid actual user input during testing)
        self.game.player.x = 3
        self.game.player.y = 5

        # Capture initial game field
        with patch('sys.stdout', self.captured_output):
            self.game.start_game()

        # Assert initial field has player's starting position marked
        field_lines = self.captured_output.getvalue().splitlines()
        expected_line = " [▓] ".join(["[0]"] * 10)  # Replace placeholders with "[0]"
        self.assertIn(expected_line.replace("[0]", f"[ANSI_RED]X{ANSI_RESET}"), field_lines)

    def test_player_guess_correct(self):
        # Generate known treasure location
        treasure_x, treasure_y = self.game.treasure.generate_treasure()
        self.game.treasure.x = treasure_x
        self.game.treasure.y = treasure_y

        # Simulate player input matching the treasure location
        self.game.player.x = treasure_x
        self.game.player.y = treasure_y

        # Capture game output
        with patch('sys.stdout', self.captured_output):
            self.game.start_game()

        # Assert success messages and no remaining attempts prompt
        self.assertIn("Поздравляем! Вы нашли сокровище.", self.captured_output.getvalue())
        self.assertIn("Осталось 0 сокровищ.", self.captured_output.getvalue())
        self.assertNotIn("Введите координаты, чтобы проверить...", self.captured_output.getvalue())

    def test_player_guess_incorrect_within_attempts(self):
        # Set maximum attempts
        self.game.player.trys = 9

        # Simulate player input (avoid actual user input during testing)
        self.game.player.x = 1
        self.game.player.y = 2

        # Capture game output
        with patch('sys.stdout', self.captured_output):
            self.game.start_game()

        # Assert hint message and remaining attempts prompt
        self.assertIn("Сокровище где-то в другом месте...", self.captured_output.getvalue())
        self.assertIn("Введите координаты, чтобы проверить...", self.captured_output.getvalue())
        self.assertIn("Попыток: [10]", self.captured_output.getvalue())

    def test_player_guess_incorrect_exceed_attempts(self):
        # Set maximum attempts
        self.game.player.trys = 10

        # Simulate player input (avoid actual user input during testing)
        self.game.player.x = 1
        self.game.player.y = 2

        # Capture game output
        with patch('sys.stdout', self.captured_output):
            self.game.start_game()

        # Assert failure message and no remaining attempts prompt
        self.assertIn("Количество попыток исчерпано. Сокровище не найдено.", self.captured_output.getvalue())
        self.assertNotIn("Введите координаты, чтобы проверить...", self.captured_output.getvalue())

    def test_multiple_treasures_and_hints(self):
        # Generate known treasure locations
        treasure1_x, treasure1_y = self.game.treasure.generate_treasure()


if __name__ == "__main__":
    unittest.main()
