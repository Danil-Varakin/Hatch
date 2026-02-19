### match
```
...
// found in the LICENSE file.
 #include "third_party/blink/renderer/bindings/core/v8/js_event_handler_for_content_attribute.h"
 
 >>> 
#include "third_party/blink/renderer/bindings/core/v8/script_controller.h"

 ... 
```
### patch
```
#include "brave/components/brave_page_graph/common/buildflags.h"
#include "third_party/blink/renderer/core/probe/core_probes.h"

```

### match
```
...
 namespace blink { ... 
 v8::Local<v8::Value> JSEventHandlerForContentAttribute::GetCompiledHandler(
    EventTarget& event_target) { ... 
compiled_function->SetName(V8String(isolate, function_name_));  >>> 
 SetCompiledHandler(script_state_of_event_target, compiled_function);  <<< ... 
return JSEventHandler::GetListenerObject(event_target);
 ... } ...  } ...  
```
### patch
```
  SetCompiledHandler(SCRIPT_STATE, FUNCTION);
  IF_BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH, {
    probe::RegisterPageGraphScriptCompilationFromAttr(
        &event_target, function_name_, script_body_, compiled_function);
  });

```

