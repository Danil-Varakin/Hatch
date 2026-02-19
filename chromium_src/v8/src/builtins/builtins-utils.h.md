### match
```
>>>
...
```

### patch

```
#include "brave/components/brave_page_graph/common/buildflags.h"
```
### match
```
...
namespace v8 {
...
namespace internal {
...
>>>
}
...
}
...
```

### patch

```
#if BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH_WEBAPI_PROBES)

consteval bool IsBuiltinTrackedInPageGraph(std::string_view name) {
  constexpr std::string_view kBuiltinsToTrack[] = {
      "Console",
      "Date",
      "Json",
  };
  for (std::string_view builtin_to_track : kBuiltinsToTrack) {
    // Check if |name| starts with |builtin_to_track|.
    if (name.starts_with(builtin_to_track)) {
      return true;
    }
  }
  return false;
}

// Replace BUILTIN macro with a similar one, but with Page Graph-tracking call.
#if !defined(BUILTIN)
static_assert(false, "BUILTIN macro is expected to be defined");
#endif
#undef BUILTIN
#define BUILTIN(name)                                                      
  V8_WARN_UNUSED_RESULT static Tagged<Object> Builtin_Impl_##name(         
      BuiltinArguments args, Isolate* isolate);                            
                                                                           
  V8_WARN_UNUSED_RESULT Address Builtin_##name(                            
      int args_length, Address* args_object, Isolate* isolate) {           
    DCHECK(isolate->context().is_null() || IsContext(isolate->context())); 
    BuiltinArguments args(args_length, args_object);                       
    Tagged<Object> result(Builtin_Impl_##name(args, isolate));             
    if (V8_UNLIKELY(IsBuiltinTrackedInPageGraph(#name)) &&                 
        V8_UNLIKELY(isolate->page_graph_delegate())) {                     
      ReportBuiltinCallAndResponse(isolate, #name, args, result);          
    }                                                                      
    return BUILTIN_CONVERT_RESULT(result);                                 
  }                                                                        
                                                                           
  V8_WARN_UNUSED_RESULT static Tagged<Object> Builtin_Impl_##name(         
      BuiltinArguments args, Isolate* isolate)

#endif  // BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH_WEBAPI_PROBES)
```

