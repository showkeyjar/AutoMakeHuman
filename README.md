# AutoMakeHuman

## English

### Overview

AutoMakeHuman is a MakeHuman plugin bundle for fitting a 3D human body or pose to a reference image.

This repository currently contains two plugins:

- `7_auto_human_body`: adjusts body-related MakeHuman modifiers to better match a target silhouette
- `7_auto_human_pose`: adjusts a BVH pose to better match a target pose image

### What Was Modernized

The original project depended heavily on the author's local machine layout and older Python/OpenCV behavior. The current version has been upgraded so it is more practical to install and use today:

- plugin data paths are resolved relative to each plugin directory
- required data folders are created automatically
- OpenCV contour handling works with both OpenCV 3 and OpenCV 4
- several Python 3 incompatibilities were fixed, including `rU`, float slicing, and `dict_values` indexing
- image-processing utilities can be tested outside MakeHuman
- installation is scriptable on Windows, Linux, and macOS

### Requirements

- Python 3.9 or newer
- MakeHuman with plugin support
- Python dependencies from `requirements.txt`

Install dependencies:

```bash
pip install -r requirements.txt
```

### Install

Recommended: use the provided installer and point it to your MakeHuman `plugins` directory.

Cross-platform:

```bash
python bin/install.py --target /path/to/makehuman/plugins
```

Windows PowerShell:

```powershell
.\bin\install.ps1 -Target "D:\MakeHuman\makehuman\plugins"
```

Linux/macOS:

```bash
bin/install.sh /path/to/makehuman/plugins
```

If `MAKEHUMAN_PLUGIN_DIR` is already set, the install scripts can use it directly.

### Plugin Data

Each plugin reads and writes its own data under its package directory:

- `src/7_auto_human_body/data`
- `src/7_auto_human_pose/data`

Important bundled assets:

- body reference image: `src/7_auto_human_body/data/MyAutoData/picture.jpg` or `picture.png`
- pose reference image: `src/7_auto_human_pose/data/MyAutoData/picture.png`
- BVH pose files: `src/7_auto_human_pose/data/MyAutoData/*.bvh`

### Usage

1. Install the plugins into the MakeHuman `plugins` directory.
2. Start or restart MakeHuman.
3. Open the `Utilities` category.
4. Use `AutoBody` to adjust body shape against a reference silhouette.
5. Use `AutoPose` to load or refine pose matching with the bundled BVH workflow.

### Development

Basic validation:

```bash
python -m unittest discover -s test -p "test_*.py"
```

Optional debug windows for contour comparison:

```bash
AUTO_MAKEHUMAN_DEBUG_WINDOWS=1
```

### Known Limits

- the pose plugin still contains a large amount of legacy search logic and repeated UI callback code
- the fitting strategy is still heuristic and not yet ML-based
- end-to-end validation still requires a real MakeHuman runtime

## 中文

### 项目简介

AutoMakeHuman 是一组用于 MakeHuman 的插件，目标是根据一张参考图片，自动拟合三维人体的体型或姿态。

当前仓库包含两个插件：

- `7_auto_human_body`：通过调节 MakeHuman 的体型参数，让模型轮廓更接近目标图片
- `7_auto_human_pose`：通过调整 BVH 姿态数据，让模型姿态更接近目标图片

### 已完成的现代化升级

原始项目强依赖作者本地目录结构，并且使用了较老版本的 Python 和 OpenCV 写法。当前版本已经做了第一轮可用性升级：

- 插件数据路径改为基于插件目录自动解析
- 运行所需的数据目录会自动创建
- 轮廓处理同时兼容 OpenCV 3 和 OpenCV 4
- 修复了多处 Python 3 兼容性问题，例如 `rU`、浮点切片、`dict_values` 下标访问
- 图像处理模块可以在 MakeHuman 外单独测试
- 安装流程支持 Windows、Linux 和 macOS

### 环境要求

- Python 3.9 及以上
- 支持插件的 MakeHuman
- `requirements.txt` 中列出的 Python 依赖

安装依赖：

```bash
pip install -r requirements.txt
```

### 安装方法

推荐使用仓库自带安装脚本，并将目标路径指向 MakeHuman 的 `plugins` 目录。

跨平台通用方式：

```bash
python bin/install.py --target /path/to/makehuman/plugins
```

Windows PowerShell：

```powershell
.\bin\install.ps1 -Target "D:\MakeHuman\makehuman\plugins"
```

Linux/macOS：

```bash
bin/install.sh /path/to/makehuman/plugins
```

如果你已经设置了 `MAKEHUMAN_PLUGIN_DIR` 环境变量，安装脚本也可以直接使用它。

### 数据目录

两个插件都会在各自目录下读写数据：

- `src/7_auto_human_body/data`
- `src/7_auto_human_pose/data`

仓库中已包含的重要示例资源：

- 体型参考图：`src/7_auto_human_body/data/MyAutoData/picture.jpg` 或 `picture.png`
- 姿态参考图：`src/7_auto_human_pose/data/MyAutoData/picture.png`
- BVH 姿态文件：`src/7_auto_human_pose/data/MyAutoData/*.bvh`

### 使用说明

1. 将插件安装到 MakeHuman 的 `plugins` 目录
2. 启动或重启 MakeHuman
3. 打开 `Utilities` 分类
4. 在 `AutoBody` 中根据目标轮廓调整体型
5. 在 `AutoPose` 中加载或微调基于 BVH 的姿态匹配流程

### 开发与验证

基础验证命令：

```bash
python -m unittest discover -s test -p "test_*.py"
```

如果需要查看轮廓对比调试窗口，可以设置：

```bash
AUTO_MAKEHUMAN_DEBUG_WINDOWS=1
```

### 当前限制

- `pose` 插件内部仍保留较多历史搜索逻辑和重复的界面回调代码
- 当前自动拟合策略仍以启发式方法为主，还不是机器学习方案
- 完整的端到端验证仍然需要真实的 MakeHuman 运行环境
