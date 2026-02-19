### match
```
...
 namespace blink { ... 
 namespace origin_trials { ... 
 >>> 
 ... } ...  } ...
```
### patch
```
BLINK_COMMON_EXPORT bool IsTrialDisabledInBrave(std::string_view trial_name);
BLINK_COMMON_EXPORT bool IsTrialDisabledInBrave(
    blink::mojom::OriginTrialFeature feature);

```


