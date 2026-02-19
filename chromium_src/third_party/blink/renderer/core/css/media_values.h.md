### match
```
...
 # ifndef ... 
 namespace blink { ... 
static float CalculateLineHeight(LocalFrame*);  >>> 
 static int CalculateDeviceWidth(LocalFrame*); 
 static int CalculateDeviceHeight(LocalFrame*);  <<< ... 
static bool CalculateStrictMode(LocalFrame*);
 ... } ...  
```
### patch
```
  static int CalculateDeviceWidth(__VA_ARGS__, bool);
  static int CalculateDeviceWidth_ChromiumImpl(__VA_ARGS__);
  static int CalculateDeviceHeight(__VA_ARGS__, bool);
  static int CalculateDeviceHeight_ChromiumImpl(__VA_ARGS__);

```

