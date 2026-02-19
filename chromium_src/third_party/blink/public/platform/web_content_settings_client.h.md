### match
```
...
 # ifndef ... 
#include <memory>

 #include <utility>
 
 >>> 
#include "base/functional/callback.h"

 ... 
```
### patch
```
#include "brave/components/brave_shields/core/common/shields_settings.mojom.h"
#include "components/content_settings/core/common/content_settings_types.h"
#include "third_party/blink/public/platform/web_security_origin.h"

```

### match
```
...
 # ifndef ... 
#include "third_party/blink/public/platform/web_security_origin.h"

 #include "base/functional/callback.h"
 
 >>> 
namespace blink {

class WebURL;

// This class provides the content settings information which tells
// whether each feature is allowed or not.
class WebContentSettingsClient {
 public:
  // Only used if this is a WebContentSettingsClient on a worker thread. Clones
  // this WebContentSettingsClient so it can be used by another worker thread.
  virtual std::unique_ptr<WebContentSettingsClient> Clone() { return nullptr; }

  enum class StorageType {
    kCacheStorage,
    kIndexedDB,
    kFileSystem,
    kWebLocks,
    kLocalStorage,
    kSessionStorage
  };

  // Controls whether access to the given StorageType is allowed for this frame.
  // Runs asynchronously.
  virtual void AllowStorageAccess(StorageType storage_type,
                                  base::OnceCallback<void(bool)> callback) {
    std::move(callback).Run(true);
  }

  // Controls whether access to the given StorageType is allowed for this frame.
  // Blocks until done.
  virtual bool AllowStorageAccessSync(StorageType storage_type) { return true; }

  // Controls whether insecure scripts are allowed to execute for this frame.
  virtual bool AllowRunningInsecureContent(bool enabled_per_settings,
                                           const WebURL&) {
    return enabled_per_settings;
  }

  // Controls whether access to read the clipboard is allowed for this frame.
  virtual bool AllowReadFromClipboard() { return false; }

  // Controls whether access to write the clipboard is allowed for this frame.
  virtual bool AllowWriteToClipboard() { return false; }

  // Reports that passive mixed content was found at the provided URL.
  virtual void PassiveInsecureContentFound(const WebURL&) {}

  // Notifies the client that the frame would have executed script if script
  // were enabled.
  virtual void DidNotAllowScript() {}

  // Notifies the client that the frame would have loaded an image if image were
  // enabled.
  virtual void DidNotAllowImage() {}

  // Controls whether mixed content autoupgrades should be allowed in this
  // frame.
  virtual bool ShouldAutoupgradeMixedContent() { return true; }

  virtual ~WebContentSettingsClient() = default;
};

}
 ... 
```
### patch
```
class GURL;

```

### match
```
...
 # ifndef ... 
 namespace blink { ... 
 class WebContentSettingsClient { ... 
// Controls whether access to the given StorageType is allowed for this frame.
 // Blocks until done. 
 >>> 
virtual bool AllowStorageAccessSync(StorageType storage_type) { return true; }
 ... } ...  } ...  
```
### patch
```
  virtual bool AllowAutoplay(bool play_requested) {                                      \
    return true;                                                            \
  }                                                                         \
  virtual bool IsCosmeticFilteringEnabled(const GURL& url) {                \
    return false;                                                           \
  }                                                                         \
  virtual bool IsFirstPartyCosmeticFilteringEnabled(const GURL& url) {      \
    return false;                                                           \
  }                                                                         \
  virtual brave_shields::mojom::ShieldsSettingsPtr GetBraveShieldsSettings( \
      ContentSettingsType webcompat_settings_type) {                        \
    return brave_shields::mojom::ShieldsSettingsPtr();                      \
  }                                                                         \
  virtual bool IsReduceLanguageEnabled() {                                  \
    return false;                                                           \
  }                                                                         \
  virtual blink::WebSecurityOrigin GetEphemeralStorageOriginSync() {        \
    return blink::WebSecurityOrigin();                                      \
  }                                                                         \
  virtual bool HasContentSettingsRules() const {                            \
    return false;                                                           \
  }                                                                         \
  virtual bool AllowScript(bool enabled_per_settings) {                     \
    return enabled_per_settings;                                            \
  }                                                                         \
  virtual bool AllowScriptFromSource(bool enabled_per_settings,             \
                                     const blink::WebURL& script_url) {     \
    return enabled_per_settings;                                            \
  }                                                                         \

```

