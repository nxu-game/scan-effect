#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import argparse
import os
import time
from datetime import datetime

class ScanEffect:
    """
    扫描线效果基类
    实现基本的扫描线效果功能
    """
    
    # 扫描方向常量
    DIRECTION_LEFT_TO_RIGHT = "left_to_right"
    DIRECTION_RIGHT_TO_LEFT = "right_to_left"
    DIRECTION_TOP_TO_BOTTOM = "top_to_bottom"
    DIRECTION_BOTTOM_TO_TOP = "bottom_to_top"
    
    # 所有支持的扫描方向
    SUPPORTED_DIRECTIONS = [
        DIRECTION_LEFT_TO_RIGHT,
        DIRECTION_RIGHT_TO_LEFT,
        DIRECTION_TOP_TO_BOTTOM,
        DIRECTION_BOTTOM_TO_TOP
    ]
    
    def __init__(self, video_source=0, direction="left_to_right", speed=2, line_width=3, line_color=(0, 255, 0), display_size=(1280, 960), flip_image=False):
        """
        初始化扫描线效果类
        
        参数:
            video_source: 视频源，可以是摄像头索引或视频文件路径
            direction: 扫描方向，可选值：left_to_right, right_to_left, top_to_bottom, bottom_to_top
            speed: 扫描速度（像素/帧）
            line_width: 扫描线宽度（像素）
            line_color: 扫描线颜色，RGB元组
            display_size: 显示窗口大小，(宽, 高)元组
            flip_image: 是否水平翻转图像（适用于摄像头）
        """
        # 基本参数
        self.video_source = video_source
        self.direction = direction
        self.speed = speed
        self.line_width = line_width
        self.line_color = line_color
        self.display_size = display_size
        self.flip_image = flip_image
        
        # 状态变量
        self.paused = False
        self.running = True
        
        # 初始化视频捕获
        self._init_video_capture()
        
        # 初始化扫描线位置
        self.scan_position = 0
        self.reset_scan_line()
        
        # 初始化静态帧
        self._init_static_frame()
    
    def _init_video_capture(self):
        """初始化视频捕获"""
        self.cap = cv2.VideoCapture(self.video_source)
        if not self.cap.isOpened():
            raise ValueError(f"无法打开视频源: {self.video_source}")
        
        # 获取视频属性
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        if self.fps <= 0:
            self.fps = 30  # 如果无法获取帧率，使用默认值
        
        # 计算缩放比例
        self.scale_factor = min(self.display_size[0] / self.width, self.display_size[1] / self.height)
        self.scaled_width = int(self.width * self.scale_factor)
        self.scaled_height = int(self.height * self.scale_factor)
    
    def _init_static_frame(self):
        """初始化静态帧"""
        ret, frame = self.cap.read()
        if not ret:
            raise ValueError("无法读取第一帧")
        
        # 如果需要，水平翻转图像
        if self.flip_image:
            frame = cv2.flip(frame, 1)
        
        self.static_frame = frame
    
    def reset_scan_line(self):
        """重置扫描线位置到初始位置"""
        if self.direction == self.DIRECTION_LEFT_TO_RIGHT:
            self.scan_position = 0
        elif self.direction == self.DIRECTION_RIGHT_TO_LEFT:
            self.scan_position = self.width
        elif self.direction == self.DIRECTION_TOP_TO_BOTTOM:
            self.scan_position = 0
        elif self.direction == self.DIRECTION_BOTTOM_TO_TOP:
            self.scan_position = self.height
        else:
            raise ValueError(f"不支持的扫描方向: {self.direction}")
    
    def update_scan_position(self):
        """更新扫描线位置"""
        if self.paused:
            return
        
        if self.direction == self.DIRECTION_LEFT_TO_RIGHT:
            self.scan_position += self.speed
            if self.scan_position > self.width:
                self.scan_position = self.width
        elif self.direction == self.DIRECTION_RIGHT_TO_LEFT:
            self.scan_position -= self.speed
            if self.scan_position < 0:
                self.scan_position = 0
        elif self.direction == self.DIRECTION_TOP_TO_BOTTOM:
            self.scan_position += self.speed
            if self.scan_position > self.height:
                self.scan_position = self.height
        elif self.direction == self.DIRECTION_BOTTOM_TO_TOP:
            self.scan_position -= self.speed
            if self.scan_position < 0:
                self.scan_position = 0
    
    def draw_scan_line(self, frame):
        """在帧上绘制扫描线"""
        if self.is_horizontal_direction():
            cv2.line(frame, 
                    (self.scan_position, 0), 
                    (self.scan_position, self.height), 
                    self.line_color, 
                    self.line_width)
        else:  # 垂直方向
            cv2.line(frame, 
                    (0, self.scan_position), 
                    (self.width, self.scan_position), 
                    self.line_color, 
                    self.line_width)
    
    def is_horizontal_direction(self):
        """判断是否为水平方向的扫描"""
        return self.direction in [self.DIRECTION_LEFT_TO_RIGHT, self.DIRECTION_RIGHT_TO_LEFT]
    
    def is_forward_direction(self):
        """判断是否为正向扫描（从左到右或从上到下）"""
        return self.direction in [self.DIRECTION_LEFT_TO_RIGHT, self.DIRECTION_TOP_TO_BOTTOM]
    
    def update_static_frame(self, current_frame, position, speed):
        """更新静态帧中扫描线扫过的区域"""
        if self.is_horizontal_direction():
            # 水平方向（左右）
            if self.is_forward_direction():
                # 从左到右
                if 0 <= position < self.width:
                    update_width = min(speed, self.width - position)
                    if update_width > 0:
                        self.static_frame[:, position:position+update_width] = current_frame[:, position:position+update_width]
            else:
                # 从右到左
                if 0 <= position < self.width:
                    update_width = min(speed, position)
                    if update_width > 0:
                        self.static_frame[:, position-update_width:position] = current_frame[:, position-update_width:position]
        else:
            # 垂直方向（上下）
            if self.is_forward_direction():
                # 从上到下
                if 0 <= position < self.height:
                    update_height = min(speed, self.height - position)
                    if update_height > 0:
                        self.static_frame[position:position+update_height, :] = current_frame[position:position+update_height, :]
            else:
                # 从下到上
                if 0 <= position < self.height:
                    update_height = min(speed, position)
                    if update_height > 0:
                        self.static_frame[position-update_height:position, :] = current_frame[position-update_height:position, :]
    
    def apply_scan_effect(self, current_frame, position):
        """应用扫描效果，将静态帧和当前帧合并"""
        result = current_frame.copy()
        
        if self.direction == self.DIRECTION_LEFT_TO_RIGHT:
            # 左侧为静态，右侧为动态
            valid_pos = int(min(max(0, position), self.width))
            if valid_pos > 0:
                result[:, :valid_pos] = self.static_frame[:, :valid_pos]
        
        elif self.direction == self.DIRECTION_RIGHT_TO_LEFT:
            # 右侧为静态，左侧为动态
            valid_pos = int(min(max(0, position), self.width))
            if valid_pos < self.width:
                result[:, valid_pos:] = self.static_frame[:, valid_pos:]
        
        elif self.direction == self.DIRECTION_TOP_TO_BOTTOM:
            # 上部为静态，下部为动态
            valid_pos = int(min(max(0, position), self.height))
            if valid_pos > 0:
                result[:valid_pos, :] = self.static_frame[:valid_pos, :]
        
        elif self.direction == self.DIRECTION_BOTTOM_TO_TOP:
            # 下部为静态，上部为动态
            valid_pos = int(min(max(0, position), self.height))
            if valid_pos < self.height:
                result[valid_pos:, :] = self.static_frame[valid_pos:, :]
        
        return result
    
    def create_scan_effect(self, current_frame):
        """创建扫描效果"""
        # 更新静态帧中扫描线扫过的区域为当前帧的内容
        self.update_static_frame(current_frame, self.scan_position, self.speed)
        
        # 应用扫描效果
        result = self.apply_scan_effect(current_frame, self.scan_position)
        
        # 绘制扫描线
        self.draw_scan_line(result)
        
        return result
    
    def save_frame(self, frame):
        """保存当前帧为图片"""
        if not os.path.exists("output"):
            os.makedirs("output")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/scan_effect_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"已保存图片: {filename}")
    
    def resize_frame(self, frame):
        """调整帧大小以适应显示窗口"""
        return cv2.resize(frame, (self.scaled_width, self.scaled_height))
    
    def process_key_event(self, key):
        """处理键盘事件"""
        if key == 27:  # ESC键
            self.running = False
        elif key == 32:  # 空格键
            self.paused = not self.paused
        elif key == ord('r'):  # r键
            self.reset_scan_line()
            ret, self.static_frame = self.cap.read()
            if self.flip_image and ret:
                self.static_frame = cv2.flip(self.static_frame, 1)
        elif key == ord('s'):  # s键
            self.save_frame(self.current_result_frame)
        elif key == ord('f'):  # f键
            self.flip_image = not self.flip_image
            print(f"图像翻转: {'开启' if self.flip_image else '关闭'}")
    
    def run(self):
        """运行扫描效果"""
        window_name = "扫描线效果"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, self.scaled_width, self.scaled_height)
        
        self.current_result_frame = None
        
        while self.running:
            if not self.paused:
                ret, current_frame = self.cap.read()
                if not ret:
                    # 如果是视频文件，则循环播放
                    if isinstance(self.video_source, str):
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        ret, current_frame = self.cap.read()
                        if not ret:
                            break
                    else:
                        break
                
                # 如果需要，水平翻转图像
                if self.flip_image:
                    current_frame = cv2.flip(current_frame, 1)
            
            # 创建扫描效果
            self.current_result_frame = self.create_scan_effect(current_frame)
            
            # 调整大小以适应显示窗口
            display_frame = self.resize_frame(self.current_result_frame)
            
            # 显示结果
            cv2.imshow(window_name, display_frame)
            
            # 更新扫描线位置
            self.update_scan_position()
            
            # 处理键盘事件
            key = cv2.waitKey(int(1000/self.fps)) & 0xFF
            self.process_key_event(key)
        
        # 释放资源
        self.cap.release()
        cv2.destroyAllWindows()

def parse_color(color_str):
    """解析颜色字符串为RGB元组"""
    try:
        r, g, b = map(int, color_str.split(','))
        return (r, g, b)
    except:
        raise argparse.ArgumentTypeError("颜色格式应为'R,G,B'")

def main():
    parser = argparse.ArgumentParser(description="视频扫描线效果")
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
        # 创建并运行扫描效果
        scan_effect = ScanEffect(
            video_source=video_source,
            direction=args.direction,
            speed=args.speed,
            line_width=args.line_width,
            line_color=args.line_color if isinstance(args.line_color, tuple) else parse_color(args.line_color),
            display_size=(args.display_width, args.display_height),
            flip_image=args.flip
        )
        scan_effect.run()
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main() 