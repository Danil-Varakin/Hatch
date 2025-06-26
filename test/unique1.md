### match:
```
...
int main() {
...
std::vector<int> values
...
>>>
std::cout << "Processing values"
...
```

### patch
```
std::clog << "Initializing vector processing: " << values.size() << std::endl;
```