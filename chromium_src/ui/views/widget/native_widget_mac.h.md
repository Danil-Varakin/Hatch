### match
```
...
 # ifndef ... 
#include <memory>

 #include <string>
 
 >>> 
#include "base/callback_list.h"

 ... 
```
### patch
```
#include <optional>
#include "ui/views/widget/native_widget_private.h"

```

### match
```
...
 # ifndef ... 
 namespace views { ... 
void GetWindowPlacement(
      gfx::Rect* bounds,
      ui::mojom::WindowShowState* show_state) const override;
 bool SetWindowTitle(const std::u16string& title) override; 
 >>> 
void SetWindowIcons(const gfx::ImageSkia& window_icon,
                      const gfx::ImageSkia& app_icon) override;
 ... } ...  
```
### patch
```
  void SetWindowTitleVisibility(bool visible);                   \
  bool has_overridden_window_title_visibility() const {     \
    return overridden_window_title_visibility_.has_value(); \
  }                                                         \
  bool GetOverriddenWindowTitleVisibility() const;          \
  void ResetWindowControlsPosition();                       \
  void UpdateWindowTitleColor(SkColor color);               \
                                                            \
 private:                                                   \
  std::optional<bool> overridden_window_title_visibility_;  \
                                                            \
 public:                                                    \

```

