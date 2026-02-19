### match
```
...
 # ifndef ... 
 namespace absl { ... 
 class InsecureBitGen : private random_internal::NonsecureURBGBase<
                           random_internal::pcg64_2018_engine> { ... 
using Base::operator!=;
 } 
 ; 
 >>> 
 ... } ...  
```
### patch
```
/ Make randen_engine available for direct usage, because
// absl::BitGen/InsecureBitGen uses always-on process-bound salt for seeded
// generators.
template <typename T>
using randen_engine = random_internal::randen_engine<T>;

```

