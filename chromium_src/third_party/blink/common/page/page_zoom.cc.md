### match
```
...
 namespace blink { ...   >>> 
 static 
 constexpr 
 double 
 kPresetBrowserZoomFactorsArray[] 
 = 
 {  <<< ... 
0.25
 ... } ...  } ...  
```
### patch
```
static constexpr double kPresetBrowserZoomFactorsArray_ChromiumImpl[] = {

```

### match
```
...
 namespace blink { ... 
static constexpr double kPresetBrowserZoomFactorsArray_ChromiumImpl[] = {
	0.25, 1 / 3.0, 0.5,  2 / 3.0, 0.75, 0.8, 0.9, 1.0, 1.1,
    1.25, 1.5,     1.75, 2.0,     2.5,  3.0, 4.0, 5.0};  >>> 
 const base::span<const double> kPresetBrowserZoomFactors(
    kPresetBrowserZoomFactorsArray);  <<< ... 
#if !BUILDFLAG(IS_ANDROID)
// The minimum and maximum amount of page zoom that is possible, independent
// of other factors such as device scale and page scale (pinch). Historically,
// these values came from WebKitLegacy/mac/WebView/WebView.mm where they are
// named MinimumZoomMultiplier and MaximumZoomMultiplier. But chromium has
// changed to use different limits.
const double kMinimumBrowserZoomFactor = 0.25;
const double kMaximumBrowserZoomFactor = 5.0;
#else
// On Android, the OS-level font size is considered when calculating zoom
// factor. At the OS-level, we support a range of 85% - 200%, and at the
// browser-level we support 50% - 300%. The max we support is therefore: 3.0 * 2
// = 6.0, and the min is 0.5 * .85 = .425 (depending on settings).
const double kMinimumBrowserZoomFactor = 0.425;
const double kMaximumBrowserZoomFactor = 6.0;
#endif
 ... } ...  
```
### patch
```
const base::span<const double> kPresetBrowserZoomFactors_ChromiumImpl(
    kPresetBrowserZoomFactorsArray_ChromiumImpl);

```

### match
```
...
 namespace blink { ... 
 bool ZoomValuesEqual(double value_a, double value_b) { ... 
return (std::fabs(value_a - value_b) <= kPageZoomEpsilon);
 } 
 >>> 
 ... } ...  
```
### patch
```
static constexpr double kPresetBrowserZoomFactorsArray[] = {
    0.25,    1 / 3.0, 0.5, 2 / 3.0, 0.75, 0.8, 0.9, 1.0, 1.1, 1.25,
    4 / 3.0, 7 / 5.0, 1.5, 1.75,    2.0,  2.5, 3.0, 4.0, 5.0};
const base::span<const double> kPresetBrowserZoomFactors(
    kPresetBrowserZoomFactorsArray);

```

