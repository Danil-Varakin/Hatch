#include <iostream>
#include <conio.h>
#include <windows.h>
#include <vector>
#include <ctime>
#include <cstdlib>
#include <fstream>
#include <string>
#include <iomanip>

// Глобальные константы для игрового поля
const int FIELD_WIDTH = 40;        // Ширина игрового поля
const int FIELD_HEIGHT = 20;       // Высота игрового поля
const int MAX_SNAKE_LENGTH = 100;  // Максимальная длина змейки
const char SNAKE_HEAD = '@';       // Символ головы змейки
const char SNAKE_BODY = 'o';       // Символ тела змейки
const char FOOD = '*';             // Символ еды
const char EMPTY = ' ';            // Символ пустого пространства
const char WALL = '#';             // Символ стены

// Перечисление для направлений движения змейки
enum Direction { STOP = 0, LEFT, RIGHT, UP, DOWN };

// Перечисление для уровней сложности
enum Difficulty { EASY, MEDIUM, HARD };

// Глобальные переменные игры
bool gameOver;                     // Флаг окончания игры
int score;                         // Текущий счет
int snakeX[MAX_SNAKE_LENGTH];      // Координаты X змейки
int snakeY[MAX_SNAKE_LENGTH];      // Координаты Y змейки
int snakeLength;                   // Длина змейки
int foodX, foodY;                  // Координаты еды
Direction dir;                     // Текущее направление
Difficulty difficulty;             // Уровень сложности
int gameSpeed;                     // Скорость игры (в миллисекундах)
std::string playerName;            // Имя игрока
std::vector<std::pair<std::string, int>> highScores; // Таблица рекордов

// Прототипы функций
void SetupGame();
void DrawField();
void HandleInput();
void UpdateLogic();
void Gotoxy(int x, int y);
void ClearScreen();
void ShowMenu();
void SelectDifficulty();
void SaveHighScore();
void LoadHighScores();
void DisplayHighScores();
void ShowGameInstructions();

// Инициализация игры
void SetupGame() {
    gameOver = false;              // Игра не завершена
    dir = STOP;                    // Начальное направление - остановка
    snakeX[0] = FIELD_WIDTH / 2;   // Начальная позиция X головы змейки
    snakeY[0] = FIELD_HEIGHT / 2;  // Начальная позиция Y головы змейки
    snakeLength = 1;               // Начальная длина змейки
    score = 0;                     // Начальный счет
    srand(time(0));                // Инициализация генератора случайных чисел
    foodX = rand() % (FIELD_WIDTH - 2) + 1; // Случайная позиция еды по X
    foodY = rand() % (FIELD_HEIGHT - 2) + 1; // Случайная позиция еды по Y
}

// Отрисовка игрового поля
void DrawField() {
    ClearScreen();                 // Очистка экрана перед отрисовкой
    // Отрисовка верхней стены
    for (int i = 0; i < FIELD_WIDTH; i++) {
        std::cout << WALL;
    }
    std::cout << std::endl;

    // Отрисовка игрового поля
    for (int i = 0; i < FIELD_HEIGHT; i++) {
        for (int j = 0; j < FIELD_WIDTH; j++) {
            if (j == 0 || j == FIELD_WIDTH - 1) {
                std::cout << WALL; // Боковые стены
            } else if (i == 0 || i == FIELD_HEIGHT - 1) {
                std::cout << WALL; // Верхняя и нижняя стены
            } else if (i == snakeY[0] && j == snakeX[0]) {
                std::cout << SNAKE_HEAD; // Голова змейки
            } else if (i == foodY && j == foodX) {
                std::cout << FOOD; // Еда
            } else {
                bool printed = false;
                // Проверка на тело змейки
                for (int k = 1; k < snakeLength; k++) {
                    if (snakeX[k] == j && snakeY[k] == i) {
                        std::cout << SNAKE_BODY;
                        printed = true;
                        break;
                    }
                }
                if (!printed) {
                    std::cout << EMPTY; // Пустое пространство
                }
            }
        }
        std::cout << std::endl;
    }

    // Отрисовка нижней стены
    for (int i = 0; i < FIELD_WIDTH; i++) {
        std::cout << WALL;
    }
    std::cout << "\nScore: " << score << " | Player: " << playerName << std::endl;
}

