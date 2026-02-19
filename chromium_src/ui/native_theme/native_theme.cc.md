### match
```
...
// found in the LICENSE file.
 #include "ui/native_theme/native_theme.h"
 
 >>> 
#include <stddef.h>

 ... 
```
### patch
```
#include "ui/gfx/color_palette.h"
#include "ui/gfx/color_utils.h"

```

### match
```
...
 namespace ui { ...   >>> 
 SkColor 
 NativeTheme::GetSystemButtonPressedColor(SkColor base_color) const 
 {  <<< ... 
return base_color;
 ... } ...  } ...  
```
### patch
```
SkColor NativeTheme::GetSystemButtonPressedColor_ChromiumImpl(SkColor base_color) const {

```

### match
```
...
 namespace ui { ... 
 NativeTheme::PreferredContrast NativeTheme::CalculatePreferredContrast() const { ... 
return IsForcedHighContrast() ? PreferredContrast::kMore
                                : OsSettingsProvider::Get().PreferredContrast();
 } 
 >>> 
 ... } ...  
```
### patch
```
SkColor NativeTheme::GetSystemButtonPressedColor(SkColor base_color) const {
  bool is_dark = (preferred_color_scheme() == PreferredColorScheme::kDark);
  return color_utils::GetResultingPaintColor(
      SkColorSetA(gfx::kColorButtonBackground, is_dark ? 0x2b : 0x23),
      base_color);
}

```

