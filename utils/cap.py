import cv2
import numpy as np
from threading import Thread, Lock
import time
from datetime import datetime

# 配置参数
DEVICE_IDS = [1, 2, 3]      # 摄像头设备索引列表
MAX_FPS = 20                   # 最大处理帧率
# 定义期望的分辨率
# SINGLE_F_WIDTH = 1280
# SINGLE_F_HEIGHT = 720
SINGLE_F_WIDTH = 1920
SINGLE_F_HEIGHT = 1080

class CameraStream:
    def __init__(self, device_id):
        self.device_id = device_id
        self.frame = None
        self.lock = Lock()
        self.running = False
        self.last_update = time.time()
        self.retry_count = 0
        
        # 初始化摄像头
        self.cap = cv2.VideoCapture(device_id, cv2.CAP_DSHOW)
        # 设置摄像头的宽度和高度
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, SINGLE_F_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, SINGLE_F_HEIGHT)

        if not self.cap.isOpened():
            raise RuntimeError(f"无法打开设备 {device_id}")
            
        # 自动适配最佳分辨率
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # print(f"设备 {device_id} 实际分辨率: 宽度 {self.width} 像素, 高度 {self.height} 像素")

    def start(self):
        self.running = True
        Thread(target=self.update, daemon=True).start()

    def update(self):
        frame_time = 1 / MAX_FPS  # 每帧的时间间隔
        next_frame_time = time.time() + frame_time
        while self.running:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    self.retry_count += 1
                    if self.retry_count > 5:
                        self.reconnect()
                    continue
                
                with self.lock:
                    self.frame = frame
                    self.last_update = time.time()
                    self.retry_count = 0
                    
                # 控制帧率
                # time.sleep(1/MAX_FPS)
                current_time = time.time()
                if current_time < next_frame_time:
                    time.sleep(next_frame_time - current_time)
                next_frame_time = current_time + frame_time       

            except Exception as e:
                print(f"设备 {self.device_id} 错误: {str(e)}")
                self.reconnect()

    def reconnect(self):
        self.cap.release()
        time.sleep(1)
        self.cap = cv2.VideoCapture(self.device_id, cv2.CAP_DSHOW)
        self.retry_count = 0

    def read(self):
        with self.lock:
            if self.frame is None or (time.time() - self.last_update) > 1:
                return None
            return self.frame.copy()

    def release(self):
        self.running = False
        self.cap.release()

def resize_keep_aspect(frame, SINGLE_F_HEIGHT):
    h, w = frame.shape[:2]
    scale = SINGLE_F_HEIGHT / h
    resized = cv2.resize(frame, (int(w*scale), SINGLE_F_HEIGHT))
    # print(f"调整后帧的尺寸: 宽度 {resized.shape[1]} 像素, 高度 {resized.shape[0]} 像素")
    return resized

def get_frame():
    # 初始化所有摄像头
    streams = []
    for dev_id in DEVICE_IDS:
        try:
            stream = CameraStream(dev_id)
            stream.start()
            streams.append(stream)
        except Exception as e:
            print(f"设备 {dev_id} 初始化失败: {str(e)}")
            streams.append(None)

    # 修改视频写入器初始化部分
    fourcc = cv2.VideoWriter_fourcc(*'avc1')  # 使用更兼容的编码器
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f'output_{current_time}.mp4'
    video_writer = None
    frame_count = 0

    try:
        while True:
            start_time = time.time()
            frames = []
            valid_frames = 0
            
            # 读取所有摄像头
            for i, stream in enumerate(streams):
                if stream is None:
                    frames.append(np.zeros((SINGLE_F_HEIGHT, SINGLE_F_WIDTH, 3), dtype=np.uint8))  # 使用固定宽度
                    continue
                    
                frame = stream.read()
                if frame is None:
                    frames.append(np.zeros((SINGLE_F_HEIGHT, SINGLE_F_WIDTH, 3), dtype=np.uint8))  # 使用固定宽度
                    continue
                
                resized = resize_keep_aspect(frame, SINGLE_F_HEIGHT)
                frames.append(resized)
                valid_frames += 1

            # 横向拼接
            combined = cv2.hconcat(frames) if len(frames) > 0 else np.zeros((100,100,3))

            height, width, channels = combined.shape
            # print(f"拼接后帧的尺寸: 宽度 {width} 像素, 高度 {height} 像素")

            # 初始化视频写入器
            if video_writer is None:
                print(f"正在创建视频文件，分辨率: {width}x{height}")
                video_writer = cv2.VideoWriter(output_filename, fourcc, MAX_FPS, (width, height))
                if not video_writer.isOpened():
                    print(f"视频写入器初始化失败，请检查：")
                    print(f"1. 输出路径权限: {output_filename}")
                    print(f"2. 分辨率支持: {width}x{height}")
                    print(f"3. 编码器兼容性: MJPG")
                    break

            # 修改帧写入逻辑
            cv2.imwrite("debug_frame.jpg", combined)
            write_success = video_writer.write(combined)
            if write_success:
                frame_count += 1
                print(f"已写入 {frame_count} 帧 ({(frame_count/MAX_FPS):.1f} 秒)")
            # else:
                # print(f"帧写入失败！当前帧尺寸: {combined.shape}")

            # 精确控制帧率（新增）
            processing_time = time.time() - start_time
            sleep_time = max(0, (1/MAX_FPS) - processing_time)
            time.sleep(sleep_time)

            cv2.namedWindow("TC-400N4", cv2.WINDOW_NORMAL)

            # 获取屏幕尺寸
            screen_width = cv2.getWindowImageRect("TC-400N4")[2]
            screen_height = cv2.getWindowImageRect("TC-400N4")[3]

            # 计算缩放比例
            scale = min(screen_width / width, screen_height / height)
            new_width = int(width * scale)
            new_height = int(height * scale)

            # 缩放图像
            resized_combined = cv2.resize(combined, (new_width, new_height))

            cv2.resizeWindow("TC-400N4", new_width, new_height)

            cv2.imshow("TC-400N4", resized_combined)

            # 获取窗口尺寸
            x, y, win_width, win_height = cv2.getWindowImageRect("TC-400N4")
            # print(f"窗口 'TC-400N4' 的尺寸: 宽度 {win_width} 像素, 高度 {win_height} 像素")

            # 退出控制
            key = cv2.waitKey(1)
            if key == ord('q') or cv2.getWindowProperty("TC-400N4", cv2.WND_PROP_VISIBLE) < 1:
                break

    except Exception as e:
        print(f"发生异常: {str(e)}")
    finally:
        # 释放视频写入器
        if video_writer is not None:
            try:
                video_writer.release()
                print("视频写入器已成功释放")
            except Exception as e:
                print(f"释放视频写入器时出错: {str(e)}")
        for stream in streams:
            if stream is not None:
                stream.release()
        cv2.destroyAllWindows()

        # 输出最终帧数和时长
        if frame_count > 0:
            duration = frame_count / MAX_FPS
            print(f"视频时长: {duration:.2f} 秒，总帧数: {frame_count}")
        else:
            print("未成功写入任何帧")

if __name__ == "__main__":
    get_frame()