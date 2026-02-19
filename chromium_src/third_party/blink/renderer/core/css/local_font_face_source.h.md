### match
```
...
 # ifndef ... 
#include "third_party/blink/renderer/core/css/css_font_face_source.h"

 #include "third_party/blink/renderer/platform/heap/member.h"
 
 >>> 
#include "third_party/blink/renderer/platform/wtf/allocator/allocator.h"

 ... 
```
### patch
```
#include "third_party/blink/renderer/core/css/css_font_face_source.h"

```

### match
```
...
 # ifndef ... 
 namespace blink { ... 
// 8 where the font lookup map needs to be built first.
 bool IsLocalNonBlocking() const override; 
 >>> 
bool IsLocalFontAvailable(const FontDescription&) const override;
 ... } ...  
```
### patch
```
  bool IsLocalFontAvailable_ChromiumImpl(const FontDescription&) const; 

```

