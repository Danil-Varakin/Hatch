### match
```
...
 # ifndef ... 
 namespace views { ... 
 class VIEWS_EXPORT DialogDelegate : public WidgetDelegate { ... 
// Reset the dialog's shown timestamp, for tests that are subject to the
 // "unintended interaction" detection mechanism. 
 >>> 
void ResetViewShownTimeStampForTesting();
 ... } ...  } ...  
```
### patch
```
  set_should_ignore_snapping(bool should_ignore_snapping) { \
    should_ignore_snapping_ = should_ignore_snapping;       \
  }                                                         \
  bool should_ignore_snapping() const {                     \
    return should_ignore_snapping_;                         \
  }                                                         \
                                                            \
 private:                                                   \
  bool should_ignore_snapping_ = false;                     \
                                                            \
 public:

```

### match
```
...
 # ifndef ... 
 namespace views { ... 
 class VIEWS_EXPORT DialogDelegate : public WidgetDelegate { ... 
 void ResetViewShownTimeStampForTesting(); 
 >>> 
 ... } ...  } ...  
```
### patch
```
class CrashReportPermissionAskDialogView;
class WindowClosingConfirmDialogView;
class PlaylistActionDialog;
class TextRecognitionDialogView;
class ObsoleteSystemConfirmDialogView;

namespace brave_vpn {
class BraveVpnFallbackDialogView;
class BraveVpnDnsSettingsNotificiationDialogView;
}  // namespace brave_vpn

```

### match
```
...
 # ifndef ... 
 namespace views { ... 
friend class ::webid::AccountSelectionModalView;
 DialogDelegateView(); 
 >>> 
static DdvPassKey CreatePassKey() { return DdvPassKey(); }
 ... } ...  
```
### patch
```
  friend class ::CrashReportPermissionAskDialogView;                  \
  friend class ::WindowClosingConfirmDialogView;                      \
  friend class ::PlaylistActionDialog;                                \
  friend class ::TextRecognitionDialogView;                           \
  friend class ::ObsoleteSystemConfirmDialogView;                     \
  friend class brave_vpn::BraveVpnFallbackDialogView;                 \
  friend class brave_vpn::BraveVpnDnsSettingsNotificiationDialogView; \

```

