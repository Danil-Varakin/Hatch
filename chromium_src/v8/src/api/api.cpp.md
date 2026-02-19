### match
```
>>>
...
```

### patch

```
#include "brave/v8/include/v8-isolate-page-graph-utils.h"
```
### match
```
...
>>>
```

### patch

```
#if BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)

namespace v8::page_graph {

ExecutingScript GetExecutingScript(Isolate* isolate, bool include_position) {
  i::Isolate* internal_isolate = reinterpret_cast<i::Isolate*>(isolate);
  return internal_isolate->GetExecutingScript(include_position);
}

std::vector<ExecutingScript> GetAllExecutingScripts(Isolate* isolate) {
  i::Isolate* internal_isolate = reinterpret_cast<i::Isolate*>(isolate);
  return internal_isolate->GetAllExecutingScripts();
}

void SetPageGraphDelegate(Isolate* isolate,
                          PageGraphDelegate* page_graph_delegate) {
  i::Isolate* internal_isolate = reinterpret_cast<i::Isolate*>(isolate);
  internal_isolate->set_page_graph_delegate(page_graph_delegate);
}

}  // namespace v8::page_graph
```