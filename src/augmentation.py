import cv2
import numpy as np
import os

class ImageDegrader:
    """图像退化模拟器"""

    def blur(self, image, sigma=2.0):
        """高斯模糊：模拟对焦不清/运动模糊"""
        return cv2.GaussianBlur(image, (0, 0), sigma)

    def low_light(self, image, gamma=0.5):
        """低光照：模拟夜间、暗光环境"""
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)])
        return cv2.LUT(image.astype(np.uint8), table.astype(np.uint8))

    def tilt(self, image, angle=10):
        """倾斜：模拟拍摄角度不正"""
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        # 白色背景填充旋转后空白
        return cv2.warpAffine(image, M, (w, h), borderValue=(255, 255, 255))

    def noise(self, image, sigma=20):
        """高斯噪声：模拟传感器噪点、压缩失真"""
        noise = np.random.normal(0, sigma, image.shape)
        return np.clip(image + noise, 0, 255).astype(np.uint8)

    def occlusion(self, image, ratio=0.15):
        """局部遮挡：模拟污渍、手指、折叠"""
        h, w = image.shape[:2]
        img = image.copy()
        bh = int(h * ratio)
        bw = int(w * ratio)
        # 随机位置
        x = np.random.randint(0, max(1, w - bw))
        y = np.random.randint(0, max(1, h - bh))
        img[y:y+bh, x:x+bw] = 0  # 黑色遮挡块
        return img


def generate_degraded_dataset(raw_dir, output_dir):
    """批量生成退化样本"""
    os.makedirs(output_dir, exist_ok=True)
    degrader = ImageDegrader()

    # 定义退化配置：(后缀, 方法, 参数)
    degradations = [
        ("blur", degrader.blur, {"sigma": 2.0}),
        ("dark", degrader.low_light, {"gamma": 0.5}),
        ("tilt", degrader.tilt, {"angle": 10}),
        ("noise", degrader.noise, {"sigma": 20}),
        ("occlusion", degrader.occlusion, {"ratio": 0.15}),
    ]

    image_files = [f for f in os.listdir(raw_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
    total = len(image_files) * len(degradations)
    current = 0

    for img_name in sorted(image_files):
        img_path = os.path.join(raw_dir, img_name)
        img = cv2.imread(img_path)

        if img is None:
            print(f"✗ 读取失败: {img_name}")
            continue

        for suffix, method, kwargs in degradations:
            degraded = method(img, **kwargs)
            out_name = f"{os.path.splitext(img_name)[0]}_{suffix}.jpg"
            out_path = os.path.join(output_dir, out_name)
            cv2.imwrite(out_path, degraded)
            current += 1
            print(f"[{current}/{total}] 生成: {out_name}")

    print(f"\n✓ 完成！共生成 {current} 张退化图像，保存在: {output_dir}")


if __name__ == "__main__":
    generate_degraded_dataset(
        raw_dir="data/raw",
        output_dir="data/degraded"
    )