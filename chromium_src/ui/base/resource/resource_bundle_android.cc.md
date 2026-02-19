### match
```
...
 namespace ui { ... 
 namespace { ... 
 bool LoadLocaleResourcesForLocaleAndGender(
    const std::string& app_locale,
    const ResourceBundle::Gender gender,
    ResourceBundle::FdAndRegion* webview_locale_pack,
    ResourceBundle::FdAndRegion* non_webview_locale_pack,
    std::vector<std::unique_ptr<ResourceHandle>>* locale_resources_data) { ... 
return true;
 } 
 >>> 
 ... } ...  } ...  
```
### patch
```
int g_brave_resources_pack_fd = -1;
base::MemoryMappedFile::Region g_brave_resources_pack_region;

```

### match
```
...
 namespace ui { ... 
 std::vector<ResourceBundle::FdAndRegion> SwapAndroidGlobalsForTesting(
    const std::vector<ResourceBundle::FdAndRegion>& new_locale_packs) { ... 
return std::exchange(GetLocalePaksGlobal(), new_locale_packs);
 } 
 >>> 
 ... } ...  
```
### patch
```
void BraveLoadMainAndroidPackFile(const char* path_within_apk,
                                  const base::FilePath& disk_file_path) {
  if (LoadFromApkOrFile(path_within_apk, &disk_file_path,
                        &g_brave_resources_pack_fd,
                        &g_brave_resources_pack_region)) {
    ResourceBundle::GetSharedInstance().AddDataPackFromFileRegion(
        base::File(g_brave_resources_pack_fd), g_brave_resources_pack_region,
        ui::kScaleFactorNone);
  }
}

```