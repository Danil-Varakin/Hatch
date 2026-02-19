### match
```
...
 # ifndef ... 
 namespace blink { ... 
 class CORE_EXPORT EventListenerMap final { ... 
 void ForAllEventListenerTypes(CallbackType callback) const { ... 
for (const auto& entry : entries_) {
      callback(entry.first, entry.second->size());
    }
 } 
 >>> 
 ... } ...  } ...  
```
### patch
```
  #if BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)
  static bool AddListenerToVector(                          
      EventListenerVector* vector, EventListener* listener,
      const AddEventListenerOptionsResolved* options,
      RegisteredEventListener** registered_listener);

```

### match
```
...
 namespace blink { ... 
 class CORE_EXPORT EventListenerMap final { ... 
 #if BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH ) ... 
static bool AddListenerToVector(                          
		      EventListenerVector* vector, EventListener* listener,
		      const AddEventListenerOptionsResolved* options,
		      RegisteredEventListener** registered_listener);
 void CopyEventListenersNotCreatedFromMarkupToTarget(EventTarget*); 
 >>> 
void Trace(Visitor*) const;
 ... } ...  } ...  
```
### patch
```
  #endif  // BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)

```

