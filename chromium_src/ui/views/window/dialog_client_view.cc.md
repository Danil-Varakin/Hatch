### match
```
...
 namespace views { ... 
 namespace { ... 
// conflict with other groups that could be in the dialog content.
 constexpr int kButtonGroup = 6666; 
 >>> 
// Returns true if the given view should be shown (i.e. exists and is
 ... ) ...  } ...  } ...  
```
### patch
```
constexpr int kVerticalButtonsSpacing = 8;

```

### match
```
...
 void DialogClientView::RemoveFillerView(size_t view_index) { ... 
if (filler) {
    button_row_container_->RemoveChildViewT(filler);
    filler = nullptr;
  }
 } 
 >>> 
 ... 
```
### patch
```
void DialogClientView::SetupButtonsLayoutVertically() {
  button_row_container_->SetLayoutManager(std::make_unique<views::BoxLayout>(
      views::BoxLayout::Orientation::kVertical, button_row_insets_,
      kVerticalButtonsSpacing));
}
void DialogClientView::IgnoreNextWindowStationaryStateChanged() {
  DCHECK(input_protector_);
  input_protector_->IgnoreNextWindowStationaryStateChanged();
}

```

