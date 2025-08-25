# Проект Smart Patches: Hatch

## Мотивация

Hatch разработан для упрощения процесса применения патчей Git. Традиционные патчи сложно анализировать и применять, особенно в крупных проектах. Логический язык Hatch позволяет описывать изменения декларативно, улучшая читаемость и автоматизируя процесс.

## В двух словах

Hatch — это прототип инструмента для применения патчей Git, работающий как рекурсивный интерпретатор для логического языка Hatch (переводится как «Люк»). Язык использует шесть операторов: `...`, `>>>`, `<<<`, `^..`, `..^`, `^n..`.


#### Hatch:

- Разбирает файлы Markdown, содержащие комментарии, инструкции Hatch и содержимое патча.
- Токенизирует код и определяет позиции для вставки изменений.
- Поддерживает языки, такие как Python и C++, учитывая вложенность и специальные операторы.

## Использование

1. Подготовьте файл Markdown (например, `example.md`):

   ```markdown
   ### match:
   Здесь должно быть ваше соответствие.
   ### patch
   Здесь должно быть ваше исправление.
   ```
2. Подготовьте исходный файл (например, `example.cpp`).
3. Укажите язык программирования (например, `cpp`) во время обработки(По умолчанию язык выбирается от расширения файла).
4. Запустите обработку через командную строку:

   ```bash
    MainCMD.py [-h] [--match MATCH] [--patch PATCH] [--in IN_FILE] [--out OUT] [--language LANGUAGE]
   ```
  #### Опции командной строки
  ```
  Опции:
  -h, --help           Показать это справочное сообщение и выйти
  --match MATCH        Путь к файлу соответствия (например, file.md)
  --patch PATCH        Путь к файлу патча, необязательно (например, patch.md)
  --in IN_FILE         Путь к входному файлу (например, 1.cpp)
  --out OUT            Путь к выходному файлу (например, 1_r.txt)
  --language LANGUAGE  Язык программирования (например, cpp)
  ```

## Операторы языка Hatch

Hatch использует логический язык с шестью основными операторами:

- `...` — Пропускает все  до следующего указанного  в шаблоне паттерна (Находит все вхождения).
- `>>>` — Указывает позицию для вставки.
- `<<<` — Указывает позицию до которой производится замена(От позиции вставки).
- `^..` — Пропускает до первого вхождения паттерна.
- `..^` — Пропускает до последнего вхождения паттерна.
- `^n..` — Пропускает до n-го вхождения паттерна.

## Примеры применения патчей

### Тест 1: Вставка перед закрывающей скобкой

**Исходный код**:

```cpp
#include <iostream>

class Calculator {
public:
    double calculate(double x, double y) {
        double result = x + y;
        std::cout << "Calculation in progress, intermediate result: " << result << std::endl;
        result *= 1.5; // Scale result
        if (result > 0.0) {

        }
        return result;
    }
};
```

**Инструкция**:

```markdown
### match:
...class Calculator {...double calculate(...)...if (result > 0.0) >>> 
...
### patch
std::cout << "Calculation in progress, intermediate result: " << result << std::endl;result *= 1.5; // Scale result
```

**Результат**:

```cpp
#include <iostream>

class Calculator {
public:
    double calculate(double x, double y) {
        double result = x + y;
        std::cout << "Calculation in progress, intermediate result: " << result << std::endl;
        result *= 1.5; // Scale result
        if (result > 0.0) std::cout << "Calculation in progress, intermediate result: " << result << std::endl;result *= 1.5; // Scale result {
        }
        return result;
    }
};
```

### Тест 2: Замена и вставка с использованием `^n..`

**Исходный код**:

```cpp
func VB   (asass) {
    class FF {
        class GG {
        }
    }
void f {
template<typename T>
void f() {
  {const int x = 10;}
  if ( x > 10) {
    for (;;) {
      if (x > 10) {
         std::cout << "abc";
         std::cout << "edf";
         77
      }- 9 ()
    }- 9
    register
    int
  }- 9
  zxc
  66 -- () 33
}- 9 8
```

**Инструкция**:

```markdown
### match:
...
void ^3.. >>> f(...) <<< {...}...
### patch
print("[INFO]: ")
```

**Результат**:

```cpp
func VB   (asass) {
    class FF {
        class GG {
        }
    }
void f {
template<typename T>
print("[INFO]: ") {
  {const int x = 10;}
  if ( x > 10) {
    for (;;) {
      if (x > 10) {
         std::cout << "abc";
         std::cout << "edf";
         77
      }- 9 ()
    }- 9
    register
    int
  }- 9
  zxc
  66 -- () 33
}- 9 8
```

### Тест 3: Вставка после закрывающей скобки

**Исходный код**:

```cpp
std::unique_ptr<VerifiedContents> VerifiedContents::CreateFromFile(
    base::span<const uint8_t> public_key,
    const base::FilePath& path) {
  std::string contents;
  if (!base::ReadFileToString(path, &contents))
    return nullptr;
  return Create(public_key, contents);
}
```

**Инструкция**:

```markdown
### match:
...VerifiedContents::CreateFromFile ^.. { ...
} >>> 
...
### patch
_ChromiumImpl
```

