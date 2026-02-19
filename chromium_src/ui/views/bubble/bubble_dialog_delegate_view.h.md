### match
```
...
#include "ui/base/cocoa/bubble_closer.h"

 #endif 
 >>> 
 ... 
```
### patch
```
class BraveNewsBubbleView;
class BraveHelpBubbleDelegateView;
class SplitViewMenuBubble;
class WaybackMachineBubbleView;
class SidebarItemAddedFeedbackBubble;
class SidebarEditItemBubbleDelegateView;
class SidebarAddItemBubbleDelegateView;

```

### match
```
...
 # ifndef ... 
 namespace ambient_signin { ... 
 } 
 >>> 
 ... 
```
### patch
```
namespace playlist {
class PlaylistBubbleView;
}  // namespace playlist

```

### match
```
...
 # ifndef ... 
 namespace 
 views 
 { 
 >>> 
class AnchorTestBubbleDialogDelegateView
 ... } ...  
```
### patch
```
class BraveBubbleDialogDelegateView;

```

### match
```
...
 # ifndef ... 
 bool autosize = false 
 ) 
 ; 
 >>> 
static BddvPassKey CreatePassKey() { return BddvPassKey(); }
 ... 
```
### patch
```
  friend class ::BraveNewsBubbleView;
  friend class ::BraveHelpBubbleDelegateView;
  friend class ::WaybackMachineBubbleView;
  friend class ::playlist::PlaylistBubbleView;
  friend class ::SplitViewMenuBubble;
  friend class ::SidebarItemAddedFeedbackBubble;
  friend class ::SidebarEditItemBubbleDelegateView;
  friend class ::SidebarAddItemBubbleDelegateView;
  friend class ::views::BraveBubbleDialogDelegateView; 

```

