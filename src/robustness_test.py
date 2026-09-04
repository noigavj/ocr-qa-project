import os
import sys
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.base_tester import BaseTester


def run_robustness_test():
    print("=" * 50)
    print("鲁棒性测试 - 退化场景识别稳定性验证")
    print("=" * 50)

    tester = BaseTester()
    gt = tester.load_ground_truth("data/ground_truth.json")

    # 5种退化场景
    degradations = {
        "blur": "模糊",
        "dark": "低光照",
        "tilt": "倾斜",
        "noise": "噪声",
        "occlusion": "遮挡"
    }

    overall = {}

    for suffix, name in degradations.items():
        print(f"\n{'=' * 50}")
        print(f">>> 场景: {name} ({suffix})")
        print(f"{'=' * 50}")

        # 构建退化图与真值的映射
        # 退化图命名: doc_01_blur.jpg -> 原图 doc_01.jpg
        degraded_gt = {}
        degraded_dir = os.path.join(PROJECT_ROOT, "data", "degraded")

        for img_name in os.listdir(degraded_dir):
            if img_name.endswith(f"_{suffix}.jpg"):
                original_name = img_name.replace(f"_{suffix}.jpg", ".jpg")
                if original_name in gt:
                    degraded_gt[img_name] = gt[original_name]

        if not degraded_gt:
            print(f"未找到 {suffix} 样本，跳过")
            continue

        print(f"样本数: {len(degraded_gt)}")

        summary = tester.run_batch(
            image_dir="data/degraded",
            gt_dict=degraded_gt,
            output_report=f"reports/robustness_{suffix}_report.json"
        )

        overall[name] = {
            "sample_count": summary["valid"],
            "avg_accuracy": summary["avg_accuracy"],
            "exact_match_rate": summary["exact_match_rate"]
        }

    # 汇总报告
    summary_path = os.path.join(PROJECT_ROOT, "reports", "robustness_summary.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(overall, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 50}")
    print("鲁棒性测试汇总")
    print(f"{'=' * 50}")
    for name, data in overall.items():
        print(
            f"  {name:8s}: 准确率 {data['avg_accuracy'] * 100:6.2f}% | 完全匹配 {data['exact_match_rate'] * 100:6.2f}%")
    print(f"\n汇总报告: reports/robustness_summary.json")


if __name__ == "__main__":
    run_robustness_test()