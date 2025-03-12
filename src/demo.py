#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
扫描线效果演示脚本
这个脚本展示了如何使用扫描线效果，并提供了一些预设的效果示例
"""

import os
import sys
import time
from scan_effect import ScanEffect

# 通用演示函数
def print_demo_info(title, description):
    """打印演示信息"""
    print("\n" + "=" * 50)
    print(f"=== {title} ===")
    print("=" * 50)
    print(description)
    print("按ESC键退出，空格键暂停/继续，r键重置扫描线，s键保存当前帧，f键切换图像翻转")
    print("=" * 50)
    print("正在初始化...")

def wait_for_key():
    """等待用户按键继续"""
    print("\n按任意键继续下一个演示，或按ESC退出...")
    key = input()
    return key.lower() == 'q' or key == '\x1b'  # q或ESC退出

def create_scan_effect(video_source=0, direction=ScanEffect.DIRECTION_LEFT_TO_RIGHT, 
                      speed=2, line_width=3, line_color=(0, 255, 0), 
                      display_size=(1280, 960), flip_image=True):
    """创建扫描效果实例"""
    return ScanEffect(
        video_source=video_source,
        direction=direction,
        speed=speed,
        line_width=line_width,
        line_color=line_color,
        display_size=display_size,
        flip_image=flip_image
    )

def demo_webcam():
    """使用摄像头演示扫描线效果"""
    print_demo_info(
        "摄像头扫描线效果演示",
        "这个演示展示了使用摄像头的基本扫描线效果。"
    )
    
    # 创建扫描效果实例（使用默认参数）
    scan_effect = create_scan_effect(
        video_source=0,  # 使用默认摄像头
        direction=ScanEffect.DIRECTION_LEFT_TO_RIGHT,
        speed=2,
        line_width=3,
        line_color=(0, 255, 0),  # 绿色
        display_size=(1280, 960),  # 适合笔记本屏幕的显示大小
        flip_image=True  # 默认启用图像翻转，使动作方向与屏幕显示一致
    )
    
    # 运行扫描效果
    scan_effect.run()

def demo_video(video_path):
    """使用视频文件演示扫描线效果"""
    if not os.path.exists(video_path):
        print(f"错误: 视频文件不存在: {video_path}")
        return
    
    print_demo_info(
        "视频文件扫描线效果演示",
        f"这个演示展示了使用视频文件的基本扫描线效果。\n视频文件: {video_path}"
    )
    
    # 创建扫描效果实例
    scan_effect = create_scan_effect(
        video_source=video_path,
        direction=ScanEffect.DIRECTION_LEFT_TO_RIGHT,
        speed=3,  # 稍快的速度
        line_width=5,  # 更宽的线
        line_color=(0, 0, 255),  # 红色
        display_size=(1280, 960),
        flip_image=False  # 视频文件通常不需要翻转
    )
    
    # 运行扫描效果
    scan_effect.run()

def demo_directions():
    """演示不同的扫描方向"""
    print_demo_info(
        "不同扫描方向演示",
        "这个演示展示了四种不同的扫描方向效果。"
    )
    
    # 定义要演示的方向
    directions = ScanEffect.SUPPORTED_DIRECTIONS
    
    for direction in directions:
        print(f"\n正在演示 {direction} 方向...")
        
        # 创建扫描效果实例
        scan_effect = create_scan_effect(
            video_source=0,  # 使用默认摄像头
            direction=direction,
            speed=3,
            line_width=3,
            line_color=(0, 255, 0),  # 绿色
            display_size=(1280, 960),
            flip_image=True
        )
        
        # 运行扫描效果
        scan_effect.run()
        
        # 检查是否继续
        if wait_for_key():
            break

def demo_colors():
    """演示不同的扫描线颜色"""
    print_demo_info(
        "不同扫描线颜色演示",
        "这个演示展示了不同颜色的扫描线效果。"
    )
    
    # 定义要演示的颜色
    colors = [
        (0, 255, 0),    # 绿色
        (0, 0, 255),    # 红色
        (255, 0, 0),    # 蓝色
        (0, 255, 255),  # 黄色
        (255, 0, 255),  # 紫色
        (255, 255, 0),  # 青色
        (255, 255, 255) # 白色
    ]
    
    for color in colors:
        print(f"\n正在演示颜色 {color}...")
        
        # 创建扫描效果实例
        scan_effect = create_scan_effect(
            video_source=0,  # 使用默认摄像头
            direction=ScanEffect.DIRECTION_LEFT_TO_RIGHT,
            speed=3,
            line_width=5,
            line_color=color,
            display_size=(1280, 960),
            flip_image=True
        )
        
        # 运行扫描效果
        scan_effect.run()
        
        # 检查是否继续
        if wait_for_key():
            break

def main():
    """主函数"""
    print("扫描线效果演示")
    print("=" * 50)
    
    while True:
        print("\n请选择演示:")
        print("1. 摄像头基本效果")
        print("2. 视频文件效果")
        print("3. 不同扫描方向")
        print("4. 不同扫描线颜色")
        print("0. 退出")
        
        choice = input("请输入选项编号: ")
        
        if choice == "1":
            demo_webcam()
        elif choice == "2":
            video_path = input("请输入视频文件路径: ")
            demo_video(video_path)
        elif choice == "3":
            demo_directions()
        elif choice == "4":
            demo_colors()
        elif choice == "0":
            break
        else:
            print("无效选项，请重新输入")
    
    print("演示结束")

if __name__ == "__main__":
    main() 