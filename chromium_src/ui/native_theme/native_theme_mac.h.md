### match
```
...
 # ifndef ... 
 namespace ui { ... 
// NativeThemeBase:  >>> 
 SkColor GetSystemButtonPressedColor(SkColor base_color) const override;  <<< ... 
void PaintMenuItemBackground(
      cc::PaintCanvas* canvas,
      const ColorProvider* color_provider,
      State state,
      const gfx::Rect& rect,
      const MenuItemExtraParams& extra_params) const override;
 ... } ...  
```
### patch
```
  GetSystemButtonPressedColor_ChromiumImpl(SkColor base_color) const override; \
  virtual SkColor GetSystemButtonPressedColor

```

