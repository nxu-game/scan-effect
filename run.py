#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
扫描线效果启动脚本
提供一个交互式菜单，方便用户选择不同的扫描线效果模式
"""

import os
import sys
import platform
import subprocess

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 现在可以直接导入src目录下的模块
from scan_effect import ScanEffect
from advanced_scan_effect import AdvancedScanEffect

def clear_screen():
    """清除终端屏幕"""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def print_header():
    """打印程序标题"""
    clear_screen()
    print("=" * 60)
    print("                  扫描线效果生成器")
    print("=" * 60)
    print("这个程序可以创建视频扫描线效果，当扫描线移动时，")
    print("扫描过的区域显示静止图像，未扫描的区域显示动态视频。")
    print("=" * 60)
    print()

def print_menu():
    """打印主菜单"""
    print("\n请选择操作:")
    print("1. 基础摄像头扫描效果")
    print("2. 基础视频文件扫描效果")
    print("3. 高级扫描效果演示")
    print("4. 自定义扫描效果")
    print("0. 退出")
    print("-" * 60)

def run_basic_webcam():
    """运行基础摄像头扫描效果"""
    clear_screen()
    print("正在启动基础摄像头扫描效果...")
    print("按ESC键退出，空格键暂停/继续，r键重置扫描线，s键保存当前帧，f键切换图像翻转")
    print("默认启用图像翻转，使动作方向与屏幕显示一致")
    
    # 导入并运行demo.py中的摄像头演示
    from demo import demo_webcam
    demo_webcam()

def run_basic_video():
    """运行基础视频文件扫描效果"""
    clear_screen()
    print("基础视频文件扫描效果")
    print("=" * 60)
    
    # 获取视频文件路径
    video_path = input("请输入视频文件路径（按Enter使用示例视频）: ")
    
    if not video_path.strip():
        # 使用示例视频
        video_path = os.path.join("examples", "sample.mp4")
        if not os.path.exists(video_path):
            print(f"错误: 示例视频不存在: {video_path}")
            print("请确保examples目录中有sample.mp4文件")
            input("按Enter键返回主菜单...")
            return
    
    if not os.path.exists(video_path):
        print(f"错误: 视频文件不存在: {video_path}")
        input("按Enter键返回主菜单...")
        return
    
    print(f"使用视频文件: {video_path}")
    print("按ESC键退出，空格键暂停/继续，r键重置扫描线，s键保存当前帧")
    
    # 导入并运行demo.py中的视频演示
    from demo import demo_video
    demo_video(video_path)

def run_advanced_demo():
    """运行高级扫描效果演示"""
    clear_screen()
    print("高级扫描效果演示")
    print("=" * 60)
    print("这个演示将展示高级扫描线效果的各种功能。")
    print("包括：不同效果类型、渐变效果、模糊效果、多线条效果、动画效果等。")
    print("按ESC键可以随时退出当前演示。")
    print("按f键可以切换图像翻转（适用于摄像头）。")
    print("=" * 60)
    
    # 询问是否使用摄像头或视频文件
    choice = input("请选择输入源 [1: 摄像头(默认), 2: 视频文件]: ")
    
    if choice == "2":
        video_path = input("请输入视频文件路径: ")
        if not os.path.exists(video_path):
            print(f"错误: 视频文件不存在: {video_path}")
            input("按Enter键返回主菜单...")
            return
        
        # 导入并运行advanced_demo.py
        from advanced_demo import main as advanced_demo_main
        # 修改sys.argv以传递视频路径
        sys.argv = [sys.argv[0], video_path]
    else:
        # 使用摄像头
        from advanced_demo import main as advanced_demo_main
        sys.argv = [sys.argv[0]]  # 重置参数
    
    # 运行高级演示
    advanced_demo_main()

def run_custom():
    """运行自定义扫描效果"""
    clear_screen()
    print("自定义扫描效果")
    print("=" * 60)
    
    # 选择基础或高级模式
    mode = input("请选择模式 [1: 基础模式(默认), 2: 高级模式]: ")
    advanced_mode = (mode == "2")
    
    # 选择输入源
    source_type = input("请选择输入源 [1: 摄像头(默认), 2: 视频文件]: ")
    
    if source_type == "2":
        video_path = input("请输入视频文件路径: ")
        if not os.path.exists(video_path):
            print(f"错误: 视频文件不存在: {video_path}")
            input("按Enter键返回主菜单...")
            return
        video_source = video_path
    else:
        video_source = 0  # 默认摄像头
    
    # 选择扫描方向
    print("\n请选择扫描方向:")
    print("1. 从左到右 (默认)")
    print("2. 从右到左")
    print("3. 从上到下")
    print("4. 从下到上")
    direction_choice = input("请选择 [1-4]: ")
    
    directions = [
        ScanEffect.DIRECTION_LEFT_TO_RIGHT,
        ScanEffect.DIRECTION_RIGHT_TO_LEFT,
        ScanEffect.DIRECTION_TOP_TO_BOTTOM,
        ScanEffect.DIRECTION_BOTTOM_TO_TOP
    ]
    
    try:
        direction = directions[int(direction_choice) - 1] if direction_choice else directions[0]
    except (ValueError, IndexError):
        direction = directions[0]  # 默认从左到右
    
    # 设置扫描速度
    speed = input("请输入扫描速度 [默认: 2]: ")
    speed = int(speed) if speed.isdigit() else 2
    
    # 设置线宽
    line_width = input("请输入扫描线宽度 [默认: 3]: ")
    line_width = int(line_width) if line_width.isdigit() else 3
    
    # 设置线颜色
    print("\n请选择扫描线颜色:")
    print("1. 绿色 (默认)")
    print("2. 红色")
    print("3. 蓝色")
    print("4. 黄色")
    print("5. 自定义 (R,G,B格式)")
    color_choice = input("请选择 [1-5]: ")
    
    colors = [
        (0, 255, 0),    # 绿色
        (0, 0, 255),    # 红色
        (255, 0, 0),    # 蓝色
        (0, 255, 255),  # 黄色
    ]
    
    if color_choice == "5":
        color_str = input("请输入颜色 (R,G,B格式，例如: 255,0,255): ")
        try:
            r, g, b = map(int, color_str.split(','))
            line_color = (r, g, b)
        except:
            print("颜色格式错误，使用默认绿色")
            line_color = colors[0]
    else:
        try:
            line_color = colors[int(color_choice) - 1] if color_choice else colors[0]
        except (ValueError, IndexError):
            line_color = colors[0]  # 默认绿色
    
    # 是否启用图像翻转（适用于摄像头）
    flip_choice = input("是否启用图像翻转（适用于摄像头）[Y/n]: ")
    flip_image = flip_choice.lower() != "n"
    
    # 构建命令参数
    cmd_args = [
        sys.executable,
        os.path.join("src", "advanced_scan_effect.py" if advanced_mode else "scan_effect.py"),
        f"--video={video_source}",
        f"--direction={direction}",
        f"--speed={speed}",
        f"--line_width={line_width}",
        f"--line_color={line_color[0]},{line_color[1]},{line_color[2]}",
    ]
    
    if flip_image:
        cmd_args.append("--flip")
    
    # 高级模式特有参数
    if advanced_mode:
        # 选择效果类型
        print("\n请选择效果类型:")
        print("1. 基本效果 (默认)")
        print("2. 霓虹效果")
        print("3. 矩阵效果")
        print("4. 故障效果")
        print("5. 彩虹效果")
        effect_choice = input("请选择 [1-5]: ")
        
        effects = [
            AdvancedScanEffect.EFFECT_BASIC,
            AdvancedScanEffect.EFFECT_NEON,
            AdvancedScanEffect.EFFECT_MATRIX,
            AdvancedScanEffect.EFFECT_GLITCH,
            AdvancedScanEffect.EFFECT_RAINBOW
        ]
        
        try:
            effect = effects[int(effect_choice) - 1] if effect_choice else effects[0]
        except (ValueError, IndexError):
            effect = effects[0]  # 默认基本效果
        
        cmd_args.append(f"--effect={effect}")
        
        # 是否启用渐变效果
        gradient_choice = input("是否启用渐变效果 [y/N]: ")
        if gradient_choice.lower() == "y":
            cmd_args.append("--gradient")
        
        # 是否启用模糊效果
        blur_choice = input("是否启用模糊效果 [y/N]: ")
        if blur_choice.lower() == "y":
            cmd_args.append("--blur")
        
        # 设置多线条数量
        multi_line = input("请输入多线条数量 [默认: 1]: ")
        multi_line = int(multi_line) if multi_line.isdigit() and int(multi_line) > 0 else 1
        cmd_args.append(f"--multi_line={multi_line}")
        
        if multi_line > 1:
            # 设置线条间距
            line_spacing = input("请输入线条间距 [默认: 50]: ")
            line_spacing = int(line_spacing) if line_spacing.isdigit() else 50
            cmd_args.append(f"--line_spacing={line_spacing}")
        
        # 选择动画类型
        print("\n请选择动画类型:")
        print("1. 无动画 (默认)")
        print("2. 脉冲动画")
        print("3. 彩虹动画")
        print("4. 闪烁动画")
        animation_choice = input("请选择 [1-4]: ")
        
        animations = [
            AdvancedScanEffect.ANIMATION_NONE,
            AdvancedScanEffect.ANIMATION_PULSE,
            AdvancedScanEffect.ANIMATION_RAINBOW,
            AdvancedScanEffect.ANIMATION_BLINK
        ]
        
        try:
            animation = animations[int(animation_choice) - 1] if animation_choice else animations[0]
        except (ValueError, IndexError):
            animation = animations[0]  # 默认无动画
        
        cmd_args.append(f"--animation={animation}")
    
    # 运行命令
    print("\n正在启动扫描效果...")
    print("按ESC键退出，空格键暂停/继续，r键重置扫描线，s键保存当前帧，f键切换图像翻转")
    print("=" * 60)
    
    try:
        subprocess.run(cmd_args)
    except Exception as e:
        print(f"错误: {e}")
    
    input("\n按Enter键返回主菜单...")

def main():
    """主函数"""
    while True:
        print_header()
        print_menu()
        
        choice = input("请输入选项编号: ")
        
        if choice == "1":
            run_basic_webcam()
        elif choice == "2":
            run_basic_video()
        elif choice == "3":
            run_advanced_demo()
        elif choice == "4":
            run_custom()
        elif choice == "0":
            clear_screen()
            print("感谢使用扫描线效果生成器！再见！")
            break
        else:
            print("无效选项，请重新输入")
            input("按Enter键继续...")

if __name__ == "__main__":
    main() 