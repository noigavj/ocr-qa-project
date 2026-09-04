from paddleocr import PaddleOCR
import os


class OcrEngine:
    """OCR推理引擎封装"""

    def __init__(self, use_gpu=False):
        print("正在初始化 OCR 引擎...")
        self.ocr = PaddleOCR(
            use_angle_cls=True,  # 方向分类
            lang='ch',  # 中文模型
            show_log=False,  # 关闭冗余日志
            use_gpu=use_gpu  # CPU运行
        )
        print("✓ OCR 引擎就绪")

    def predict(self, image_path):
        """对单张图片推理，返回拼接后的完整文字"""
        if not os.path.exists(image_path):
            print(f"✗ 图片不存在: {image_path}")
            return ""

        result = self.ocr.ocr(image_path, cls=True)
        texts = []
        if result and result[0]:
            for line in result[0]:
                texts.append(line[1][0])
        return "".join(texts)

    def predict_with_detail(self, image_path):
        """返回文字 + 每行置信度列表"""
        if not os.path.exists(image_path):
            return "", []

        result = self.ocr.ocr(image_path, cls=True)
        texts = []
        confidences = []
        if result and result[0]:
            for line in result[0]:
                texts.append(line[1][0])
                confidences.append(round(line[1][1], 4))
        return "".join(texts), confidences