### match
```
...
 # ifndef ... 
 #define UI_VIEWS_INPUT_EVENT_ACTIVATION_PROTECTOR_H_
 
 >>> 
#include "base/time/time.h"

 ... 
```
### patch
```
#include "ui/views/windows_stationarity_monitor.h"

```

### match
```
...
 # ifndef ... 
 namespace views { ... 
 class VIEWS_EXPORT InputEventActivationProtector
    : WindowsStationarityMonitor::Observer { ... 
// Implements WindowsStationarityMonitor::Observer:  >>> 
 void OnWindowStationaryStateChanged() override;  <<< ... 
// Resets the state for click tracking.
 ... } ...  } ...  
```
### patch
```
  void OnWindowStationaryStateChanged_ChromiumImpl(__VA_ARGS__);
  void IgnoreNextWindowStationaryStateChanged();

 private:
  bool ignore_next_window_stationary_state_changed_ = false;

 public:
  void OnWindowStationaryStateChanged(__VA_ARGS__) override;

```

