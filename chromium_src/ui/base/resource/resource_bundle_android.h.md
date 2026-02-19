### match
```
...
 # ifndef ... 
 namespace ui { ... 
 const base::FilePath& disk_file_path 
 ) 
 ; 
 >>> 
 ... } ...  
```
### patch
```
COMPONENT_EXPORT(UI_BASE)
void BraveLoadMainAndroidPackFile(const char* path_within_apk,
                                  const base::FilePath& disk_file_path);


```

