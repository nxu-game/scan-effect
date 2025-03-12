#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
高级扫描线效果
提供更多特效选项，如扫描线动画、颜色渐变、多重扫描线等
"""

import cv2
import numpy as np
import argparse
import os
import time
import random
import colorsys
from datetime import datetime
from scan_effect import ScanEffect, parse_color

class AdvancedScanEffect(ScanEffect):
    """
    高级扫描线效果类
    扩展基本扫描线效果，添加更多视觉效果选项
    """
    
    # 效果类型常量
    EFFECT_BASIC = "basic"
    EFFECT_NEON = "neon"
    EFFECT_MATRIX = "matrix"
    EFFECT_GLITCH = "glitch"
    EFFECT_RAINBOW = "rainbow"
    
    # 所有支持的效果类型
    SUPPORTED_EFFECTS = [
        EFFECT_BASIC,
        EFFECT_NEON,
        EFFECT_MATRIX,
        EFFECT_GLITCH,
        EFFECT_RAINBOW
    ]
    
    # 动画类型常量
    ANIMATION_NONE = "none"
    ANIMATION_PULSE = "pulse"
    ANIMATION_RAINBOW = "rainbow"
    ANIMATION_BLINK = "blink"
    
    # 所有支持的动画类型
    SUPPORTED_ANIMATIONS = [
        ANIMATION_NONE,
        ANIMATION_PULSE,
        ANIMATION_RAINBOW,
        ANIMATION_BLINK
    ]
    
    def __init__(self, video_source=0, direction="left_to_right", speed=2, 
                 line_width=3, line_color=(0, 255, 0), effect_type="basic",
                 gradient_effect=False, blur_effect=False, multi_line=1,
                 line_spacing=50, animation_type="none", display_size=(1280, 960),
                 flip_image=False):
        """
        初始化高级扫描线效果类
        
        参数:
            video_source: 视频源，可以是摄像头索引或视频文件路径
            direction: 扫描方向，可选值：left_to_right, right_to_left, top_to_bottom, bottom_to_top
            speed: 扫描速度（像素/帧）
            line_width: 扫描线宽度（像素）
            line_color: 扫描线颜色，RGB元组
            effect_type: 效果类型，可选值：basic, neon, matrix, glitch, rainbow
            gradient_effect: 是否启用渐变效果
            blur_effect: 是否启用模糊效果
            multi_line: 多线条数量
            line_spacing: 多线条间距（像素）
            animation_type: 动画类型，可选值：none, pulse, rainbow, blink
            display_size: 显示窗口大小，(宽, 高)元组
            flip_image: 是否水平翻转图像（适用于摄像头）
        """
        # 调用父类初始化方法
        super().__init__(
            video_source=video_source,
            direction=direction,
            speed=speed,
            line_width=line_width,
            line_color=line_color,
            display_size=display_size,
            flip_image=flip_image
        )
        
        # 高级效果参数
        self.effect_type = effect_type
        self.gradient_effect = gradient_effect
        self.blur_effect = blur_effect
        self.multi_line = multi_line
        self.line_spacing = line_spacing
        self.animation_type = animation_type
        
        # 动画参数
        self.animation_counter = 0
        self.animation_speed = 0.05
        self.pulse_min = 0.5
        self.pulse_max = 2.0
        self.blink_state = True
        self.blink_counter = 0
        self.blink_interval = 10
        
        # 多线条参数
        self._init_multi_lines()
    
    def _init_multi_lines(self):
        """初始化多线条参数"""
        self.multi_line_positions = []
        
        if self.multi_line <= 1:
            self.multi_line_positions = [0]  # 只有一条线，位置偏移为0
            return
        
        # 计算多线条的位置偏移
        half_lines = self.multi_line // 2
        
        if self.multi_line % 2 == 1:  # 奇数条线
            self.multi_line_positions = [i * self.line_spacing for i in range(-half_lines, half_lines + 1)]
        else:  # 偶数条线
            half_spacing = self.line_spacing // 2
            self.multi_line_positions = [i * self.line_spacing + (half_spacing if i >= 0 else -half_spacing) 
                                        for i in range(-half_lines, half_lines)]
    
    def update_scan_position(self):
        """更新扫描线位置"""
        # 调用父类方法更新主扫描线位置
        super().update_scan_position()
        
        # 更新动画计数器
        self.animation_counter += self.animation_speed
        if self.animation_counter > 1.0:
            self.animation_counter = 0.0
        
        # 更新闪烁状态
        if self.animation_type == self.ANIMATION_BLINK:
            self.blink_counter += 1
            if self.blink_counter >= self.blink_interval:
                self.blink_state = not self.blink_state
                self.blink_counter = 0
    
    def _get_animated_color(self, base_color):
        """根据动画类型获取动画颜色"""
        if self.animation_type == self.ANIMATION_NONE:
            return base_color
        
        elif self.animation_type == self.ANIMATION_PULSE:
            # 脉冲动画：颜色亮度随时间变化
            pulse_factor = self.pulse_min + (self.pulse_max - self.pulse_min) * (np.sin(self.animation_counter * 2 * np.pi) * 0.5 + 0.5)
            r = min(255, int(base_color[0] * pulse_factor))
            g = min(255, int(base_color[1] * pulse_factor))
            b = min(255, int(base_color[2] * pulse_factor))
            return (r, g, b)
        
        elif self.animation_type == self.ANIMATION_RAINBOW:
            # 彩虹动画：颜色随时间变化
            h = (self.animation_counter) % 1.0
            r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
            return (int(r * 255), int(g * 255), int(b * 255))
        
        elif self.animation_type == self.ANIMATION_BLINK:
            # 闪烁动画：颜色在两种状态间切换
            if self.blink_state:
                return base_color
            else:
                return (0, 0, 0)  # 黑色（不可见）
        
        return base_color
    
    def _get_line_width(self):
        """获取当前线宽（可能受动画影响）"""
        if self.animation_type == self.ANIMATION_PULSE:
            # 脉冲动画：线宽随时间变化
            pulse_factor = self.pulse_min + (self.pulse_max - self.pulse_min) * (np.sin(self.animation_counter * 2 * np.pi) * 0.5 + 0.5)
            return max(1, int(self.line_width * pulse_factor))
        
        return self.line_width
    
    def draw_scan_line(self, frame):
        """在帧上绘制扫描线（支持多线条和动画）"""
        # 获取当前线宽和颜色（可能受动画影响）
        current_width = self._get_line_width()
        current_color = self._get_animated_color(self.line_color)
        
        # 如果是闪烁动画且当前状态为不可见，则跳过绘制
        if self.animation_type == self.ANIMATION_BLINK and not self.blink_state:
            return
        
        # 绘制多条扫描线
        for offset in self.multi_line_positions:
            position = self.scan_position + offset
            
            # 检查位置是否在有效范围内
            if self.is_horizontal_direction():
                if position < 0 or position >= self.width:
                    continue
                
                # 绘制水平方向的扫描线
                cv2.line(frame, 
                        (position, 0), 
                        (position, self.height), 
                        current_color, 
                        current_width)
                
                # 添加渐变效果
                if self.gradient_effect:
                    self._add_gradient_effect(frame, position, True)
                
            else:  # 垂直方向
                if position < 0 or position >= self.height:
                    continue
                
                # 绘制垂直方向的扫描线
                cv2.line(frame, 
                        (0, position), 
                        (self.width, position), 
                        current_color, 
                        current_width)
                
                # 添加渐变效果
                if self.gradient_effect:
                    self._add_gradient_effect(frame, position, False)
    
    def _add_gradient_effect(self, frame, position, is_horizontal):
        """添加渐变效果"""
        gradient_width = 20  # 渐变宽度
        
        if is_horizontal:
            # 水平方向的渐变
            for i in range(1, gradient_width):
                alpha = 1.0 - (i / gradient_width)
                color = tuple(int(c * alpha) for c in self.line_color)
                width = max(1, int(self.line_width * alpha))
                
                # 向左渐变
                left_pos = position - i
                if 0 <= left_pos < self.width:
                    cv2.line(frame, (left_pos, 0), (left_pos, self.height), color, width)
                
                # 向右渐变
                right_pos = position + i
                if 0 <= right_pos < self.width:
                    cv2.line(frame, (right_pos, 0), (right_pos, self.height), color, width)
        else:
            # 垂直方向的渐变
            for i in range(1, gradient_width):
                alpha = 1.0 - (i / gradient_width)
                color = tuple(int(c * alpha) for c in self.line_color)
                width = max(1, int(self.line_width * alpha))
                
                # 向上渐变
                top_pos = position - i
                if 0 <= top_pos < self.height:
                    cv2.line(frame, (0, top_pos), (self.width, top_pos), color, width)
                
                # 向下渐变
                bottom_pos = position + i
                if 0 <= bottom_pos < self.height:
                    cv2.line(frame, (0, bottom_pos), (self.width, bottom_pos), color, width)
    
    def _apply_effect(self, frame):
        """应用特殊效果"""
        if self.effect_type == self.EFFECT_BASIC:
            # 基本效果，不做额外处理
            return frame
        
        elif self.effect_type == self.EFFECT_NEON:
            # 霓虹效果：增加亮度和对比度，添加发光效果
            result = frame.copy()
            
            # 增加亮度和对比度
            result = cv2.convertScaleAbs(result, alpha=1.2, beta=10)
            
            # 添加发光效果（模糊）
            if self.blur_effect:
                glow = cv2.GaussianBlur(result, (15, 15), 0)
                result = cv2.addWeighted(result, 1.0, glow, 0.5, 0)
            
            return result
        
        elif self.effect_type == self.EFFECT_MATRIX:
            # 矩阵效果：绿色色调，添加数字雨效果
            result = frame.copy()
            
            # 提取绿色通道并增强
            b, g, r = cv2.split(result)
            g = cv2.convertScaleAbs(g, alpha=1.5, beta=10)
            result = cv2.merge([b * 0.2, g, r * 0.2])
            
            # 随机添加一些亮点（模拟数字）
            if random.random() < 0.3:  # 30%的帧添加
                for _ in range(50):
                    x = random.randint(0, self.width - 1)
                    y = random.randint(0, self.height - 1)
                    brightness = random.randint(200, 255)
                    cv2.circle(result, (x, y), 1, (0, brightness, 0), -1)
            
            return result
        
        elif self.effect_type == self.EFFECT_GLITCH:
            # 故障效果：随机偏移通道，添加噪点
            result = frame.copy()
            
            # 随机通道偏移
            if random.random() < 0.2:  # 20%的帧添加偏移
                b, g, r = cv2.split(result)
                
                # 随机偏移红色通道
                offset_x = random.randint(-10, 10)
                offset_y = random.randint(-10, 10)
                r_shifted = np.zeros_like(r)
                
                # 应用偏移
                if offset_x >= 0 and offset_y >= 0:
                    r_shifted[offset_y:, offset_x:] = r[:self.height-offset_y, :self.width-offset_x]
                elif offset_x >= 0 and offset_y < 0:
                    r_shifted[:self.height+offset_y, offset_x:] = r[-offset_y:, :self.width-offset_x]
                elif offset_x < 0 and offset_y >= 0:
                    r_shifted[offset_y:, :self.width+offset_x] = r[:self.height-offset_y, -offset_x:]
                else:
                    r_shifted[:self.height+offset_y, :self.width+offset_x] = r[-offset_y:, -offset_x:]
                
                result = cv2.merge([b, g, r_shifted])
            
            # 添加噪点
            if random.random() < 0.3:  # 30%的帧添加噪点
                noise = np.zeros((self.height, self.width), dtype=np.uint8)
                cv2.randu(noise, 0, 255)
                noise = cv2.threshold(noise, 200, 255, cv2.THRESH_BINARY)[1]
                
                # 将噪点添加到随机通道
                channel = random.randint(0, 2)
                b, g, r = cv2.split(result)
                channels = [b, g, r]
                channels[channel] = cv2.bitwise_or(channels[channel], noise)
                result = cv2.merge(channels)
            
            return result
        
        elif self.effect_type == self.EFFECT_RAINBOW:
            # 彩虹效果：根据位置添加彩虹色调
            result = frame.copy()
            
            # 创建彩虹渐变
            rainbow = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            if self.is_horizontal_direction():
                # 水平彩虹
                for x in range(self.width):
                    h = x / self.width
                    r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
                    rainbow[:, x] = [b * 255, g * 255, r * 255]
            else:
                # 垂直彩虹
                for y in range(self.height):
                    h = y / self.height
                    r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
                    rainbow[y, :] = [b * 255, g * 255, r * 255]
            
            # 混合原始帧和彩虹
            result = cv2.addWeighted(result, 0.7, rainbow, 0.3, 0)
            
            return result
        
        return frame
    
    def create_scan_effect(self, current_frame):
        """创建高级扫描效果"""
        # 更新静态帧中扫描线扫过的区域为当前帧的内容
        self.update_static_frame(current_frame, self.scan_position, self.speed)
        
        # 应用扫描效果
        result = self.apply_scan_effect(current_frame, self.scan_position)
        
        # 应用特殊效果
        result = self._apply_effect(result)
        
        # 应用模糊效果（如果启用）
        if self.blur_effect and self.effect_type != self.EFFECT_NEON:  # 霓虹效果已经包含模糊
            result = cv2.GaussianBlur(result, (5, 5), 0)
        
        # 绘制扫描线
        self.draw_scan_line(result)
        
        return result
    
    def reset_scan_line(self):
        """重置扫描线位置和动画参数"""
        super().reset_scan_line()
        self.animation_counter = 0
        self.blink_state = True
        self.blink_counter = 0

def main():
    parser = argparse.ArgumentParser(description="高级视频扫描线效果")
    parser.add_argument("--video", type=str, default=0,
                        help="视频文件路径，默认使用摄像头")
    parser.add_argument("--direction", type=str, default=ScanEffect.DIRECTION_LEFT_TO_RIGHT,
                        choices=ScanEffect.SUPPORTED_DIRECTIONS,
                        help="扫描方向")
    parser.add_argument("--speed", type=int, default=2,
                        help="扫描速度（像素/帧）")
    parser.add_argument("--line_width", type=int, default=3,
                        help="扫描线宽度（像素）")
    parser.add_argument("--line_color", type=parse_color, default="0,255,0",
                        help="扫描线颜色，格式为'R,G,B'")
    parser.add_argument("--effect", type=str, default=AdvancedScanEffect.EFFECT_BASIC,
                        choices=AdvancedScanEffect.SUPPORTED_EFFECTS,
                        help="效果类型")
    parser.add_argument("--gradient", action="store_true",
                        help="启用渐变效果")
    parser.add_argument("--blur", action="store_true",
                        help="启用模糊效果")
    parser.add_argument("--multi_line", type=int, default=1,
                        help="多线条数量")
    parser.add_argument("--line_spacing", type=int, default=50,
                        help="多线条间距（像素）")
    parser.add_argument("--animation", type=str, default=AdvancedScanEffect.ANIMATION_NONE,
                        choices=AdvancedScanEffect.SUPPORTED_ANIMATIONS,
                        help="动画类型")
    parser.add_argument("--display_width", type=int, default=1280,
                        help="显示窗口宽度")
    parser.add_argument("--display_height", type=int, default=960,
                        help="显示窗口高度")
    parser.add_argument("--flip", action="store_true",
                        help="水平翻转图像（适用于摄像头）")
    
    args = parser.parse_args()
    
    # 处理视频源
    video_source = args.video
    if video_source != 0 and not os.path.exists(video_source):
        print(f"错误: 视频文件不存在: {video_source}")
        return
    
    try:
        # 创建并运行高级扫描效果
        video_source = 0 if args.video == "0" else args.video
        scan_effect = AdvancedScanEffect(
            video_source=video_source,
            direction=args.direction,
            speed=args.speed,
            line_width=args.line_width,
            line_color=args.line_color if isinstance(args.line_color, tuple) else parse_color(args.line_color),
            effect_type=args.effect,
            gradient_effect=args.gradient,
            blur_effect=args.blur,
            multi_line=args.multi_line,
            line_spacing=args.line_spacing,
            animation_type=args.animation,
            display_size=(args.display_width, args.display_height),
            flip_image=args.flip
        )
        scan_effect.run()
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main() 