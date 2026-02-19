### match
```
...
#include "third_party/blink/renderer/platform/wtf/threading.h"

 #endif 
 >>> 
 ... 
```
### patch
```
#if BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)
#include "third_party/blink/renderer/core/probe/core_probes.h"
#endif  // BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)

```

### match
```
...
 namespace blink { ... 
 void EventListenerMap::Trace(Visitor* visitor) const { ... 
visitor->Trace(entries_);
 } 
 >>> 
 ... } ...  
```
### patch
```

#if BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)
// static
bool EventListenerMap::AddListenerToVector(
    EventListenerVector* vector,
    EventListener* listener,
    const AddEventListenerOptionsResolved* options,
    RegisteredEventListener** registered_listener) {
  const bool result = ::blink::AddListenerToVector(vector, listener, options,
                                                   registered_listener);
  if (result && CoreProbeSink::HasAgentsGlobal(CoreProbeSink::kPageGraph)) {
    DCHECK(registered_listener);
    DCHECK(*registered_listener);
    DCHECK(vector && !vector->empty());
    DCHECK(*registered_listener == vector->back());
    const int id = RegisteredEventListener::GenerateId();
    // Set id to the returned object.
    (*registered_listener)->SetId(id);
    // Set id to the vector-stored object (it's a copy).
    vector->back()->SetId(id);
  }
  return result;
}
#endif  // BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)

```

