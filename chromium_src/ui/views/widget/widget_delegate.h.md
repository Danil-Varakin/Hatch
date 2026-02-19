### match
```
...
 # ifndef ... 
 namespace views { ... 
 class VIEWS_EXPORT WidgetDelegate { ... 
 bool has_desired_bounds_delegate() const { ... 
return static_cast<bool>(params_.desired_bounds_delegate);
 } 
 >>> 
 ... } ...  } ...  
```
### patch
```
  gfx::Point get_desired_position() {                               
    return desired_position_delegate_.Run();                        
  }                                                                 
  bool has_desired_position_delegate() const {                      
    return static_cast<bool>(desired_position_delegate_);           
  }                                                                 
  void set_desired_position_delegate(                               
      base::RepeatingCallback<gfx::Point()> delegate) {             
    desired_position_delegate_ = std::move(delegate);               
  }                                                                 
  base::WeakPtr<WidgetDelegate> GetWeakPtr() {                      
    return weak_ptr_factory_.GetWeakPtr();                          
  }                                                                 
                                                                    
 private:                                                           
  base::RepeatingCallback<gfx::Point()> desired_position_delegate_;
                                                                    
 public:                                                            

```

### match
```
...
 # ifndef ... 
FRIEND_TEST_ALL_PREFIXES(test::WidgetOwnsNativeWidgetTest,
                           WidgetDelegateView);
 WidgetDelegateView(); 
 >>> 
static WdvPassKey CreatePassKey() { return WdvPassKey(); }
 ... 
```
### patch
```
  friend class ::brave_ads::NotificationAdPopup;     
  friend class ::brave_tooltips::BraveTooltipPopup;
  friend class ::MenuButtonDelegate;
  friend class ::VerticalTabStripWidgetDelegateView;

```

### match
```
...
 # ifndef ... 
 DEFINE_VIEW_BUILDER(VIEWS_EXPORT, WidgetDelegateView) 
 >>> 
 ... 
```
### patch
```
namespace brave_ads {
class NotificationAdPopup;
}  // namespace brave_ads
namespace brave_tooltips {
class BraveTooltipPopup;
}  // namespace brave_tooltips
class MenuButtonDelegate;
class VerticalTabStripWidgetDelegateView;

```