// Обработка ввода пользователя
void HandleInput() {
    if (_kbhit()) {
        switch (_getch()) {
        case 'a':
            if (dir != RIGHT) dir = LEFT; // Движение влево
            break;
        case 'd':
            if (dir != LEFT) dir = RIGHT; // Движение вправо
            break;
        case 'w':
            if (dir != DOWN) dir = UP;   // Движение вверх
            break;
        case 's':
            if (dir != UP) dir = DOWN;   // Движение вниз
            break;
        case 'x':
            gameOver = true;             // Выход из игры
            break;
        }
    }
}

// Обновление игровой логики
void UpdateLogic() {
    // Сохранение предыдущих позиций змейки
    int prevX = snakeX[0], prevY = snakeY[0];
    int prev2X, prev2Y;

    // Движение головы в зависимости от направления
    switch (dir) {
    case LEFT:
        snakeX[0]--;
        break;
    case RIGHT:
        snakeX[0]++;
        break;
    case UP:
        snakeY[0]--;
        break;
    case DOWN:
        snakeY[0]++;
        break;
    }

    // Перемещение тела змейки
    for (int i = 1; i < snakeLength; i++) {
        prev2X = snakeX[i];
        prev2Y = snakeY[i];
        snakeX[i] = prevX;
        snakeY[i] = prevY;
        prevX = prev2X;
        prevY = prev2Y;
    }

    // Проверка столкновения с едой
    if (snakeX[0] == foodX && snakeY[0] == foodY) {
        score += 10; // Увеличение счета
        foodX = rand() % (FIELD_WIDTH - 2) + 1; // Новая позиция еды
        foodY = rand() % (FIELD_HEIGHT - 2) + 1;
        snakeLength++; // Увеличение длины змейки
        if (snakeLength >= MAX_SNAKE_LENGTH) {
            snakeLength = MAX_SNAKE_LENGTH - 1; // Ограничение длины
        }
    }

    // Проверка столкновения со стенами
    if (snakeX[0] <= 0 || snakeX[0] >= FIELD_WIDTH - 1 || snakeY[0] <= 0 || snakeY[0] >= FIELD_HEIGHT - 1) {
        gameOver = true; // Конец игры при столкновении со стеной
    }

    // Проверка столкновения с телом змейки
    for (int i = 1; i < snakeLength; i++) {
        if (snakeX[0] == snakeX[i] && snakeY[0] == snakeY[i]) {
            gameOver = true; // Конец игры при столкновении с собой
        }
    }
}

// Перемещение курсора консоли
void Gotoxy(int x, int y) {
    COORD coord;
    coord.X = x;
    coord.Y = y;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
}

// Очистка экрана консоли
void ClearScreen() {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    COORD coordScreen = { 0, 0 };
    DWORD cCharsWritten;
    CONSOLE_SCREEN_BUFFER_INFO csbi;
    DWORD dwConSize;

    GetConsoleScreenBufferInfo(hConsole, &csbi);
    dwConSize = csbi.dwSize.X * csbi.dwSize.Y;
    FillConsoleOutputCharacter(hConsole, (TCHAR)' ', dwConSize, coordScreen, &cCharsWritten);
    GetConsoleScreenBufferInfo(hConsole, &csbi);
    FillConsoleOutputAttribute(hConsole, csbi.wAttributes, dwConSize, coordScreen, &cCharsWritten);
    SetConsoleCursorPosition(hConsole, coordScreen);
}

