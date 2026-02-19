### match
```
...
 # ifndef ... 
#define THIRD_PARTY_BLINK_PUBLIC_COMMON_CLIENT_HINTS_ENABLED_CLIENT_HINTS_H_

 #include <array>
 
 >>> 
#include "services/network/public/mojom/web_client_hints_types.mojom-shared.h"

 ... 
```
### patch
```
#include "services/network/public/mojom/web_client_hints_types.mojom-shared.h"

```

### match
```
...
 # ifndef ... 
 namespace blink { ... 
 class BLINK_COMMON_EXPORT EnabledClientHints { ... 
// Returns false if `type` is not a valid WebClientHintsType value.
 bool IsEnabled(network::mojom::WebClientHintsType type) const; 
 >>> 
// Sets the client hint as enabled for sending in an HTTP request header. Even
 ... } ...  } ...  
```
### patch
```
  void SetIsEnabled_ChromiumImpl(network::mojom::WebClientHintsType type,
                                 bool should_send);

```

