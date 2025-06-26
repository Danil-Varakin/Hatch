### match:
```
...
void compute_sum(...) {
...
int total = 0;
...
>>>
for (int i = 0; i < n; i++)
...
```

### patch
```
total += 10; // Add offset before loop
std::cout << "Starting sum computation with offset: " << total << std::endl;
```