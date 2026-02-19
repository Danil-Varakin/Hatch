### match
```
...
#include "ui/wm/core/window_util.h"

 #include "ui/wm/public/activation_client.h"
 
 >>> 
#if BUILDFLAG(IS_WIN)
#include "ui/base/win/shell.h"
#include "ui/gfx/win/hwnd_util.h"
#include "ui/views/widget/desktop_aura/desktop_native_cursor_manager_win.h"
#endif
 ... 
```
### patch
```
#include "ui/compositor/compositor.h"

#if BUILDFLAG(IS_WIN)
// This header includes shobjidl.h which also defines SetBackgroundColor in
// Windows SDK 10.0.26100.0
#include "ui/gfx/win/hwnd_util.h"

```

