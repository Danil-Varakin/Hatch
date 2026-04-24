# Smart Patches Project: Hatch

## Motivation

Hatch is designed to simplify the process of applying Git patches. Traditional patches are complex to analyze and apply, especially in large projects. The Hatch logical language allows changes to be described declaratively, improving readability and automating the process.

## In a Nutshell

Hatch is a prototype tool for applying Git patches, functioning as a recursive interpreter for the Hatch logical language (translated as "hatch"). The language uses six operators: `...`, `>>>`, `<<<`, `^..`, `..^`, `^n..`.

### Hatch:
- Parses Markdown files containing comments, Hatch instructions, and patch content.
- Tokenizes code and identifies positions for inserting changes.
- Supports languages like Python and C++, accounting for nesting and special operators.
- Can automatically **generate** Hatch instructions by comparing two versions of a file.

## Installation

### Quick Setup from Repository

1. **Clone the repository:**
```bash
git clone https://github.com/Danil-Varakin/Hatch.git
cd Hatch
```

2. **Create a virtual environment:**
```bash
python -m venv venv
```

3. **Activate the virtual environment:**

   **Windows:**
```bash
venv\Scripts\activate
```

   **Linux/Mac:**
```bash
source venv/bin/activate
```

4. **Install the project:**
```bash
pip install -e .
```

## Usage

Hatch provides two commands: `apply` and `generate`.

### apply — Apply patch instructions to a source file

1. Prepare a Markdown file (e.g., `example.md`):
   ```markdown
   ### match:
   Your Match should be here.
   ### patch
   Your Patch should be here.
   ```
2. Prepare the source file (e.g., `example.cpp`).
3. Run via the command line:
   ```bash
   python Hatch.py apply --match example.md --in example.cpp --out result.cpp
   ```

#### apply Options

```
options:
  -h, --help           Show this help message and exit
  --match MATCH        Path to the match file (e.g., changes.md)
  --patch PATCH        Path to separate patch file, optional (e.g., patch.md)
  --in IN_FILE         Path to the input source file (e.g., main.cpp)
  --out OUT            Path to the output file (e.g., main_patched.cpp)
  --language LANGUAGE  Programming language (e.g., cpp, python). Auto-detected if not specified.
```

### generate — Generate Hatch instructions from file differences

Compares two versions of a file and automatically produces a `.md` file with Hatch match/patch instructions.

```bash
python Hatch.py generate --in new_version.cpp --in-old old_version.cpp --out changes.md
```

#### generate Options

```
options:
  -h, --help           Show this help message and exit
  --in IN_FILE         Path to the new version of the file (e.g., src/main.cpp)
  --in-old OLD_IN_FILE Path to the old version of the file (e.g., src/main_old.cpp)
  --out OUT_FILE       Path to the output markdown file (e.g., changes.md)
  --branch BRANCH      Git branch for comparison (default: master)
  --language LANGUAGE  Programming language (e.g., cpp, python). Auto-detected if not specified.
  -a, --agreement      Enable confirmation mode for each individual match
```

## Hatch Language Operators

Hatch uses a logical language with six main operators:

- `...` — Skips everything until the next specified pattern in the template (Finds all occurrences).
- `>>>` — Indicates the position for insertion.
- `<<<` — Indicates the position up to which the replacement is made (from the insertion position).
- `^..` — Skips until the first occurrence of the pattern.
- `..^` — Skips until the last occurrence of the pattern.
- `^n..` — Skips until the n-th occurrence of the pattern.

## Patch Application Examples

The following examples are real Hatch instructions from the [MatchPatch](https://github.com/Kirillkadr/MatchPatch) repository, which patches Chromium source files.

### Example 1: Adding an Include Before a Namespace (`content/common/features.cc`)

Inserts `#include "base/feature_override.h"` right after the existing features header include, before the standard library includes.

**Instruction**:
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

### Example 2: Overriding Feature Defaults Inside a Namespace (`content/browser/shared_storage/shared_storage_features.cc`)

First inserts a new include, then uses `^..` to find the first occurrence of the closing namespace brace and inserts `OVERRIDE_FEATURE_DEFAULT_STATES` before it.

**Instruction**:
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

### Example 3: Inserting a New Method After an Existing One (`content/browser/service_worker/service_worker_content_settings_proxy_impl.cc`)

Finds the end of `RequestFileSystemAccessSync` inside the `content` namespace and inserts a new `GetBraveShieldsSettings` method right after its closing brace.

**Instruction**:
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

### Example 4: Inserting a Method Inside Nested Namespaces (`content/browser/devtools/protocol/network_handler.cc`)

Navigates through two nested namespaces (`content` → `protocol`) and inserts `RequestAdblockInfoReceived` after the closing brace of `ConfigureDurableMessages`.

**Instruction**:
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

## Architecture and Repository Structure

The prototype is written in Python and uses `pytest` for testing. The project structure is as follows:

| File/Directory | Description |
|----------------|-------------|
| `Hatch.py` | Main CLI entry point with `apply` and `generate` subcommands |
| `constants.py` | Constants such as Hatch operators, supported languages, and extensions |
| `Insert.py` | Logic for inserting and replacing patches in source code |
| `SearchCode.py` | Logic for searching insertion positions in code |
| `TokenizeCode.py` | Code tokenization with support for Hatch operators |
| `Utilities.py` | Utility functions for file reading/writing and Markdown parsing |
| `Logging.py` | Colorized logging system with truncation support |
| `getChange.py` | Logic for detecting code changes between two file versions |
| `gitUtils.py` | Git utilities: reading commits from branches, computing diffs |
| `CompressionVersion.py` | Generates Hatch match/patch instructions from file differences |
| `CompressionInput.py` | Creates Markdown instruction files from match/patch pairs |
| `CompressionConstants/` | Per-language constants for the instruction generation engine |
| `MainTest.py` | Module for automated testing |
| `pyproject.toml` | Package configuration and dependencies |
| `test/PassedTests/` | Test files (C++ and Markdown) for successful scenarios |
| `test/FailedTests/` | Test files for error scenarios |

## Conclusion

Hatch is an experimental tool for managing Git patches through the Hatch logical language, simplifying and structuring the code modification process. The tool is under active development, and we welcome any suggestions and contributions to the project via [GitHub](https://github.com/Danil-Varakin/Hatch).
