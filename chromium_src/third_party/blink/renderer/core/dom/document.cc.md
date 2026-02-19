### match
```
...
>>>
 void 
 Document::ProcessJavaScriptUrl 
 ( 
 const KURL& url 
 ,  <<< ... 
const DOMWrapperWorld* world
 ... ) ...
```
### patch
```
void Document::ProcessJavaScriptUrl_ChromiumImpl(const KURL& url,
```

### match
```
...
 namespace blink { ... 
bool operator==(const RegisteredEventListener& lhs,
                const RegisteredEventListener& rhs) {
  DCHECK(lhs.Callback());
  DCHECK(rhs.Callback());
  return lhs.Callback()->Matches(*rhs.Callback()) &&
         lhs.Capture() == rhs.Capture();
}
 } 
 // namespace blink 
 >>> 
 ... 
```
### patch
```
#if BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)

namespace blink {

// static
int RegisteredEventListener::GenerateId() {
  static base::AtomicSequenceNumber id_sequence;
  return id_sequence.GetNext();
}

}  // namespace blink
#endif  // BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)

```

