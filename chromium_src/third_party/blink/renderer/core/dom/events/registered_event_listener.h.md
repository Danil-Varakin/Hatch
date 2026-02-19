### match
```
...
#include "third_party/blink/renderer/core/dom/events/event.h"

 #include "third_party/blink/renderer/core/dom/events/event_listener.h"
 
 >>> 
namespace blink {

RegisteredEventListener::RegisteredEventListener()
    : use_capture_(false),
      passive_(false),
      once_(false),
      blocked_event_warning_emitted_(false),
      passive_forced_for_document_target_(false),
      passive_specified_(false),
      removed_(false),
      animation_trigger_(false) {}

RegisteredEventListener::RegisteredEventListener(
    EventListener* listener,
    const AddEventListenerOptionsResolved* options)
    : callback_(listener),
      use_capture_(options->capture()),
      passive_(options->passive()),
      once_(options->once()),
      blocked_event_warning_emitted_(false),
      passive_forced_for_document_target_(
          options->PassiveForcedForDocumentTarget()),
      passive_specified_(options->PassiveSpecified()),
      removed_(false),
      animation_trigger_(options->IsAnimationTrigger()) {}

void RegisteredEventListener::Trace(Visitor* visitor) const {
  visitor->Trace(callback_);
}

AddEventListenerOptionsResolved* RegisteredEventListener::Options() const {
  auto* result = MakeGarbageCollected<AddEventListenerOptionsResolved>();
  result->setCapture(use_capture_);
  result->setPassive(passive_);
  result->SetPassiveForcedForDocumentTarget(
      passive_forced_for_document_target_);
  result->setOnce(once_);
  result->SetPassiveSpecified(passive_specified_);
  result->SetAnimationTrigger(animation_trigger_);
  return result;
}

void RegisteredEventListener::SetCallback(EventListener* listener) {
  callback_ = listener;
}

bool RegisteredEventListener::Matches(const EventListener* listener,
                                      const OptionsForMatching& options) const {
  // Equality is soley based on the listener and useCapture flags.
  DCHECK(callback_);
  DCHECK(listener);
  return callback_->Matches(*listener) && options == GetOptionsForMatching();
}

bool RegisteredEventListener::ShouldFire(const Event& event) const {
  if (event.FireOnlyCaptureListenersAtTarget()) {
    DCHECK_EQ(event.eventPhase(), Event::PhaseType::kAtTarget);
    return Capture();
  }
  if (event.FireOnlyNonCaptureListenersAtTarget()) {
    DCHECK_EQ(event.eventPhase(), Event::PhaseType::kAtTarget);
    return !Capture();
  }
  if (event.eventPhase() == Event::PhaseType::kCapturingPhase)
    return Capture();
  if (event.eventPhase() == Event::PhaseType::kBubblingPhase)
    return !Capture();
  return true;
}

bool operator==(const RegisteredEventListener& lhs,
                const RegisteredEventListener& rhs) {
  DCHECK(lhs.Callback());
  DCHECK(rhs.Callback());
  return lhs.Callback()->Matches(*rhs.Callback()) &&
         lhs.Capture() == rhs.Capture();
}

}
 ... 
```
### patch
```
#if BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)
#include "base/atomic_sequence_num.h"
#endif  // BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)

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

