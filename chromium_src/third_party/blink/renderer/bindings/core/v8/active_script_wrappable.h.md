### match
```
...
 # ifndef ... 
#include "third_party/blink/renderer/core/execution_context/execution_context.h"

 #include "third_party/blink/renderer/platform/bindings/active_script_wrappable_base.h"
 
 >>> 
namespace blink {

// Derived by wrappable objects which need to remain alive due to ongoing
// asynchronous activity, even if they are not referenced in the JavaScript or
// Blink heap.
//
// This can be useful for ScriptWrappable objects that are not held alive by
// regular references from the object graph. E.g., XMLHttpRequest may have a
// pending activity that may be visible (e.g. firing event listeners or
// resolving promises) and should thus not be collected.
//
// Alternatively, it is generally less error prone though to attach the
// wrappable object to the regular Blink heap. ActiveScriptWrappable negatively
// affects garbage collection performance and is thus preferred to keep objects
// alive through other means, e.g. normal Member<> pointers. When not easily
// feasibly, a new ActiveScriptWrappable should be allow-listed in
// ActiveScriptWrappableCreationKey as a friend.
//
// The objects should derive from ActiveScriptWrappable<T>, and override
// `ActiveScriptWrappableBase::HasPendingActivity()`. The method is not allowed
// to allocate.
//
// Caveat:
// - To avoid leaking objects after the context is destroyed, users of
//   ActiveScriptWrappable<T> also have to provide a `GetExecutionContext()`
//   method that returns the ExecutionContext or nullptr. A nullptr or already
//   destroyed context results in ignoring `HasPendingActivity()`.
//
// Automatically activates the ASW behavior after construction. For lazy
// initialization, see LazyActiveScriptWrappable below.
template <typename T>
class ActiveScriptWrappable : public ActiveScriptWrappableBase {
 public:
  ActiveScriptWrappable(const ActiveScriptWrappable&) = delete;
  ActiveScriptWrappable& operator=(const ActiveScriptWrappable&) = delete;

  ~ActiveScriptWrappable() override = default;

  // See trait below.
  void ActiveScriptWrappableBaseConstructed() {
    if (auto* context = static_cast<const T*>(this)->GetExecutionContext()) {
      RegisterActiveScriptWrappable();
    }
  }

 protected:
  explicit ActiveScriptWrappable(ActiveScriptWrappableCreationKey) {}

  bool IsContextDestroyed() const final {
    return IsContextDestroyedForActiveScriptWrappable(
        static_cast<const T*>(this)->GetExecutionContext());
  }
};

// Same as ActiveScriptWrappable with the difference the the object is not
// automatically activated. Instead, child classes need to use
// `RegisterActiveScriptWrappable()` to activate the
// ASW behavior.
template <typename T>
class LazyActiveScriptWrappable : public ActiveScriptWrappableBase {
 public:
  LazyActiveScriptWrappable(const LazyActiveScriptWrappable&) = delete;
  LazyActiveScriptWrappable& operator=(const LazyActiveScriptWrappable&) =
      delete;

  ~LazyActiveScriptWrappable() override = default;

  // Registers the ASW, activating it.
  void RegisterActiveScriptWrappable() {
    ActiveScriptWrappableBase::RegisterActiveScriptWrappable();
  }

  bool IsContextDestroyed() const final {
    return IsContextDestroyedForActiveScriptWrappable(
        static_cast<const T*>(this)->GetExecutionContext());
  }

 protected:
  explicit LazyActiveScriptWrappable(ActiveScriptWrappableCreationKey) {}
};

// Helper for ActiveScriptWrappable<T>::IsContextDestroyed();
CORE_EXPORT bool IsContextDestroyedForActiveScriptWrappable(
    const ExecutionContext* execution_context);

}
 ... 
```
### patch
```
#if BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)
#include "third_party/blink/renderer/core/core_export.h"
#include "third_party/blink/renderer/platform/bindings/active_script_wrappable_base.h"


```

### match
```
...
 #if BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH ) ... 
 namespace cppgc { ... 
<typename T, typename Unused>  >>> 
 struct PostConstructionCallbackTrait 
 ;  <<< ... } ...  
```
### patch
```
struct PostConstructionCallbackTrait_ChromiumImpl;

```

### match
```
...
 #if BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH ) ... 
 namespace cppgc { ...   >>> 
 struct 
 PostConstructionCallbackTrait 
 <  <<< ... 
T
 ... } ...  
```
### patch
```
struct PostConstructionCallbackTrait_ChromiumImpl<

```

### match
```
...
 #if BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH ) ... 
 namespace cppgc { ... 
template <typename T>
struct PostConstructionCallbackTrait_ChromiumImpl<
	T,
    std::void_t<
        decltype(std::declval<T>().ActiveScriptWrappableBaseConstructed())>> {
  static void Call(T* object) {
    static_assert(std::is_base_of<blink::ActiveScriptWrappableBase, T>::value,
                  "Only ActiveScriptWrappableBase should use the "
                  "post-construction hook.");
    // Registering the ActiveScriptWrappableBase after construction means that
    // the garbage collector does not need to deal with objects that are
    // currently under construction. This is important as checking whether ASW
    // should be treated as active involves calling virtual functions which may
    // not work during construction. The objects in construction are kept alive
    // via conservative stack scanning.
    object->ActiveScriptWrappableBaseConstructed();
  }
};
 } 
 // namespace cppgc 
 >>> 
 ... 
```
### patch
```
#if BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)
namespace blink {
class Node;
}  // namespace blink
namespace cppgc {

template <typename T, typename>
struct PostConstructionCallbackTrait;

template <class, class = void>
struct HasActiveScriptWrappableBaseConstructed : std::false_type {};

template <class T>
struct HasActiveScriptWrappableBaseConstructed<
    T,
    std::void_t<
        decltype(std::declval<T>().ActiveScriptWrappableBaseConstructed())>>
    : std::true_type {};

// Allow PostConstructionCallback to work with Node types.
template <typename T>
struct PostConstructionCallbackTrait<
    T,
    typename std::enable_if<HasActiveScriptWrappableBaseConstructed<T>::value &&
                                !std::is_base_of<blink::Node, T>::value,
                            void>::type> {
  static void Call(T* object) {
    PostConstructionCallbackTrait_ChromiumImpl<T, void>::Call(object);
  }
};

}  // namespace cppgc
#endif  // BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)

```

