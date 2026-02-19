### match
```
...
 # ifndef ... 
#include "ui/views/style/typography.h"

 #include "ui/views/view.h"
 
 >>> 
namespace views {
...
}
 ... } ...  
```
### patch
```
class CustomStyledLabel;

```

### match
```
...
>>>
 std::unique_ptr<Label> 
 CreateLabel 
 (  <<< ... 
const std::u16string& text
 ... ) ...  
```
### patch
```

  friend class ::CustomStyledLabel;                                        \
  virtual std::unique_ptr<views::Label> CreateLabel(

```