**Результат**:

```cpp
std::unique_ptr<VerifiedContents> VerifiedContents::CreateFromFile(
    base::span<const uint8_t> public_key,
    const base::FilePath& path) {
  std::string contents;
  if (!base::ReadFileToString(path, &contents))
    return nullptr;
  return Create(public_key, contents);
}
_ChromiumImpl
```

### Тест 4: Замена и вставка с использованием `..^`

**Исходный код**:

```cpp
class BraveSearchTest : public InProcessBrowserTest {
 public:
  BraveSearchTest() = default;

  void SetUpOnMainThread() override {
    InProcessBrowserTest::SetUpOnMainThread();
    mock_cert_verifier_.mock_cert_verifier()->set_default_result(net::OK);
    host_resolver()->AddRule("*", "127.0.0.1");

    https_server_ = std::make_unique<net::EmbeddedTestServer>(
        net::test_server::EmbeddedTestServer::TYPE_HTTPS);
    https_server_->RegisterRequestHandler(base::BindRepeating(
        &BraveSearchTest::HandleRequest, base::Unretained(this)));

    base::FilePath test_data_dir;
    base::PathService::Get(brave::DIR_TEST_DATA, &test_data_dir);
    test_data_dir = test_data_dir.AppendASCII(kEmbeddedTestServerDirectory);
    https_server_->ServeFilesFromDirectory(test_data_dir);

    ASSERT_TRUE(https_server_->Start());
    GURL url = https_server()->GetURL("google.com", "/search");
    brave_search::BraveSearchFallbackHost::SetBackupProviderForTest(url);

    // Force default search engine to Google
    // Some tests will fail if Brave is default
    auto* template_url_service =
        TemplateURLServiceFactory::GetForProfile(browser()->profile());
    TemplateURL* google = template_url_service->GetTemplateURLForKeyword(u":g");
    template_url_service->SetUserSelectedDefaultSearchProvider(google);
  }
};
```

**Инструкция**:

```markdown
### match:
...
class ..^ {...>>>};...
### patch
print("[INFO]: ")
```

**Результат**:

```cpp
class BraveSearchTest : public InProcessBrowserTest {
 public:
  BraveSearchTest() = default;

  void SetUpOnMainThread() override {
    InProcessBrowserTest::SetUpOnMainThread();
    mock_cert_verifier_.mock_cert_verifier()->set_default_result(net::OK);
    host_resolver()->AddRule("*", "127.0.0.1");

    https_server_ = std::make_unique<net::EmbeddedTestServer>(
        net::test_server::EmbeddedTestServer::TYPE_HTTPS);
    https_server_->RegisterRequestHandler(base::BindRepeating(
        &BraveSearchTest::HandleRequest, base::Unretained(this)));

    base::FilePath test_data_dir;
    base::PathService::Get(brave::DIR_TEST_DATA, &test_data_dir);
    test_data_dir = test_data_dir.AppendASCII(kEmbeddedTestServerDirectory);
    https_server_->ServeFilesFromDirectory(test_data_dir);

    ASSERT_TRUE(https_server_->Start());
    GURL url = https_server()->GetURL("google.com", "/search");
    brave_search::BraveSearchFallbackHost::SetBackupProviderForTest(url);

    // Force default search engine to Google
    // Some tests will fail if Brave is default
    auto* template_url_service =
        TemplateURLServiceFactory::GetForProfile(browser()->profile());
    TemplateURL* google = template_url_service->GetTemplateURLForKeyword(u":g");
    template_url_service->SetUserSelectedDefaultSearchProvider(google);
  }
print("[INFO]: ")
};
```

## Архитектура и структура репозитория

Прототип написан на Python и использует `pytest` для тестирования. Структура проекта следующая:

| Файл/Директория | Описание |
| --- | --- |
| `unique3.cpp`, `unique5.cpp`, ... | Исходные файлы C++ для тестирования |
| `unique3.md`, `unique5.md`, ... | Файлы Markdown с инструкциями и патчами для тестирования |
| `test/PassedTests/` | Тестовые файлы (C++ и Markdown) для успешных сценариев |
| `test/FailedTests/` | Тестовые файлы для сценариев с ошибками |
| `constants.py` | Константы, такие как операторы Hatch, поддерживаемые языки и расширения |
| `Insert.py` | Логика для вставки и замены патчей в исходном коде |
| `MainCMD.py` | Точка входа для интерфейса командной строки |
| `MainTest.py` | Модуль для автоматизированного тестирования |
| `SearchCode.py` | Логика для поиска позиций вставки в коде |
| `TokenizeCode.py` | Токенизация кода с поддержкой операторов Hatch |
| `Utilities.py` | Вспомогательные функции для чтения/записи файлов и парсинга Markdown |
| `CodeComprasion.py ` |Будущая логика создание Mаtch относительно измененного кода |

## Заключение

Hatch — это экспериментальный инструмент для управления патчами Git с использованием логического языка Hatch, упрощающий и структурирующий процесс модификации кода. Инструмент находится в активной разработке, и мы приветствуем любые предложения и вклад в проект через GitHub.