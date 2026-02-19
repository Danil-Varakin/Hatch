### match
```
...
 namespace ui { ... 
 void SimpleMenuModel::ValidateItem(const Item& item) { ... 
// DCHECK_IS_ON()
 } 
 >>> 
 ... } ...  
```
### patch
```
void SimpleMenuModel::AddButtonItemAt(int command_id,
                                      ButtonMenuItemModel* model,
                                      size_t index) {
  Item item(command_id, TYPE_BUTTON_ITEM, std::u16string());
  item.button_model = model;
  InsertItemAtIndex(std::move(item), index);
}

```

