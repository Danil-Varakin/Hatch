### match
```
...
// found in the LICENSE file.
 #include "third_party/blink/renderer/core/css/media_values_dynamic.h"
 
 >>> 
#include "third_party/blink/public/common/css/forced_colors.h"

 ... 
```
### patch
```
#include "third_party/blink/renderer/core/css/media_values_dynamic.h"

```

### match
```
...
 namespace blink { ... 
 int MediaValuesDynamic::DeviceWidth() const { ...   >>> 
 return CalculateDeviceWidth(frame_);  <<< ... } ...  } ...  
```
### patch
```
  return CalculateDeviceWidth(__VA_ARGS__, /* early = */ false);

```

### match
```
...
 namespace blink { ... 
 int MediaValuesDynamic::DeviceHeight() const { ...   >>> 
 return CalculateDeviceHeight(frame_);  <<< ... } ...  } ...  
```
### patch
```
  return CalculateDeviceHeight(__VA_ARGS__, /* early = */ false);

```

