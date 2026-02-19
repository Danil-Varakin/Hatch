### match
```
...
 namespace blink { ... 
 void V8ScriptRunner::ReportException(v8::Isolate* isolate,
                                     v8::Local<v8::Value> exception) { ... 
if (IsMainThread())
    V8Initializer::MessageHandlerInMainThread(message, exception);
  else
    V8Initializer::MessageHandlerInWorker(message, exception);
 } 
 >>> 
 ... } ...  
```
### patch
```
// static
v8::MaybeLocal<v8::Script> V8ScriptRunner::CompileScript(
    ScriptState* script_state,
    const ClassicScript& classic_script,
    v8::ScriptOrigin origin,
    v8::ScriptCompiler::CompileOptions compile_options,
    v8::ScriptCompiler::NoCacheReason no_cache_reason,
    bool can_use_crowdsourced_compile_hints) {
  v8::MaybeLocal<v8::Script> result = CompileScript_ChromiumImpl(
      script_state, classic_script, origin, compile_options, no_cache_reason,
      can_use_crowdsourced_compile_hints);
#if BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)
  if (CoreProbeSink::HasAgentsGlobal(CoreProbeSink::kPageGraph)) {
    v8::Local<v8::Script> script;
    if (result.ToLocal(&script)) {
      const auto referrer_info = ReferrerScriptInfo::FromV8HostDefinedOptions(
          v8::Isolate::GetCurrent()->GetCurrentContext(),
          origin.GetHostDefinedOptions(), classic_script.SourceUrl());
      probe::RegisterPageGraphScriptCompilation(
          ExecutionContext::From(script_state), referrer_info, classic_script,
          script);
    }
  }
#endif  // BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)
  return result;
}
// static
v8::MaybeLocal<v8::Module> V8ScriptRunner::CompileModule(
    v8::Isolate* isolate,
    const ModuleScriptCreationParams& params,
    const TextPosition& start_position,
    v8::ScriptCompiler::CompileOptions compile_options,
    v8::ScriptCompiler::NoCacheReason no_cache_reason,
    const ReferrerScriptInfo& referrer_info) {
  v8::MaybeLocal<v8::Module> result = CompileModule_ChromiumImpl(
      isolate, params, start_position, compile_options, no_cache_reason,
      referrer_info);
#if BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)
  if (CoreProbeSink::HasAgentsGlobal(CoreProbeSink::kPageGraph)) {
    v8::Local<v8::Module> module;
    if (result.ToLocal(&module)) {
      probe::RegisterPageGraphModuleCompilation(
          ExecutionContext::From(isolate->GetCurrentContext()), referrer_info,
          params, module);
    }
  }
#endif  // BUILDFLAG(ENABLE_BRAVE_PAGE_GRAPH)
  return result;
}

```

