# Blender 工作台

用于 IDN®理想营养双 11 视频「购物车日记」（主题 2）的 3D 部分。

## 文件夹

- `给Codex/`：发给 Codex 的需求（`需求说明.md`）和参考图。
- `Codex产出/`：Codex 做好的立牌设计放这里。

## 正在使用的工程文件（暂时没有搬过来）

- Blender 工程：`/Users/kummerspeck/Documents/ChatGPT/IDN官号内容/outputs/blender/双11-购物车日记.blend`
- 贴图：同目录下 `textures/`
- 进度交接：`/Users/kummerspeck/Documents/ChatGPT/IDN官号内容/docs/handoff.md`

工程里的贴图用的是绝对路径，整体搬家前要先在 Blender 里把路径改成相对路径（文件 → 外部数据 → 设为相对路径），否则贴图会丢。

## 当前立牌交接（2026-10-19）

Punk 已选 F 版：蓝字细黄边、中英文字、轻度复古油墨做旧。接入素材和说明在 `Codex产出/F_Claude接入素材_v1/给Claude_先读我.md`；运行素材也已复制到原工程 `textures/codex_checkout_F_v1/`。先让 Claude 试装并渲静帧。收银线复用原 `LineDash_0`–`LineDash_8`，附专用深蓝哑光材质脚本，无需新增虚线图片。A/B及旧独立模型均为历史方案。原视频工程未修改。
