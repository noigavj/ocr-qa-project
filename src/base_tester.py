import os
import sys
import json

# 自动定位项目根目录（兼容任意路径运行）
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.ocr_engine import OcrEngine
from src.metrics import OcrMetrics
from tqdm import tqdm


class BaseTester:
    """批量测试执行器"""

    def __init__(self):
        self.engine = OcrEngine()
        self.metrics = OcrMetrics()

    def load_ground_truth(self, gt_path):
        """加载真值 JSON"""
        full_path = os.path.join(PROJECT_ROOT, gt_path)
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def run_batch(self, image_dir, gt_dict, output_report):
        """
        批量测试并生成报告
        image_dir: 图片文件夹（相对根目录）
        gt_dict: {图片名: 真值文字}
        output_report: 报告输出路径（相对根目录）
        """
        report_path = os.path.join(PROJECT_ROOT, output_report)
        os.makedirs(os.path.dirname(report_path), exist_ok=True)

        results = []
        image_dir_full = os.path.join(PROJECT_ROOT, image_dir)
        image_files = [f for f in os.listdir(image_dir_full)
                       if f.endswith(('.jpg', '.jpeg', '.png'))]

        print(f"开始测试: {len(image_files)} 张图片")

        for img_name in tqdm(sorted(image_files), desc="Testing"):
            if img_name not in gt_dict:
                continue

            img_path = os.path.join(image_dir_full, img_name)
            gt_text = gt_dict[img_name]

            try:
                pred_text = self.engine.predict(img_path)
                metric = self.metrics.compute_all(pred_text, gt_text)
                metric["image"] = img_name
                results.append(metric)
            except Exception as e:
                print(f"\n✗ 错误 {img_name}: {e}")
                results.append({
                    "image": img_name,
                    "error": str(e),
                    "char_accuracy": 0,
                    "exact_match": False
                })

        # 汇总统计
        valid = [r for r in results if "error" not in r]
        summary = {
            "total": len(results),
            "valid": len(valid),
            "avg_accuracy": round(sum(r["char_accuracy"] for r in valid) / len(valid), 4) if valid else 0,
            "exact_match_rate": round(sum(r["exact_match"] for r in valid) / len(valid), 4) if valid else 0,
            "details": results
        }

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        print(f"\n{'=' * 50}")
        print("测试完成")
        print(f"  总样本: {summary['total']}")
        print(f"  平均字符准确率: {summary['avg_accuracy'] * 100:.2f}%")
        print(f"  完全匹配率: {summary['exact_match_rate'] * 100:.2f}%")
        print(f"  报告保存: {output_report}")
        return summary


if __name__ == "__main__":
    tester = BaseTester()
    gt = tester.load_ground_truth("data/ground_truth_clean.json")
    tester.run_batch("data/raw", gt, "reports/test_raw.json")