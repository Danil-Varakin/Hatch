### match
```
...
// Use of this source code is governed by a BSD-style license that can be
 // found in the LICENSE file. 
 >>> 
#include "ui/webui/webui_util.h"

 ...  

```
### patch
```
#include "ui/webui/webui_util.h"

```

### match
```
...
#include "ui/webui/webui_util.h"

 #include "ui/webui/webui_util.h"
 
 >>> 
#include <string>
```
### patch
```
  #include "base/no_destructor.h"
#include "base/strings/strcat.h"
#include "content/public/common/url_constants.h"

```
### match
```
...
>>>
 namespace 
 webui 
 { 
 >>> 
void SetJSModuleDefaults(content::WebUIDataSource* source) {
  std::string scheme =
      base::StartsWith(source->GetSource(), content::kChromeUIUntrustedScheme)
          ? content::kChromeUIUntrustedScheme
          : content::kChromeUIScheme;
  // Set the default src to 'self' only. Generally necessary overrides are set
  // below. Additional overrides should generally be added for individual
  // data sources only.
  source->OverrideContentSecurityPolicy(
      network::mojom::CSPDirectiveName::DefaultSrc, "default-src 'self';");
  // Allow connecting to chrome://resources for trusted UIs and images from
  // chrome://image, chrome://theme, chrome://favicon2, chrome://resources and
  // data URLs.
  // TODO: Both of these are needed by only a smaller subset of UIs. Should
  // the overrides be moved to those UIs only?
  if (scheme == content::kChromeUIScheme) {
    source->OverrideContentSecurityPolicy(
        network::mojom::CSPDirectiveName::ConnectSrc,
        "connect-src chrome://webui-test chrome://resources chrome://theme "
        "'self';");
    source->OverrideContentSecurityPolicy(
        network::mojom::CSPDirectiveName::ImgSrc,
        "img-src chrome://resources chrome://theme chrome://image "
        "chrome://favicon2 chrome://app-icon chrome://extension-icon "
        "chrome://fileicon "
#if BUILDFLAG(IS_CHROMEOS)
        "chrome://chromeos-asset chrome://userimage "
#endif
        "blob: data: 'self';");
  }

  // webui-test is required for tests. Scripts from //resources are allowed
  // for all UIs.
  source->OverrideContentSecurityPolicy(
      network::mojom::CSPDirectiveName::ScriptSrc,
      base::StringPrintf("script-src %s://resources %s://webui-test 'self';",
                         scheme.c_str(), scheme.c_str()));
  // Allow loading fonts from //resources.
  source->OverrideContentSecurityPolicy(
      network::mojom::CSPDirectiveName::FontSrc,
      base::StringPrintf("font-src %s://resources 'self';", scheme.c_str()));
  // unsafe-inline is required for Polymer. Allow styles to be imported from
  // //resources and //theme.
  source->OverrideContentSecurityPolicy(
      network::mojom::CSPDirectiveName::StyleSrc,
      base::StringPrintf(
          "style-src %s://resources %s://theme 'self' 'unsafe-inline';",
          scheme.c_str(), scheme.c_str()));

  source->UseStringsJs();
  source->EnableReplaceI18nInJS();
  source->AddResourcePath("test_loader.js", IDR_WEBUI_JS_TEST_LOADER_JS);
  source->AddResourcePath("test_loader_util.js",
                          IDR_WEBUI_JS_TEST_LOADER_UTIL_JS);
  source->AddResourcePath("test_loader.html", IDR_WEBUI_TEST_LOADER_HTML);
}
 ... } ...   
```
### patch
```
namespace {
// A chrome-untrusted data source's name starts with chrome-untrusted://.
bool IsChromeUntrustedDataSource(content::WebUIDataSource* source) {
  static const base::NoDestructor<std::string> kChromeUntrustedSourceNamePrefix(
      base::StrCat(
          {content::kChromeUIUntrustedScheme, url::kStandardSchemeSeparator}));

  return source->GetSource().starts_with(*kChromeUntrustedSourceNamePrefix);
}

constexpr char kBraveCSP[] =
    "script-src chrome://resources chrome://webui-test "
    "'self';";

constexpr char kBraveUntrustedCSP[] =
    "script-src chrome-untrusted://resources "
    "'self';";
}  // namespace

```


