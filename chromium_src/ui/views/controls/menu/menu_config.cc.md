### match
```
...
// found in the LICENSE file.
 #include "ui/views/controls/menu/menu_config.h"
 
 >>> 
#include "base/debug/dump_without_crashing.h"

 ... 
```
### patch
```
#include "ui/views/controls/menu/menu_config.h"
#include "ui/views/controls/menu/menu_controller.h"

```

### match
```
...
 namespace views { ...   >>> 
 const 
 MenuConfig 
 & MenuConfig::instance() 
 { 
 static base::NoDestructor<MenuConfig> instance; 
 return *instance;  <<< ... } ...  } ...  
```
### patch
```
const MenuConfig& MenuConfig::instance_ChromiumImpl() {
  static base::NoDestructor<MenuConfig> instance_ChromiumImpl;
  return *instance_ChromiumImpl;

```

### match
```
...
 namespace views { ... 
 const MenuConfig& MenuConfig::instance_ChromiumImpl() { ... 
return *instance_ChromiumImpl;
 } 
 >>> 
 ... } ...  
```
### patch
```
MenuConfig::MenuConfig(const MenuConfig&) = default;
// static
const MenuConfig& MenuConfig::instance() {
  const auto& config = instance_ChromiumImpl();
  static class RunOnce {
   public:
    RunOnce(const MenuConfig& config) {
      auto& mutable_config = const_cast<MenuConfig&>(config);
      // Each platform sets its own config in its Init().
      // Apply our config globally at once after Init() is done.
      mutable_config.item_horizontal_border_padding = 4;
      mutable_config.item_horizontal_padding =
          24 - config.item_horizontal_border_padding;
      mutable_config.corner_radius = 8;
      mutable_config.use_bubble_border = true;
    }
  } const run_once(config);

  return config;
}

```