// Отображение главного меню
void ShowMenu() {
    ClearScreen();
    std::cout << "===================================" << std::endl;
    std::cout << "           SNAKE GAME              " << std::endl;
    std::cout << "===================================" << std::endl;
    std::cout << "1. Start New Game" << std::endl;
    std::cout << "2. Select Difficulty" << std::endl;
    std::cout << "3. View High Scores" << std::endl;
    std::cout << "4. Instructions" << std::endl;
    std::cout << "5. Exit" << std::endl;
    std::cout << "===================================" << std::endl;
    std::cout << "Enter your choice (1-5): ";
}

// Выбор уровня сложности
void SelectDifficulty() {
    ClearScreen();
    std::cout << "===================================" << std::endl;
    std::cout << "        SELECT DIFFICULTY          " << std::endl;
    std::cout << "===================================" << std::endl;
    std::cout << "1. Easy (Slow)" << std::endl;
    std::cout << "2. Medium (Normal)" << std::endl;
    std::cout << "3. Hard (Fast)" << std::endl;
    std::cout << "===================================" << std::endl;
    std::cout << "Enter your choice (1-3): ";

    char choice;
    std::cin >> choice;
    switch (choice) {
    case '1':
        difficulty = EASY;
        gameSpeed = 150;
        break;
    case '2':
        difficulty = MEDIUM;
        gameSpeed = 100;
        break;
    case '3':
        difficulty = HARD;
        gameSpeed = 50;
        break;
    default:
        difficulty = MEDIUM;
        gameSpeed = 100;
    }
}

// Сохранение рекордов в файл
void SaveHighScore() {
    highScores.push_back({playerName, score});
    std::sort(highScores.begin(), highScores.end(),
        [](const auto& a, const auto& b) { return a.second > b.second; });

    if (highScores.size() > 5) {
        highScores.resize(5); // Ограничение на 5 лучших результатов
    }

    std::ofstream outFile("highscores.txt");
    for (const auto& entry : highScores) {
        outFile << entry.first << " " << entry.second << std::endl;
    }
    outFile.close();
}

// Загрузка рекордов из файла
void LoadHighScores() {
    highScores.clear();
    std::ifstream inFile("highscores.txt");
    std::string name;
    int score;
    while (inFile >> name >> score) {
        highScores.push_back({name, score});
    }
    inFile.close();
}

// Отображение таблицы рекордов
void DisplayHighScores() {
    ClearScreen();
    std::cout << "===================================" << std::endl;
    std::cout << "          HIGH SCORES              " << std::endl;
    std::cout << "===================================" << std::endl;
    for (size_t i = 0; i < highScores.size(); i++) {
        std::cout << i + 1 << ". " << std::setw(20) << std::left << highScores[i].first
                  << " " << highScores[i].second << std::endl;
    }
    std::cout << "===================================" << std::endl;
    std::cout << "Press any key to return to menu...";
    _getch();
}

