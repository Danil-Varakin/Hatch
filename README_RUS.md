# Проект Smart Patches: Hatch

## Мотивация

Hatch разработан для упрощения процесса применения патчей Git. Традиционные патчи сложно анализировать и применять, особенно в крупных проектах. Логический язык Hatch позволяет описывать изменения декларативно, улучшая читаемость и автоматизируя процесс.

## В двух словах

Hatch — это прототип инструмента для применения патчей Git, работающий как рекурсивный интерпретатор для логического языка Hatch (переводится как «Люк»). Язык использует шесть операторов: `...`, `>>>`, `<<<`, `^..`, `..^`, `^n..`.

### Hatch:

- Разбирает файлы Markdown, содержащие комментарии, инструкции Hatch и содержимое патча.
- Токенизирует код и определяет позиции для вставки изменений.
- Поддерживает языки, такие как Python и C++, учитывая вложенность и специальные операторы.
- Умеет автоматически **генерировать** инструкции Hatch, сравнивая две версии файла.

## Инициализация

### Быстрая установка из репозитория

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/Danil-Varakin/Hatch.git
cd Hatch
```

2. **Создайте виртуальное окружение:**
```bash
python -m venv venv
```

3. **Активируйте виртуальное окружение:**
   
   **Windows:**
```bash
venv\Scripts\activate
```
   
   **Linux/Mac:**
```bash
source venv/bin/activate
```

4. **Установите проект:**
```bash
pip install -e .
```

## Использование

Hatch предоставляет две команды: `apply` и `generate`.

### apply — Применить инструкции патча к исходному файлу

1. Подготовьте файл Markdown (например, `example.md`):

   ```markdown
   ### match:
   Здесь должно быть ваше соответствие.
   ### patch
   Здесь должно быть ваше исправление.
   ```
2. Подготовьте исходный файл (например, `example.cpp`).
3. Запустите обработку через командную строку:

   ```bash
   python Hatch.py apply --match example.md --in example.cpp --out result.cpp
   ```

#### Опции команды apply

```
Опции:
  -h, --help           Показать это справочное сообщение и выйти
  --match MATCH        Путь к файлу соответствия (например, changes.md)
  --patch PATCH        Путь к отдельному файлу патча, необязательно (например, patch.md)
  --in IN_FILE         Путь к входному исходному файлу (например, main.cpp)
  --out OUT            Путь к выходному файлу (например, main_patched.cpp)
  --language LANGUAGE  Язык программирования (например, cpp, python). Определяется автоматически, если не указан.
```

### generate — Сгенерировать инструкции Hatch из различий между файлами

Сравнивает две версии файла и автоматически создаёт `.md` файл с инструкциями match/patch.

```bash
python Hatch.py generate --in new_version.cpp --in-old old_version.cpp --out changes.md
```

#### Опции команды generate

```
Опции:
  -h, --help           Показать это справочное сообщение и выйти
  --in IN_FILE         Путь к новой версии файла (например, src/main.cpp)
  --in-old OLD_IN_FILE Путь к старой версии файла (например, src/main_old.cpp)
  --out OUT_FILE       Путь к выходному файлу Markdown (например, changes.md)
  --branch BRANCH      Ветка Git для сравнения (по умолчанию: master)
  --language LANGUAGE  Язык программирования (например, cpp, python). Определяется автоматически, если не указан.
  -a, --agreement      Включить режим подтверждения для каждого отдельного совпадения
```

## Операторы языка Hatch

Hatch использует логический язык с шестью основными операторами:

- `...` — Пропускает все до следующего указанного в шаблоне паттерна (Находит все вхождения).
- `>>>` — Указывает позицию для вставки.
- `<<<` — Указывает позицию до которой производится замена(От позиции вставки).
- `^..` — Пропускает до первого вхождения паттерна.
- `..^` — Пропускает до последнего вхождения паттерна.
- `^n..` — Пропускает до n-го вхождения паттерна.

## Примеры применения патчей

Следующие примеры — это реальные инструкции Hatch из репозитория [MatchPatch](https://github.com/Kirillkadr/MatchPatch), который патчит исходные файлы Chromium.

### Пример 1: Добавление include перед namespace (`content/common/features.cc`)

Вставляет `#include "base/feature_override.h"` сразу после существующего заголовочного include, перед стандартными библиотечными includes.

**Инструкция**:
```markdown
### match
```cpp
...
// found in the LICENSE file.
 #include "content/common/features.h"
 
 >>> 
#include "base/feature_list.h"

 ... 
```
### patch
```cpp
#include "base/feature_override.h"
#include "build/build_config.h"

```
```

---

### Пример 2: Переопределение дефолтных значений фич внутри namespace (`content/browser/shared_storage/shared_storage_features.cc`)

Сначала вставляет новый include, затем использует `^..` для нахождения первого вхождения закрывающей скобки namespace и вставляет `OVERRIDE_FEATURE_DEFAULT_STATES` перед ней.

