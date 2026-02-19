### match
```
...
 # ifndef ... 
// owned by the same owner of this SimpleMenuModel.  >>> 
 void AddButtonItem(int command_id, ButtonMenuItemModel* model);  <<< ... 
void AddSubMenu(int command_id,
                  const std::u16string& label,
                  MenuModel* model);
 ... 
```
### patch
```
  void AddButtonItemAt(int command_id, ButtonMenuItemModel* model, size_t index);

```

