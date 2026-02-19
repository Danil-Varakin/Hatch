### match
```
...
 namespace blink { ...   >>> 
 void 
 EnabledClientHints::SetIsEnabled 
 ( 
 const WebClientHintsType type 
 ,  <<< ... 
const bool should_send
 ... ) ...  } ...  
```
### patch
```
void EnabledClientHints::SetIsEnabled_ChromiumImpl(const WebClientHintsType type,

```

### match
```
...
 namespace blink { ... 
 std::vector<WebClientHintsType> EnabledClientHints::GetEnabledHints() const { ... 
return hints;
 } 
 >>> 
 ... } ...  
```
### patch
```
void EnabledClientHints::SetIsEnabled(const WebClientHintsType type,
                                      const bool should_send) {
  bool type_is_enabled = false;
  switch (type) {
    case WebClientHintsType::kUA:
    case WebClientHintsType::kUAArch:
    case WebClientHintsType::kUABitness:
    case WebClientHintsType::kUAFullVersionList:
    case WebClientHintsType::kUAMobile:
    case WebClientHintsType::kUAModel:
    case WebClientHintsType::kUAPlatform:
    case WebClientHintsType::kUAPlatformVersion:
    case WebClientHintsType::kUAWoW64:
      type_is_enabled = true;
      break;
    default:
      break;
  }
  if (type_is_enabled) {
    SetIsEnabled_ChromiumImpl(type, should_send);
  } else {
    enabled_types_[static_cast<int>(type)] = false;
  }
}

```