**Инструкция**:
```markdown
### match
```cpp
...
// found in the LICENSE file.
 #include "content/browser/shared_storage/shared_storage_features.h"
 
 >>> 
namespace content::features {
 ... 
```
### patch
```cpp
#include "base/feature_override.h"

```

### match
```cpp
...
 
 namespace content::features { ... 
 6.0 
 ) 
 ; 
 >>> 
 ... } ...  
```
### patch
```cpp
OVERRIDE_FEATURE_DEFAULT_STATES({{
    {kSharedStorageSelectURLLimit, base::FEATURE_DISABLED_BY_DEFAULT},
}});

```
```

---

### Пример 3: Вставка нового метода после существующего (`content/browser/service_worker/service_worker_content_settings_proxy_impl.cc`)

Находит конец метода `RequestFileSystemAccessSync` внутри namespace `content` и вставляет новый метод `GetBraveShieldsSettings` сразу после его закрывающей скобки.

**Инструкция**:
```markdown
### match
```cpp
...
 
 namespace content { ... 
 
 void ServiceWorkerContentSettingsProxyImpl::RequestFileSystemAccessSync(
    RequestFileSystemAccessSyncCallback callback) { ... 
mojo::ReportBadMessage(
      "The FileSystem API is not exposed to service workers "
      "but somehow a service worker requested access.");
 } 
 >>> 
 ... } ...  
```
### patch
```cpp
void ServiceWorkerContentSettingsProxyImpl::GetBraveShieldsSettings(
    GetBraveShieldsSettingsCallback callback) {
  DCHECK_CURRENTLY_ON(BrowserThread::UI);
  // May be shutting down.
  if (!context_wrapper_->browser_context()) {
    std::move(callback).Run(brave_shields::mojom::ShieldsSettings::New());
    return;
  }
  // Shields should also work in opaque origins.
  const GURL url = origin_.GetTupleOrPrecursorTupleIfOpaque().GetURL();
  std::move(callback).Run(
      GetContentClient()->browser()->WorkerGetBraveShieldSettings(
          url, context_wrapper_->browser_context()));
}

```
```

---

### Пример 4: Вставка метода внутри вложенных namespace (`content/browser/devtools/protocol/network_handler.cc`)

Проходит через два вложенных namespace (`content` → `protocol`) и вставляет `RequestAdblockInfoReceived` после закрывающей скобки `ConfigureDurableMessages`.

**Инструкция**:
```markdown
### match
```cpp
...
 
 namespace content { ... 
 
 namespace protocol { ... 
 
 void NetworkHandler::ConfigureDurableMessages(
    std::optional<int> max_total_size,
    std::optional<int> max_resource_size,
    std::unique_ptr<ConfigureDurableMessagesCallback> callback) { ... 
MaybeEnableDurableMessages(base::BindOnce(
      &ConfigureDurableMessagesCallback::sendSuccess, std::move(callback)));
 } 
 >>> 
 ... } ...  } ...  
```
### patch
```cpp
void NetworkHandler::RequestAdblockInfoReceived(
    const std::string& request_id,
    std::unique_ptr<protocol::Network::AdblockInfo> info) {
  if (!enabled_) {
    return;
  }
  frontend_->RequestAdblockInfoReceived(request_id, std::move(info));
}

```
```

## Архитектура и структура репозитория

Прототип написан на Python и использует `pytest` для тестирования. Структура проекта следующая:

| Файл/Директория | Описание |
| --- | --- |
| `Hatch.py` | Главная точка входа CLI с командами `apply` и `generate` |
| `constants.py` | Константы, такие как операторы Hatch, поддерживаемые языки и расширения |
| `Insert.py` | Логика для вставки и замены патчей в исходном коде |
| `SearchCode.py` | Логика для поиска позиций вставки в коде |
| `TokenizeCode.py` | Токенизация кода с поддержкой операторов Hatch |
| `Utilities.py` | Вспомогательные функции для чтения/записи файлов и парсинга Markdown |
| `Logging.py` | Система цветного логирования с поддержкой усечения вывода |
| `getChange.py` | Логика определения изменений между двумя версиями файла |
| `gitUtils.py` | Git-утилиты: чтение коммитов из веток, вычисление diff |
| `CompressionVersion.py` | Генерирует инструкции Hatch match/patch из различий между файлами |
| `CompressionInput.py` | Создаёт файлы Markdown с инструкциями из пар match/patch |
| `CompressionConstants/` | Per-language константы для движка генерации инструкций |
| `MainTest.py` | Модуль для автоматизированного тестирования |
| `pyproject.toml` | Конфигурация пакета и зависимости |
| `test/PassedTests/` | Тестовые файлы (C++ и Markdown) для успешных сценариев |
| `test/FailedTests/` | Тестовые файлы для сценариев с ошибками |

## Заключение

Hatch — это экспериментальный инструмент для управления патчами Git с использованием логического языка Hatch, упрощающий и структурирующий процесс модификации кода. Инструмент находится в активной разработке, и мы приветствуем любые предложения и вклад в проект через [GitHub](https://github.com/Danil-Varakin/Hatch).
