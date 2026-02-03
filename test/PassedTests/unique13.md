
строки 263- 266
### match
```
...
 class BraveSearchTestEnabled : public BraveSearchTest  
 { ... 
 BraveSearchTestEnabled()  
 { ... 
 feature_list_.InitAndEnableFeatureWithParameters  
 ( ... 
  >>> 
 { 
 {brave_search::features::kBraveSearchDefaultAPIDailyLimitName, "3"} 
 ,  
 <<< ... 
{brave_search::features::kBraveSearchDefaultAPITotalLimitName, "10"}
 ...  ) ... } ... } ... 
```

### patch


```
print("[INFO]: ")
```

