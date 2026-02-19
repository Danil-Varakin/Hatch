### match
```
...
#include "ui/views/layout/layout_provider.h"

 #include <algorithm>
 
 >>> 
#include "base/containers/fixed_flat_map.h"

 ... 
```
### patch
```
#include "ui/views/layout/layout_provider.h"

```

### match
```
...
 namespace views { ... 
 int LayoutProvider::GetShadowElevationMetric(Emphasis emphasis) const { ... 
switch (emphasis) {
    case Emphasis::kNone:
      return 0;
    case Emphasis::kLow:
      return 1;
    case Emphasis::kMedium:
      return 2;
    case Emphasis::kHigh:
      return 3;
    case Emphasis::kMaximum:
      return 16;
  }
 } 
 >>> 
 ... } ...  
```
### patch
```
int LayoutProvider::GetCornerRadiusMetric(ShapeContextTokensOverride id) const {
  switch (id) {
    case ShapeContextTokensOverride::kOmniboxExpandedRadius:
      return 4;
    case ShapeContextTokensOverride::kRoundedCornersBorderRadius:
      return 4;
    case ShapeContextTokensOverride::kRoundedCornersBorderRadiusAtWindowCorner:
      return 4;
    default:
      break;
  }
  NOTREACHED();
}

```