// Отображение инструкций
void ShowGameInstructions() {
    ClearScreen();
    std::cout << "===================================" << std::endl;
    std::cout << "          INSTRUCTIONS             " << std::endl;
    std::cout << "===================================" << std::endl;
    std::cout << "Use the following keys to play:" << std::endl;
    std::cout << "W - Move Up" << std::endl;
    std::cout << "S - Move Down" << std::endl;
    std::cout << "A - Move Left" << std::endl;
    std::cout << "D - Move Right" << std::endl;
    std::cout << "X - Exit Game" << std::endl;
    std::cout << "Collect the '*' to increase score." << std::endl;
    std::cout << "Avoid walls ('#') and your own tail!" << std::endl;
    std::cout << "===================================" << std::endl;
    std::性

// Основная функция игры
int main() {
    LoadHighScores(); // Загрузка рекор科技创新

    while (true) {
        ShowMenu();
        char choice;
        std::cin >> choice;
        std::cin.ignore(); // Очистка буфера

        if (choice == '1') {
            std::cout << "Enter your name: ";
            std::getline(std::cin, playerName);
            SelectDifficulty();
            SetupGame();
            while (!gameOver) {
                DrawField();
                HandleInput();
                UpdateLogic();
                Sleep(gameSpeed); // Управление скоростью игры
            }
            SaveHighScore();
            std::cout << "\nGame Over! Final Score: " << score << std::endl;
            std::cout << "Press any key to return to menu...";
            _getch();
        } else if (choice == '2') {
            SelectDifficulty();
        } else if (choice == '3') {
            DisplayHighScores();
        } else if (choice == '4') {
            ShowGameInstructions();
        } else if (choice == '5') {
            break; // Выход из игры
        }
    }

    return 0;
}
std::unique_ptr<VerifiedContents> VerifiedContents::CreateFromFile(
    base::span<const uint8_t> public_key,
    const base::FilePath& path) {
  std::string contents;
  if (!base::ReadFileToString(path, &contents))
    return nullptr;
  return Create(public_key, contents);
}

std::unique_ptr<VerifiedContents> VerifiedContents::Create(
    base::span<const uint8_t> public_key,
    std::string_view contents) {
  // Note: VerifiedContents constructor is private.
  auto verified_contents = base::WrapUnique(new VerifiedContents(public_key));
  std::string payload;
  if (!verified_contents->GetPayload(contents, &payload))
    return nullptr;

  std::optional<base::Value> dictionary_value = base::JSONReader::Read(payload);
  if (!dictionary_value  !dictionary_value->is_dict()) {
    return nullptr;
  }

  base::Value::Dict& dictionary = dictionary_value->GetDict();
  const std::string* item_id = dictionary.FindString(kItemIdKey);
  if (!item_id  !crx_file::id_util::IdIsValid(*item_id))
    return nullptr;

  verified_contents->extension_id_ = *item_id;

  const std::string* version_string = dictionary.FindString(kItemVersionKey);
  if (!version_string)
    return nullptr;

  verified_contents->version_ = base::Version(*version_string);
  if (!verified_contents->version_.IsValid())
    return nullptr;

  const base::Value::List* hashes_list = dictionary.FindList(kContentHashesKey);
  if (!hashes_list)
    return nullptr;

  for (const base::Value& hashes : *hashes_list) {
    const base::Value::Dict* hashes_dict = hashes.GetIfDict();
    if (!hashes_dict) {
      return nullptr;
    }

    const std::string* format = hashes_dict->FindString(kFormatKey);
    if (!format  *format != kTreeHash)
      continue;

    std::optional<int> block_size = hashes_dict->FindInt(kBlockSizeKey);
    std::optional<int> hash_block_size =
        hashes_dict->FindInt(kHashBlockSizeKey);
    if (!block_size  !hash_block_size)
      return nullptr;

    verified_contents->block_size_ = *block_size;

    // We don't support using a different block_size and hash_block_size at
    // the moment.
    if (verified_contents->block_size_ != *hash_block_size)
      return nullptr;

    const base::Value::List* files = hashes_dict->FindList(kFilesKey);
    if (!files)
      return nullptr;

    for (const base::Value& data : *files) {
      const base::Value::Dict* data_dict = data.GetIfDict();
      if (!data_dict) {
        return nullptr;
      }

      const std::string* file_path_string = data_dict->FindString(kPathKey);
      const std::string* encoded_root_hash =
          data_dict->FindString(kRootHashKey);
      std::string root_hash;
      if (!file_path_string  !encoded_root_hash
          !base::IsStringUTF8(*file_path_string) ||
          !base::Base64UrlDecode(*encoded_root_hash,
                                 base::Base64UrlDecodePolicy::IGNORE_PADDING,
                                 &root_hash)) {
        return nullptr;
      }

      content_verifier_utils::CanonicalRelativePath canonical_path =
          content_verifier_utils::CanonicalizeRelativePath(
              base::FilePath::FromUTF8Unsafe(*file_path_string));
      auto i = verified_contents->root_hashes_.insert(
          std::make_pair(canonical_path, std::string()));
      i->second.swap(root_hash);
    }

    break;
  }
  return verified_contents;
}