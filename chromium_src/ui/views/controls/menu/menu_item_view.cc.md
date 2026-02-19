### match
```
...
#include <string>

 #include <utility>
 
 >>> 
#include "base/auto_reset.h"

 ... 
```
### patch
```
#include "components/vector_icons/vector_icons.h"

```

### match
```
...
 namespace views { ... 
 void MenuItemView::UpdateSelectionBasedState(bool paint_as_selected) { ... 
 if (submenu_arrow_image_view_) { ...   >>> 
 vector_icons::kSubmenuArrowChromeRefreshIcon 
 , 
 colors.icon_color 
 ) 
 ) 
 ;  <<< ... } ...  } ...  } ...  
```
### patch
```
        vector_icons::kSubmenuArrowChromeRefreshIcon, colors.icon_color, 16));
  if (false)
    submenu_arrow_image_view_->SetImage(ui::ImageModel::FromVectorIcon)
        vector_icons::kSubmenuArrowChromeRefreshIcon

```

