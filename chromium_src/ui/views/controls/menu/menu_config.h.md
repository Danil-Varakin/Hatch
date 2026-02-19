### match
```
...
 # ifndef ... 
 namespace views { ... 
 struct VIEWS_EXPORT MenuConfig { ... 
// than 0) is fine.
 static constexpr int kMenuControllerGroupingId = 1001; 
 >>> 
static const MenuConfig& instance();
 ... } ...  } ...  
```
### patch
```
  static const MenuConfig&  instance_ChromiumImpl();
  MenuConfig(const MenuConfig&); 

```

