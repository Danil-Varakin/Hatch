### match
```cpp
...
 
 namespace printing { ... 
 
 namespace { ... 
>>> 
 } 
 // namespace 
<<< 
FrameReference::FrameReference(blink::WebLocalFrame* frame) {
  Reset(frame);
}
 ... } ... 


```
### patch
```cpp
                         DISABLED_RecentlyClosedTabsFromCurrentSession) {
```
