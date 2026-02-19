### match
```
...
 namespace blink { ...   >>> 
 bool 
 LocalFontFaceSource::IsLocalFontAvailable 
 (  <<< ... 
const FontDescription& font_description
 ... ) ...  } ...  
```
### patch
```
bool LocalFontFaceSource::IsLocalFontAvailable_ChromiumImpl(

```

### match
```
...
 namespace blink { ... 
 bool LocalFontFaceSource::IsValid() const { ...   >>> 
 return IsLoading() || IsLocalFontAvailable(FontDescription());  <<< ... } ...  } ...  
```
### patch
```
  return IsLoading() || IsLocalFontAvailable_ChromiumImpl(FontDescription());

```

### match
```
...
 namespace blink { ... 
 void LocalFontFaceSource::Trace(Visitor* visitor) const { ... 
CSSFontFaceSource::Trace(visitor);
 } 
 >>> 
 ... } ...  
```
### patch
```
bool LocalFontFaceSource::IsLocalFontAvailable(
    const FontDescription& font_description) const {
  if (!brave::AllowFontFamily(font_selector_->GetExecutionContext(),
                              font_name_)) {
    return false;
  }
  return IsLocalFontAvailable_ChromiumImpl(font_description);
}

```

