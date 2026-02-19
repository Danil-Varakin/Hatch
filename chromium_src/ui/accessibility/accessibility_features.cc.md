### match
```
...
 namespace features { ... 
 #if !BUILDFLAG(IS_ANDROID ) ...   >>> 
 bool 
 IsScreenAIMainContentExtractionEnabled() 
 {  <<< ... 
return base::FeatureList::IsEnabled(
      ax::mojom::features::kScreenAIMainContentExtractionEnabled);
 ... } ...  } ...  
```
### patch
```
bool IsScreenAIMainContentExtractionEnabled_ChromiumImpl() {

```

### match
```
...
 namespace features { ... 
 #if !BUILDFLAG(IS_ANDROID ) ...   >>> 
 bool 
 IsScreenAIOCREnabled() 
 {  <<< ... 
return base::FeatureList::IsEnabled(ax::mojom::features::kScreenAIOCREnabled);
 ... } ...  } ...  
```
### patch
```
bool IsScreenAIOCREnabled_ChromiumImpl() {

```

### match
```
...
 namespace features { ... 
bool IsWasmTtsEngineAutoInstallDisabled() {
  return base::FeatureList::IsEnabled(
      ::features::kWasmTtsEngineAutoInstallDisabled);
}
 #endif 
 // BUILDFLAG(IS_WIN) || BUILDFLAG(IS_MAC) || BUILDFLAG(IS_LINUX) 
 >>> 
 ... } ...  
```
### patch
```
bool IsScreenAIMainContentExtractionEnabled() {
  return false;
}

bool IsScreenAIOCREnabled() {
  return false;
}

```

