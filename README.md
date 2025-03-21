# 扫描线效果生成器

这个项目实现了一个视频扫描线效果，当扫描线移动时，扫描过的区域显示静止图像，未扫描的区域显示动态视频。这种效果可以用于创建有趣的视觉展示、教学演示或艺术创作。

![扫描线效果示例](https://github.com/wangqiqi/interesting_assets/raw/main/images/effect.jpg)

## 功能特点

- **多方向扫描**：支持从左到右、从右到左、从上到下、从下到上四个方向的扫描
- **可定制外观**：可调节扫描线的速度、颜色和宽度
- **多种输入源**：支持从摄像头或视频文件输入
- **高级视觉效果**：
  - 多种效果类型：基本效果、霓虹效果、矩阵效果、故障效果、彩虹效果
  - 渐变过渡：使扫描线周围区域呈现平滑渐变
  - 多线条效果：同时显示多条平行扫描线
  - 动画效果：脉冲、彩虹、闪烁等动态效果
- **交互控制**：通过键盘控制暂停/继续、重置扫描线、保存图片等操作
- **图像翻转**：可选择水平翻转图像，使摄像头捕获的图像方向与实际动作方向一致

![高级效果示例](https://github.com/wangqiqi/interesting_assets/raw/main/images/effect.jpg)

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

最简单的方式是运行启动脚本，它提供了一个交互式菜单：

```bash
python run.py
```

## 使用方法

### 基本扫描线效果

```bash
python src/scan_effect.py [--video VIDEO_PATH] [--direction {left_to_right,right_to_left,top_to_bottom,bottom_to_top}] [--speed SPEED] [--line_width LINE_WIDTH] [--line_color LINE_COLOR] [--flip]
```

参数说明：
- `--video`: 视频文件路径，默认使用摄像头
- `--direction`: 扫描方向，可选值：left_to_right, right_to_left, top_to_bottom, bottom_to_top，默认为left_to_right
- `--speed`: 扫描速度，默认为2（像素/帧）
- `--line_width`: 扫描线宽度，默认为3像素
- `--line_color`: 扫描线颜色，格式为"R,G,B"，默认为"0,255,0"（绿色）
- `--flip`: 水平翻转图像（适用于摄像头）

### 高级扫描线效果

```bash
python src/advanced_scan_effect.py [--video VIDEO_PATH] [--direction {left_to_right,right_to_left,top_to_bottom,bottom_to_top}] [--speed SPEED] [--line_width LINE_WIDTH] [--line_color LINE_COLOR] [--effect {basic,neon,matrix,glitch,rainbow}] [--gradient] [--blur] [--multi_line MULTI_LINE] [--line_spacing LINE_SPACING] [--animation {none,pulse,rainbow,blink}] [--flip]
```

额外参数说明：
- `--effect`: 效果类型，可选值：basic, neon, matrix, glitch, rainbow，默认为basic
- `--gradient`: 启用渐变效果
- `--blur`: 启用模糊效果
- `--multi_line`: 多线条数量，默认为1
- `--line_spacing`: 多线条间距（像素），默认为50
- `--animation`: 动画类型，可选值：none, pulse, rainbow, blink，默认为none

### 演示脚本

```bash
# 基本演示
python src/demo.py

# 高级演示
python src/advanced_demo.py
```

## 控制键

- `ESC`: 退出程序
- `空格`: 暂停/继续
- `r`: 重置扫描线位置
- `s`: 保存当前帧为图片
- `f`: 切换图像翻转（适用于摄像头）

## 项目结构

```
scan-effect/
├── README.md               # 项目说明文档
├── requirements.txt        # 项目依赖文件
├── run.py                  # 启动脚本
├── blog.md                 # 项目博客文章
└── src/                    # 源代码目录
    ├── scan_effect.py      # 基本扫描线效果实现
    ├── demo.py             # 基本扫描线效果演示
    ├── advanced_scan_effect.py  # 高级扫描线效果实现
    └── advanced_demo.py    # 高级扫描线效果演示
```

## 技术原理

扫描线效果的基本原理是：
1. 捕获视频帧
2. 根据扫描线位置，将当前帧分为两部分
3. 扫描线之前的区域显示静态帧（之前捕获的帧）
4. 扫描线之后的区域显示当前帧
5. 随着扫描线移动，不断更新静态帧的内容

高级效果则在此基础上添加了更多视觉处理，如特效滤镜、渐变过渡、多线条和动画效果等。

## 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 微信：znzatop

![微信](https://github.com/wangqiqi/interesting_assets/blob/main/images/wechat.jpg)

## 许可证

本项目采用 GNU Affero General Public License v3.0 (AGPL-3.0) 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交问题报告、功能请求和代码贡献。请先讨论您想要进行的更改，然后再提交拉取请求。 