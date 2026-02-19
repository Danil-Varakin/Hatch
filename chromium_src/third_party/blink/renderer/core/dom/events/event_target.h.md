### match
```
...
 # ifndef ... 
 namespace blink { ... 
 class CORE_EXPORT EventTarget : public ScriptWrappable { ... 
// javascript originated calls. This method will validate and may adjust
 // the Event object before dispatching. 
 >>> 
bool dispatchEventForBindings(Event*, ExceptionState&);
 ... } ...  } ...  
```
### patch
```
  bool SetAttributeEventListener_ChromiumImpl(const AtomicString& event_type, 
                                              EventListener*);

```

