

### match
```
...
 (void)mainScreenChanged { ... 
 namespace { ...   >>> 
 auto* window_scene = base::apple::ObjCCastStrict<UIWindowScene>(scene) 
 ;  <<< ... } ...  } ... 

```

### patch

```
print("[INFO]: ")
```

