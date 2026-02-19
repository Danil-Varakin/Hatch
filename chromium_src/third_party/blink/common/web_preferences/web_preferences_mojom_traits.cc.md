### match
```
...
// Use of this source code is governed by a BSD-style license that can be
 // found in the LICENSE file. 
 >>> 
#include "third_party/blink/public/common/web_preferences/web_preferences_mojom_traits.h"

 ... 
```
### patch
```
#include "third_party/blink/public/common/web_preferences/web_preferences_mojom_traits.h"

```

### match
```
...
 namespace mojo { ... 
 bool StructTraits<blink::mojom::WebPreferencesDataView,
                  blink::web_pref::WebPreferences>::
    Read(blink::mojom::WebPreferencesDataView data,
         blink::web_pref::WebPreferences* out) { ... 
return true;
 } 
 >>> 
 ... } ...  
```
### patch
```
bool StructTraits<blink::mojom::WebPreferencesDataView,
                  blink::web_pref::WebPreferences>::
    Read(blink::mojom::WebPreferencesDataView data,
         blink::web_pref::WebPreferences* out) {
  if (!StructTraits<blink::mojom::WebPreferencesDataView,
                    blink::web_pref::WebPreferences_ChromiumImpl>::Read(data,
                                                                        out)) {
    return false;
  }
  out->force_cosmetic_filtering = data.force_cosmetic_filtering();
  out->page_in_reader_mode = data.page_in_reader_mode();
  out->is_tor_window = data.is_tor_window();
  out->global_privacy_control_enabled = data.global_privacy_control_enabled();
  return true;
}

```

