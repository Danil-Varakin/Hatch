### match
```
...
 namespace ui { ...   >>> 
 void 
 AddUiColorMixer(ColorProvider* provider, const ColorProviderKey& key) 
 {  <<< ... 
const bool dark_mode = key.color_mode == ColorProviderKey::ColorMode::kDark;
 ... } ...  } ...  
```
### patch
```
void AddUiColorMixer_Chromium(ColorProvider* provider, const ColorProviderKey& key) {

```

### match
```
...
 namespace ui { ... 
 void AddUiColorMixer_Chromium(ColorProvider* provider, const ColorProviderKey& key) { ... 
CompleteDefaultWebNativeRendererColorIdsDefinition(
      mixer, dark_mode,
      key.contrast_mode == ColorProviderKey::ContrastMode::kHigh);
 } 
 >>> 
 ... } ...  
```
### patch
```
// TODO(simonhong): Use nala color if it's available from UI layer.
void AddBraveUiColorMixer(ColorProvider* provider,
                          const ColorProviderKey& key) {
  ColorMixer& mixer = provider->AddMixer();
  const bool dark_mode = key.color_mode == ColorProviderKey::ColorMode::kDark;

  // --------------------------------------------------------------------------
  // Border colors
  // --------------------------------------------------------------------------
  // For deprecated kColorId_FocusedBorderColor
  mixer[kColorFocusableBorderFocused] = {nala::kColorPrimary40};

  // --------------------------------------------------------------------------
  // Button colors
  // --------------------------------------------------------------------------
  // For deprecated kColorId_ProminentButtonColor
  mixer[kColorButtonBackgroundProminent] = {gfx::kColorButtonBackground};
  // For deprecated kColorId_ProminentButtonDisabledColor
  mixer[kColorButtonBackgroundProminentDisabled] = {gfx::kColorButtonDisabled};
  // For deprecated kColorId_ProminentButtonFocusedColor
  mixer[kColorButtonBackgroundProminentFocused] = {gfx::kColorButtonBackground};
  // For deprecated kColorId_ButtonBorderColor
  // TODO(simonhong): Add this color to palette.
  mixer[kColorButtonBorder] = {SkColorSetRGB(0xc3, 0xc4, 0xcf)};
  // For deprecated kColorId_ButtonEnabledColor
  mixer[kColorButtonForeground] = {nala::kColorTextPrimary};
  mixer[kColorRadioButtonForegroundChecked] = {kColorButtonForeground};
  // For deprecated kColorId_TextOnProminentButtonColor
  mixer[kColorButtonForegroundProminent] = {SK_ColorWHITE};

  // --------------------------------------------------------------------------
  // Link colors
  // --------------------------------------------------------------------------
  // For deprecated kColorId_LinkEnabled & kColorId_LinkPressed
  mixer[kColorLinkForeground] = {dark_mode ? gfx::kColorTextInteractiveDark
                                           : gfx::kColorTextInteractive};
  mixer[kColorLinkForegroundPressed] = {kColorLinkForeground};

  // --------------------------------------------------------------------------
  // Checkbox colors
  // --------------------------------------------------------------------------
  mixer[kColorCheckboxForegroundChecked] = {kColorLinkForeground};

  // --------------------------------------------------------------------------
  // Table colors (e.g. Task Manager)
  // --------------------------------------------------------------------------
  // For deprecated kColorId_TableSelectionBackgroundFocused and
  // kColorId_TableSelectionBackgroundUnfocused (which were
  // AlphaBlend(kColorId_ProminentButtonColor, kColorId_WindowBackground,
  // SkAlpha{0x3C}))
  mixer[kColorTableBackgroundSelectedFocused] =
      AlphaBlend(gfx::kColorButtonBackground, kColorPrimaryBackground, 0x3C);
  mixer[kColorTableBackgroundSelectedUnfocused] = {
      kColorTableBackgroundSelectedFocused};
  // For deprecated kColorId_TableGroupingIndicatorColor (which was the same as
  // kColorId_FocusedBorderColor)
  mixer[kColorTableGroupingIndicator] = {gfx::kColorButtonBackground};

  // --------------------------------------------------------------------------
  // Text colors
  // --------------------------------------------------------------------------
  // For deprecated kColorId_TextfieldSelectionBackgroundFocused
  mixer[kColorTextfieldSelectionBackground] = {dark_mode ? gfx::kGoogleBlue800
                                                         : gfx::kGoogleBlue200};
}

void AddUiColorMixer(ColorProvider* provider, const ColorProviderKey& key) {
  AddUiColorMixer_Chromium(provider, key);
  AddBraveUiColorMixer(provider, key);
}

```

