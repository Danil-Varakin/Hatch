### match
```
...
 namespace ui { ...   >>> 
 SkColor 
 NativeThemeMac::GetSystemButtonPressedColor(SkColor base_color) const 
 {  <<< ... 
// Mac has a different "pressed button" styling because it doesn't use
 ... } ...  } ...  
```
### patch
```
SkColor NativeThemeMac::GetSystemButtonPressedColor_ChromiumImpl(SkColor base_color) const {

```

### match
```
...
 namespace ui { ... 
 void NativeThemeMac::PaintMenuPopupBackground(
    cc::PaintCanvas* canvas,
    const ColorProvider* color_provider,
    const gfx::Size& size,
    const MenuBackgroundExtraParams& extra_params) const { ... 
canvas->drawRoundRect(gfx::RectToSkRect(gfx::Rect(size)), radius, radius,
                        flags);
 } 
 >>> 
 ... } ...  
```
### patch
```
SkColor NativeThemeMac::GetSystemButtonPressedColor(SkColor base_color) const {
  return NativeTheme::GetSystemButtonPressedColor(base_color);
}

```

