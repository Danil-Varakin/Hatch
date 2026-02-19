### match
```
...
 # ifndef ... 
 namespace views { ... 
 class VIEWS_EXPORT DesktopWindowTreeHost { ... 
virtual void ClientDestroyedWidget();
 virtual DesktopNativeCursorManager* GetSingletonDesktopNativeCursorManager(); 
 >>> 
 ... } ...  } ...  
```
### patch
```
   virtual SkColor GetBackgroundColor(SkColor requested_color) const;


```

