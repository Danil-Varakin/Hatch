### match
```
...
 namespace blink { ... 
 namespace features { ... 
 BASE_FEATURE ( ... 
base::FEATURE_DISABLED_BY_DEFAULT
 ) 
 ; 
 >>> 
 ... } ...  } ...  
```
### patch
```
OVERRIDE_FEATURE_DEFAULT_STATES({{
    {kAIProofreadingAPI, base::FEATURE_DISABLED_BY_DEFAULT},
    {kAIPromptAPI, base::FEATURE_DISABLED_BY_DEFAULT},
    {kAIPromptAPIMultimodalInput, base::FEATURE_DISABLED_BY_DEFAULT},
    {kAIRewriterAPI, base::FEATURE_DISABLED_BY_DEFAULT},
    {kAISummarizationAPI, base::FEATURE_DISABLED_BY_DEFAULT},
    {kAIWriterAPI, base::FEATURE_DISABLED_BY_DEFAULT},
    {kLanguageDetectionAPI, base::FEATURE_DISABLED_BY_DEFAULT},
    {kTranslationAPI, base::FEATURE_DISABLED_BY_DEFAULT},
    {kUserMediaElement, base::FEATURE_DISABLED_BY_DEFAULT},
}});
```

