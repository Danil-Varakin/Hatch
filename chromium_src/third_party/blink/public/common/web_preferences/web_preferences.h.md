### match
```
...
 # ifndef ... 
#include "url/gurl.h"

 #include "url/origin.h"
 
 >>> 
namespace blink {

namespace web_pref {
...
}  // namespace web_pref

}
 ... 
```
### patch
```
#define WebPreferences WebPreferences_ChromiumImpl

```

### match
```
...
 # ifndef ... 
 namespace blink { ... 
 namespace web_pref { ... 
 struct BLINK_COMMON_EXPORT WebPreferences { ... 
WebPreferences& operator=(WebPreferences&& other);
 } 
 ; 
 >>> 
 ... } ...  } ...  
```
### patch
```
struct BLINK_COMMON_EXPORT WebPreferences : public WebPreferences_ChromiumImpl {
  using WebPreferences_ChromiumImpl::WebPreferences_ChromiumImpl;

  WebPreferences(const WebPreferences& other);
  WebPreferences(WebPreferences&& other);
  ~WebPreferences();
  WebPreferences& operator=(const WebPreferences& other);
  WebPreferences& operator=(WebPreferences&& other);

  bool force_cosmetic_filtering = false;
  bool page_in_reader_mode = false;
  bool is_tor_window = false;
  bool global_privacy_control_enabled = true;
};

```

