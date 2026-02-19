### match
```
...
#include "ui/ozone/public/ozone_platform.h"

 #endif 
 >>> 
 ... 
```
### patch
```
#if BUILDFLAG(IS_MAC)
#include "ui/views/widget/native_widget_mac.h"
#endif


```

### match
```
...
 namespace views { ... 
 #if BUILDFLAG(IS_MAC ) ... 
 void Widget::SetActivationIndependence(bool independence) { ... 
if (native_widget_) {
    native_widget_->SetActivationIndependence(independence);
  }
 } 
 >>> 
 ... } ...  
```
### patch
```
namespace views {

void Widget::SetWindowTitleVisibility(bool visible) {
  static_cast<NativeWidgetMac*>(native_widget_private())
      ->SetWindowTitleVisibility(visible);
}

void Widget::ResetWindowControlsPosition() {
  static_cast<NativeWidgetMac*>(native_widget_private())
      ->ResetWindowControlsPosition();
}

void Widget::UpdateWindowTitleColor(SkColor color) {
  static_cast<NativeWidgetMac*>(native_widget_private())
      ->UpdateWindowTitleColor(color);
}

}  // namespace views

```

