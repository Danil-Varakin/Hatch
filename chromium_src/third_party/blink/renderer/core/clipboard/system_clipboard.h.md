### match
```
...
 # ifndef ... 
#include <memory>

 #include <optional>
 
 >>> 
#include "build/build_config.h"

 ... 
```
### patch
```
#include "third_party/blink/public/mojom/clipboard/clipboard.mojom-blink.h"

```

### match
```
...
 # ifndef ... 
 namespace blink { ... 
// the OS clipboard.  >>> 
 void CommitWrite();  <<< ... 
void CopyToFindPboard(const String& text);
 ... } ...  
```
### patch
```
  void CommitWrite()
  void SanitizeOnNextWriteText;

```

