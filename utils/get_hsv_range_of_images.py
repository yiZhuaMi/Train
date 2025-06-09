import cv2
import numpy as np
import os


def get_hsv_range(image_folder, prefix):
    h_list, s_list, v_list = [], [], []

    for filename in os.listdir(image_folder):
        if filename.startswith(prefix):
            img = cv2.imread(os.path.join(image_folder, filename))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # 掩膜：排除黑色像素（V < 15 且 S < 15）
            mask = (hsv[:, :, 2] > 15) | (hsv[:, :, 1] > 15)
            hsv_non_black = hsv[mask]

            if len(hsv_non_black) > 0:
                h, s, v = hsv_non_black.T
                h_list.extend(h)
                s_list.extend(s)
                v_list.extend(v)

    if not h_list:
        return None

    h_min, h_max = np.min(h_list), np.max(h_list)
    s_min, s_max = np.min(s_list), np.max(s_list)
    v_min, v_max = np.min(v_list), np.max(v_list)

    return {
        'H': (int(h_min), int(h_max)),
        'S': (int(s_min), int(s_max)),
        'V': (int(v_min), int(v_max))
    }


# 假设图片存放在当前目录的 images 文件夹中
image_folder = "../image/rail_line_hsv"
prefixes = ['r', 'g', 'w']

for prefix in prefixes:
    hsv_range = get_hsv_range(image_folder, prefix)
    if hsv_range:
        print(f"Class '{prefix}' HSV Range (non-black pixels):")
        print(f"H: {hsv_range['H']}")
        print(f"S: {hsv_range['S']}")
        print(f"V: {hsv_range['V']}")
        print()
    else:
        print(f"Class '{prefix}' has no valid non-black pixels.")