#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
高级扫描线效果演示脚本
这个脚本展示了高级扫描线效果的各种功能
"""

import os
import sys
import time
import cv2
from advanced_scan_effect import AdvancedScanEffect
from scan_effect import ScanEffect
from demo import print_demo_info, wait_for_key

def create_advanced_scan_effect(video_source=0, direction=ScanEffect.DIRECTION_LEFT_TO_RIGHT, 
                               speed=2, line_width=3, line_color=(0, 255, 0), 
                               effect_type=AdvancedScanEffect.EFFECT_BASIC,
                               gradient_effect=False, blur_effect=False, 
                               multi_line=1, line_spacing=50, 
                               animation_type=AdvancedScanEffect.ANIMATION_NONE,
                               display_size=(1280, 960), flip_image=True):
    """创建高级扫描效果实例"""
    return AdvancedScanEffect(
        video_source=video_source,
        direction=direction,
        speed=speed,
        line_width=line_width,
        line_color=line_color,
        effect_type=effect_type,
        gradient_effect=gradient_effect,
        blur_effect=blur_effect,
        multi_line=multi_line,
        line_spacing=line_spacing,
        animation_type=animation_type,
        display_size=display_size,
        flip_image=flip_image
    )

def demo_basic_effects(video_source=0):
    """演示基本效果类型"""
    print_demo_info(
        "基本效果类型演示",
        "这个演示展示了不同的基本效果类型。\n"
        "包括：基本效果、霓虹效果、矩阵效果、故障效果和彩虹效果。"
    )
    
    # 定义要演示的效果类型
    effects = AdvancedScanEffect.SUPPORTED_EFFECTS
    
    for effect in effects:
        print(f"\n正在演示 {effect} 效果...")
        
        # 创建高级扫描效果实例
        scan_effect = create_advanced_scan_effect(
            video_source=video_source,
            effect_type=effect,
            flip_image=True
        )
        
        # 运行扫描效果
        scan_effect.run()
        
        # 检查是否继续
        if wait_for_key():
            break

def demo_gradient_effect(video_source=0):
    """演示渐变效果"""
    print_demo_info(
        "渐变效果演示",
        "这个演示展示了带有渐变效果的扫描线。\n"
        "渐变效果使扫描线周围的区域呈现渐变过渡。"
    )
    
    # 创建带有渐变效果的扫描效果实例
    scan_effect = create_advanced_scan_effect(
        video_source=video_source,
        direction=ScanEffect.DIRECTION_LEFT_TO_RIGHT,
        speed=3,
        line_width=5,
        line_color=(0, 255, 255),  # 黄色
        gradient_effect=True,
        flip_image=True
    )
    
    # 运行扫描效果
    scan_effect.run()

def demo_blur_effect(video_source=0):
    """演示模糊效果"""
    print_demo_info(
        "模糊效果演示",
        "这个演示展示了带有模糊效果的扫描线。\n"
        "模糊效果使整个图像呈现柔和的外观。"
    )
    
    # 创建带有模糊效果的扫描效果实例
    scan_effect = create_advanced_scan_effect(
        video_source=video_source,
        direction=ScanEffect.DIRECTION_LEFT_TO_RIGHT,
        speed=3,
        line_width=5,
        line_color=(255, 0, 255),  # 紫色
        blur_effect=True,
        flip_image=True
    )
    
    # 运行扫描效果
    scan_effect.run()

def demo_multi_line(video_source=0):
    """演示多线条效果"""
    print_demo_info(
        "多线条效果演示",
        "这个演示展示了多线条扫描效果。\n"
        "多线条效果使用多条平行的扫描线同时移动。"
    )
    
    # 定义要演示的多线条数量
    multi_lines = [1, 3, 5, 7]
    
    for num_lines in multi_lines:
        print(f"\n正在演示 {num_lines} 条线...")
        
        # 创建多线条扫描效果实例
        scan_effect = create_advanced_scan_effect(
            video_source=video_source,
            direction=ScanEffect.DIRECTION_LEFT_TO_RIGHT,
            speed=3,
            line_width=3,
            line_color=(0, 255, 0),  # 绿色
            multi_line=num_lines,
            line_spacing=40,
            flip_image=True
        )
        
        # 运行扫描效果
        scan_effect.run()
        
        # 检查是否继续
        if wait_for_key():
            break

def demo_animations(video_source=0):
    """演示动画效果"""
    print_demo_info(
        "动画效果演示",
        "这个演示展示了不同的扫描线动画效果。\n"
        "包括：无动画、脉冲动画、彩虹动画和闪烁动画。"
    )
    
    # 定义要演示的动画类型
    animations = AdvancedScanEffect.SUPPORTED_ANIMATIONS
    
    for animation in animations:
        print(f"\n正在演示 {animation} 动画...")
        
        # 创建带有动画效果的扫描效果实例
        scan_effect = create_advanced_scan_effect(
            video_source=video_source,
            direction=ScanEffect.DIRECTION_LEFT_TO_RIGHT,
            speed=2,
            line_width=5,
            line_color=(0, 255, 0),  # 绿色
            animation_type=animation,
            flip_image=True
        )
        
        # 运行扫描效果
        scan_effect.run()
        
        # 检查是否继续
        if wait_for_key():
            break

def demo_directions(video_source=0):
    """演示不同的扫描方向"""
    print_demo_info(
        "不同扫描方向演示",
        "这个演示展示了四种不同的扫描方向效果，结合高级效果。"
    )
    
    # 定义要演示的方向
    directions = ScanEffect.SUPPORTED_DIRECTIONS
    
    for direction in directions:
        print(f"\n正在演示 {direction} 方向...")
        
        # 创建高级扫描效果实例
        scan_effect = create_advanced_scan_effect(
            video_source=video_source,
            direction=direction,
            speed=3,
            line_width=3,
            line_color=(0, 255, 0),  # 绿色
            effect_type=AdvancedScanEffect.EFFECT_NEON,
            flip_image=True
        )
        
        # 运行扫描效果
        scan_effect.run()
        
        # 检查是否继续
        if wait_for_key():
            break

def demo_combined_effects(video_source=0):
    """演示组合效果"""
    print_demo_info(
        "组合效果演示",
        "这个演示展示了多种效果组合在一起的效果。\n"
        "包括：多线条 + 渐变 + 动画 + 特效"
    )
    
    # 创建组合效果的扫描效果实例
    scan_effect = create_advanced_scan_effect(
        video_source=video_source,
        direction=ScanEffect.DIRECTION_LEFT_TO_RIGHT,
        speed=2,
        line_width=3,
        line_color=(0, 255, 255),  # 黄色
        effect_type=AdvancedScanEffect.EFFECT_RAINBOW,
        gradient_effect=True,
        blur_effect=True,
        multi_line=3,
        line_spacing=50,
        animation_type=AdvancedScanEffect.ANIMATION_PULSE,
        flip_image=True
    )
    
    # 运行扫描效果
    scan_effect.run()

def main():
    """主函数"""
    print("高级扫描线效果演示")
    print("=" * 50)
    
    # 默认使用摄像头
    video_source = 0
    
    while True:
        print("\n请选择演示:")
        print("1. 基本效果类型")
        print("2. 渐变效果")
        print("3. 模糊效果")
        print("4. 多线条效果")
        print("5. 动画效果")
        print("6. 不同扫描方向")
        print("7. 组合效果")
        print("8. 使用视频文件")
        print("0. 退出")
        
        choice = input("请输入选项编号: ")
        
        if choice == "1":
            demo_basic_effects(video_source)
        elif choice == "2":
            demo_gradient_effect(video_source)
        elif choice == "3":
            demo_blur_effect(video_source)
        elif choice == "4":
            demo_multi_line(video_source)
        elif choice == "5":
            demo_animations(video_source)
        elif choice == "6":
            demo_directions(video_source)
        elif choice == "7":
            demo_combined_effects(video_source)
        elif choice == "8":
            video_path = input("请输入视频文件路径: ")
            if os.path.exists(video_path):
                video_source = video_path
                print(f"已设置视频源为: {video_path}")
            else:
                print(f"错误: 视频文件不存在: {video_path}")
        elif choice == "0":
            break
        else:
            print("无效选项，请重新输入")
    
    print("演示结束")

if __name__ == "__main__":
    main() 