### match
```
...
 # ifndef ... 
 namespace views { ... 
 class VIEWS_EXPORT LayoutProvider { ... 
// given type of content. |leading| is the type (text or control) of the first
 // element in the content  and |trailing| is the type of the final element. 
 >>> 
gfx::Insets GetDialogInsetsForContentType(DialogContentType leading,
                                            DialogContentType trailing) const;
 ... } ...  } ...  
```
### patch
```
  virtual int GetCornerRadiusMetric(ShapeContextTokensOverride token) const;

```

### match
```
...
 # ifndef ... 
 namespace views { ... 
 class VIEWS_EXPORT LayoutProvider { ... 
private:
  TypographyProvider typography_provider_;
 } 
 ; 
 >>> 
 ... } ...  
```
### patch
```
// An enum type to provide an override path for kOmniboxExpandedRadius to be
// mapped to ShapeSysTokens::kMedium. This is used by
// `RoundedOmniboxResultsFrame`.
enum class ShapeContextTokensOverride {
  kOmniboxExpandedRadius,
  kRoundedCornersBorderRadius,
  kRoundedCornersBorderRadiusAtWindowCorner,
};

```

