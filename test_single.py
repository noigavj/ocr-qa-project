import os
import json
from src.ocr_engine import OcrEngine
from src.metrics import OcrMetrics

print("=" * 50)
print("单图测试验证")
print("=" * 50)

engine = OcrEngine()
metrics = OcrMetrics()

# 测试第一张图
img_name = "doc_01.jpg"
img_path = os.path.join("data", "raw", img_name)

if not os.path.exists(img_path):
    print(f"✗ 找不到 {img_path}")
    exit(1)

print(f"\n图片: {img_path}")
pred, confs = engine.predict_with_detail(img_path)
print(f"识别结果: {pred}")
if confs:
    print(f"平均置信度: {sum(confs)/len(confs):.4f}")

# 读取真值
with open(os.path.join("data", "ground_truth.json"), 'r', encoding='utf-8') as f:
    gt = json.load(f)

gt_text = gt.get(img_name, "")
print(f"真值: {gt_text}")

result = metrics.compute_all(pred, gt_text)
print(f"\n指标计算:")
print(f"  编辑距离: {result['edit_distance']}")
print(f"  字符准确率: {result['char_accuracy']*100:.2f}%")
print(f"  完全匹配: {'是' if result['exact_match'] else '否'}")

print("\n✓ 单图验证通过！框架运行正常。")