### match
```
...
 namespace blink { ...   >>> 
 int 
 MediaValues::CalculateDeviceWidth(LocalFrame* frame) 
 {  <<< ... 
DCHECK(frame && frame->View() && frame->GetSettings() && frame->GetPage());
 ... } ...  } ...  
```
### patch
```
int MediaValues::CalculateDeviceWidth(__VA_ARGS__, bool early) {
    ExecutionContext* context = frame->DomWindow()->GetExecutionContext();
    auto* top_frame = DynamicTo<LocalFrame>(frame->Top());
    return top_frame && brave::BlockScreenFingerprinting(context, early)
               ? brave::FarbleInteger(context,
                                      brave::FarbleKey::kWindowInnerWidth,
                                      CalculateViewportWidth(top_frame), 0, 8)
               : CalculateDeviceWidth_ChromiumImpl(frame);
  }
  int MediaValues::CalculateDeviceWidth_ChromiumImpl(__VA_ARGS__) {

```

### match
```
...
 namespace blink { ...   >>> 
 int 
 MediaValues::CalculateDeviceHeight(LocalFrame* frame) 
 {  <<< ... 
DCHECK(frame && frame->View() && frame->GetSettings() && frame->GetPage());
 ... } ...  } ...  
```
### patch
```
int MediaValues::CalculateDeviceHeight(__VA_ARGS__, bool early) {                         \
    ExecutionContext* context = frame->DomWindow()->GetExecutionContext(); \
    auto* top_frame = DynamicTo<LocalFrame>(frame->Top());                 \
    return top_frame && brave::BlockScreenFingerprinting(context, early)   \
               ? brave::FarbleInteger(                                     \
                     context, brave::FarbleKey::kWindowInnerHeight,        \
                     CalculateViewportHeight(top_frame), 0, 8)             \
               : CalculateDeviceHeight_ChromiumImpl(frame);                \
  }                                                                        \
  int MediaValues::CalculateDeviceHeight_ChromiumImpl(__VA_ARGS__) {

```

