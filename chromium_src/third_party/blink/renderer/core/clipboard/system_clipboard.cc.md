### match
```
...
#include "third_party/blink/renderer/core/clipboard/system_clipboard.h"

 #include <variant>
 
 >>> 
#include "base/memory/scoped_refptr.h"

 ... 
```
### patch
```
#include "third_party/blink/renderer/core/clipboard/system_clipboard.h"
#include "base/check.h"

```

### match
```
...
 namespace blink { ... 
 ScopedSystemClipboardSnapshot::~ScopedSystemClipboardSnapshot() { ... 
clipboard_.DropSnapshot();
 } 
 >>> 
 ... } ...  
```
### patch
```
void SystemClipboard::SanitizeOnNextWriteText() {
  DCHECK(!snapshot_);
  if (!clipboard_.is_bound()) {
    return;
  }
  clipboard_->SanitizeOnNextWriteText();
}

```

