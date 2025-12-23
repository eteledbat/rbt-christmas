# 🎄 圣诞红黑树

> **语言切换: [English](./README.md) | [한국어](./README_ko.md)**

一个基于**完美平衡红黑树**结构的交互式圣诞树可视化项目。

灵感来源于 EXO 的《初雪》。

### 🖼️ 运行结果示意

![运行结果示意](./preview.png)

### ✨ 项目特性

- **动态物理**: 带有四腿奔跑动画的驯鹿和实时下雪效果。
- **CS 核心**: 节点严格遵守红黑树着色规则 (黑根 -> 红 -> 黑 -> 红)。
- **趣味交互**: 点击树底部的礼物节点，随机获得计算机科学主题的祝福语。

### 🛠️ 个性化定制

#### 1. 修改心愿清单

在 `christmas_rbt.py` 中找到 `WISH_POOL` 列表进行修改：

```python
WISH_POOL = ["你的自定义祝福 1", "你的自定义祝福 2"]
```

#### 2. 更换背景音乐

用你喜欢的 MP3 文件替换根目录下的 music.mp3，并确保文件名保持不变。

### 🚀 生成可执行文件 (.exe)

安装依赖：

```bash
pip install pygame pyinstaller
```

执行打包命令：

```bash
pyinstaller --onefile --noconsole christmas_rbt.py
```

在 dist/ 文件夹下获取程序。注意：运行 .exe 时必须将其与 music.mp3 放在同一目录下。