# Smart Patches Project: Hatch

## Motivation

Hatch is designed to simplify the process of applying Git patches. Traditional patches are complex to analyze and apply, especially in large projects. The Hatch logical language allows changes to be described declaratively, improving readability and automating the process.

## In a Nutshell

Hatch is a prototype tool for applying Git patches, functioning as a recursive interpreter for the Hatch logical language (translated as "hatch"). The language uses six operators: `...`, `>>>`, `<<<`, `^..`, `..^`, `^n..`.

#№## Hatch:
- Parses Markdown files containing comments, Hatch instructions, and patch content.
- Tokenizes code and identifies positions for inserting changes.
- Supports languages like Python and C++, accounting for nesting and special operators.


## Usage

1. Prepare a Markdown file (e.g., `example.md`):
   ```markdown
   ### match:
   Your Match should be here.
   ### patch
   Your Patch should be here.
   ```
2. Prepare the source file (e.g., `example.cpp`).
3. Specify the programming language (e.g., `cpp`) during processing(The default value is relative to the file extension).
4. Run the processing via the command line:
   ```bash
   python source/MainCMD.py --match test/example.md --in source/example.cpp --out result.cpp
   ```

  #### Command-Line Options

  ```
  options:
    -h, --help           Show this help message and exit
    --match MATCH        Path to the match file (e.g., file.md)
    --patch PATCH        Path to the patch file, optional (e.g., patch.md)
    --in IN_FILE         Path to the input file (e.g., 1.cpp)
    --out OUT            Path to the output file (e.g., 1_r.txt)
    --language LANGUAGE  Programming language (e.g., cpp)
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

### Test 1: Insertion Before Closing Parenthesis

**Source Code**:
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

**Instruction**:
```markdown
### match:
...class Calculator {...double calculate(...)...if (result > 0.0) >>> 
...
### patch
std::cout << "Calculation in progress, intermediate result: " << result << std::endl;result *= 1.5; // Scale result
```

**Result**:
```cpp
#include <iostream>

class Calculator {
public:
    double calculate(double x, double y) {
        double result = x + y;
        std::cout << "Calculation in progress, intermediate result: " << result << std::endl;
        result *= 1.5; // Scale result
        if (result > 0.0) std::cout << "Calculation in progress, intermediate result: " << result << std::endl;result *= 1.5; // Scale result 
        {
        }
        return result;
    }
};
```

### Test 2: Replacement and Insertion Using `^n..`

**Source Code**:
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

**Instruction**:
```markdown
### match:
...
void ^3.. >>>f(...) <<< {...}...
### patch
print("[INFO]: ")
```

**Result**:
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


### Test 3: Insertion After Closing Brace

**Source Code**:
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

**Instruction**:
```markdown
### match:
...VerifiedContents::CreateFromFile ^.. { ...
}>>>
...
### patch
_ChromiumImpl
```

**Result**:
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

### Test 4: Replacement and Insertion using `..^`

**Source Code**:
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

**Instruction**:
```markdown
### match:
...
class ..^ {...>>>};...
### patch
print("[INFO]: ")
```

**Result**:
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

## Architecture and Repository Structure

The prototype is written in Python and uses `pytest` for testing. The project structure is as follows:

| File/Directory | Description |
|----------------|-------------|
| `unique3.cpp`, `unique5.cpp`, ... | C++ source files for testing |
| `unique3.md`, `unique5.md`, ... | Markdown files with instructions and patches for testing |
| `test/PassedTests/` | Test files (C++ and Markdown) for successful scenarios |
| `test/FailedTests/` | Test files for error scenarios |
| `constants.py` | Constants such as Hatch operators, supported languages, and extensions |
| `Insert.py` | Logic for inserting and replacing patches in source code |
| `MainCMD.py` | Entry point for the command-line interface |
| `MainTest.py` | Module for automated testing |
| `SearchCode.py` | Logic for searching insertion positions in code |
| `TokenizeCode.py` | Code tokenization with support for Hatch operators |
| `Utilities.py` | Utility functions for file reading/writing and Markdown parsing |
| `CodeComprasion.py ` | The future logic of creating a Match based on the modified code|

## Conclusion

Hatch is an experimental tool for managing Git patches through the Hatch logical language, simplifying and structuring the code modification process. The tool is under active development, and we welcome any suggestions and contributions to the project via [GitHub](https://github.com/Kirillkadr/Hatch).
