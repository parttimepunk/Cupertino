# Cupertino

IDN®理想营养双 11 短视频「购物车日记」的 Blender 制作内容快照。

## 目录

- `Blender/`：给 Codex 的需求说明、参考图，以及 Codex 交付的收银台立牌方案（F 版为当前采用版本）。
- `blender-project/`：Blender 工程与产出。
  - `双11-购物车日记.blend`：主工程（镜 1–5，帧 1–510，30fps，1080×1920）。
  - `*_备份.blend`：修改前的备份版本。
  - `textures/`：D3K2 标签、收银台立牌等贴图。
  - `audio/`：镜 1–5 的音效与配乐（程序合成）。
  - `*.mp4` / `*.png`：测试视频、预览和静帧。

## 注意

工程里的贴图使用的是原电脑上的绝对路径（`/Users/kummerspeck/Documents/ChatGPT/IDN官号内容/outputs/blender/textures/`）。在其他位置打开时，需要在 Blender 里用「文件 → 外部数据 → 查找缺失文件」指向本仓库的 `blender-project/textures/`。
