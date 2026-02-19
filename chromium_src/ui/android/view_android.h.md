### match
```
...
 # ifndef ... 
 namespace ui { ... 
 class UI_ANDROID_EXPORT ViewAndroid { ... 
friend class WindowAndroid;  >>> 
 bool OnDragEvent(const DragEventAndroid& event);  <<< ... 
bool OnTouchEvent(const MotionEventAndroid& event);
 ... } ...  } ...  
```
### patch
```
  Unused() {
    return false;
  }
  friend class speedreader::SpeedreaderTabHelper;
  bool OnDragEvent

```

### match
```
...
 # ifndef ... 
 namespace ui { ... 
;
 } 
 // namespace ui 
 >>> 
 ... 
```
### patch
```
namespace speedreader {
class SpeedreaderTabHelper;
}

```

