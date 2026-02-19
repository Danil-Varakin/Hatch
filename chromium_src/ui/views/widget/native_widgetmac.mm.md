### match
```
...
>>>
```
### patch
```
#include "base/check.h"
```

### match
```
...
namespace views {
...
>>>
}
```
### patch
```
 void NativeWidgetMac::SetWindowTitleVisibility(bool visible) {
  if (overridden_window_title_visibility_.has_value() &&
      visible == *overridden_window_title_visibility_) {
    return;
  }

  GetNSWindowMojo()->SetWindowTitleVisibility(visible);
  overridden_window_title_visibility_ = visible;
}

void NativeWidgetMac::UpdateWindowTitleColor(SkColor color) {
  GetNSWindowMojo()->UpdateWindowTitleColor(color);
}

bool NativeWidgetMac::GetOverriddenWindowTitleVisibility() const {
  DCHECK(has_overridden_window_title_visibility())
      << "Didn't call SetWindowTitleVisibility(). Use "
         "WidgetDelegate::ShouldShowWindowTitle() instead.";
  return *overridden_window_title_visibility_;
}

void NativeWidgetMac::ResetWindowControlsPosition() {
  GetNSWindowMojo()->ResetWindowControlsPosition();
}                         \

```

