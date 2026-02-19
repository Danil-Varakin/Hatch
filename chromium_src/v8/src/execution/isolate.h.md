### match
```
...
 # ifndef ... 
 namespace v8 { ... 
 namespace internal { ... 
using InterruptEntry = std::pair<InterruptCallback, void*>;
 std::queue<InterruptEntry> api_interrupts_queue_; 
 >>> 
#define GLOBAL_BACKING_STORE(type, name, initialvalue) type name##_;

 ... } ...  } ...  
```
### patch
```
  #if BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)
  public:                                                                     \
  void set_page_graph_delegate(                                              \
      v8::page_graph::PageGraphDelegate* page_graph_delegate) {              \
    page_graph_delegate_ = page_graph_delegate;                              \
  }                                                                          \
  v8::page_graph::PageGraphDelegate* page_graph_delegate() const {           \
    return page_graph_delegate_;                                             \
  }                                                                          \
  v8::page_graph::ExecutingScript GetExecutingScript(bool include_position); \
  std::vector<v8::page_graph::ExecutingScript> GetAllExecutingScripts();     \
                                                                             \
 private:                                                                    \
  v8::page_graph::PageGraphDelegate* page_graph_delegate_ = nullptr

#endif  // BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)


```