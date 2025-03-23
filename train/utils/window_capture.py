import sys
import cv2
import numpy as np
from PIL import Image

class WindowCapture:
    def __init__(self, window_name=None):
        self.window_name = window_name
        self.platform = sys.platform
        
        # 根据平台初始化捕获方式
        if self.platform == "darwin":
            self._init_mac()
        elif self.platform == "win32":
            self._init_win()
        else:
            raise NotImplementedError("Unsupported platform")

    def _init_mac(self):
        """macOS初始化"""
        from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionAll, kCGNullWindowID
        self.mac_lib = __import__('Quartz')
        
        # 获取窗口ID
        self.window_id = self._get_mac_window_id()

    def _init_win(self):
        """Windows初始化"""
        import win32gui
        self.win32gui = win32gui
        
        # 获取窗口句柄
        self.hwnd = self._get_win_window_handle()
        if not self.hwnd:
            raise Exception(f"Window '{self.window_name}' not found")

    def _get_mac_window_id(self):
        """获取macOS窗口ID"""
        from Quartz import (CGWindowListCopyWindowInfo, 
                          kCGWindowListOptionAll,
                          kCGNullWindowID)
        
        window_list = CGWindowListCopyWindowInfo(
            kCGWindowListOptionAll, kCGNullWindowID)
        for window in window_list:
            name = window.get('kCGWindowName', '')
            owner = window.get('kCGWindowOwnerName', '')
            if self.window_name.lower() in (name + owner).lower():
                return window['kCGWindowNumber']
        raise Exception(f"Window '{self.window_name}' not found")

    def _get_win_window_handle(self):
        """获取Windows窗口句柄"""
        def callback(hwnd, hwnd_list):
            if self.win32gui.IsWindowVisible(hwnd):
                title = self.win32gui.GetWindowText(hwnd)
                if self.window_name.lower() in title.lower():
                    hwnd_list.append(hwnd)
            return True
        
        hwnd_list = []
        self.win32gui.EnumWindows(callback, hwnd_list)
        return hwnd_list[0] if hwnd_list else None

    def get_frame(self):
        """获取当前窗口画面"""
        if self.platform == "darwin":
            return self._capture_mac()
        elif self.platform == "win32":
            return self._capture_win()

    def _capture_mac(self):
        """macOS捕获实现"""
        from Quartz import (CGWindowListCreateImage,
                          CGRectNull,
                          kCGWindowImageDefault,
                          kCGWindowImageBoundsIgnoreFraming,
                          kCGWindowImageShouldBeOpaque)
        
        # 捕获窗口区域
        cg_image = CGWindowListCreateImage(
            CGRectNull,
            self.mac_lib.kCGWindowListOptionIncludingWindow,
            self.window_id,
            kCGWindowImageBoundsIgnoreFraming | kCGWindowImageShouldBeOpaque
        )
        
        # 转换为OpenCV格式
        width = self.mac_lib.CGImageGetWidth(cg_image)
        height = self.mac_lib.CGImageGetHeight(cg_image)
        bytesperrow = self.mac_lib.CGImageGetBytesPerRow(cg_image)
        
        pixeldata = self.mac_lib.CGDataProviderCopyData(
            self.mac_lib.CGImageGetDataProvider(cg_image))
        
        # 检查 pixeldata 是否为 None
        if pixeldata is None:
            print("未能获取有效的窗口图像数据，请检查窗口是否存在或是否被遮挡。")
            return None
        
        np_data = np.frombuffer(pixeldata, dtype=np.uint8)
        cv_img = np_data.reshape((height, width, 4))  # RGBA格式
        # 修改颜色转换代码
        return cv2.cvtColor(cv_img, cv2.COLOR_RGBA2RGB)
    
    def _capture_win(self):
        """Windows捕获实现"""
        import win32ui
        import win32con
        
        # 获取窗口位置
        left, top, right, bottom = self.win32gui.GetClientRect(self.hwnd)
        w = right - left
        h = bottom - top

        # 创建设备上下文
        hwnd_dc = self.win32gui.GetWindowDC(self.hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        
        # 创建位图
        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
        save_dc.SelectObject(save_bitmap)
        
        # 复制画面
        save_dc.BitBlt((0, 0), (w, h), mfc_dc, (left, top), win32con.SRCCOPY)
        
        # 转换为OpenCV格式
        bmp_info = save_bitmap.GetInfo()
        bmp_str = save_bitmap.GetBitmapBits(True)
        img = np.frombuffer(bmp_str, dtype=np.uint8).reshape(
            (bmp_info["bmHeight"], bmp_info["bmWidth"], 4))
        # 修改颜色转换代码
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        
        # 清理资源
        self.win32gui.DeleteObject(save_bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        self.win32gui.ReleaseDC(self.hwnd, hwnd_dc)
        return img