### match
```
...
 # ifndef ... 
 namespace blink { ... 
 class BLINK_EXPORT WebDocument : public WebNode { ... 
bool IsHTMLDocument() const;
 bool IsXHTMLDocument() const; 
 >>> 
bool IsPluginDocument() const;
 ... } ...  } ...  
```
### patch
```
  bool IsDOMFeaturePolicyEnabled(v8::Isolate* isolate,v8::Local<v8::Context> context, const WebString& feature);

```

