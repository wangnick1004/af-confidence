import {Config} from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);

// 讓 Remotion Studio 在任何瀏覽器（含 Safari）都找得到每個元素在程式碼裡的位置。
// 預設做法是讀瀏覽器的錯誤堆疊，在非 Chrome 瀏覽器可能失敗，導致時間軸只剩一條軌道。
// 這裡改成編譯時就把檔案位置寫進每個元素（只在 Studio 預覽時啟用，不影響輸出影片）。
Config.overrideWebpackConfig((config) => {
  if (config.mode !== 'development') {
    return config;
  }
  const visit = (rule: unknown): void => {
    if (!rule || typeof rule !== 'object') return;
    const r = rule as {loader?: string; options?: Record<string, unknown>; use?: unknown; oneOf?: unknown; rules?: unknown};
    if (typeof r.loader === 'string' && r.loader.includes('esbuild-loader') && r.options) {
      r.options = {...r.options, jsx: 'automatic', jsxDev: true};
    }
    for (const key of ['use', 'oneOf', 'rules'] as const) {
      const v = r[key];
      if (Array.isArray(v)) v.forEach(visit);
    }
  };
  (config.module?.rules ?? []).forEach(visit);
  return config;
});
