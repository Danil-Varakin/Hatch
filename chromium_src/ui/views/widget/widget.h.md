### match
```
...
 # ifndef ... 
#include <utility>

 #include <vector>
 
 >>> 
#include "base/callback_list.h"

 ... 
```
### patch
```
#include "build/build_config.h"

```

### match
```
...
 # ifndef ... 
 namespace views { ... 
// Undoes LockPaintAsActive(). This should never be called outside of
 // PaintAsActiveLock destructor. 
 >>> 
void UnlockPaintAsActive();
 ... } ...  
```
### patch
```
  SetWindowTitleVisibility(bool visible);
  void ResetWindowControlsPosition();
  void UpdateWindowTitleColor(SkColor color);

```

