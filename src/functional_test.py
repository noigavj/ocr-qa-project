import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.base_tester import BaseTester


def run_functional_test():
    print("=" * 50)
    print("功能测试 - 标准场景识别能力验证")
    print("=" * 50)

    tester = BaseTester()
    gt = tester.load_ground_truth("data/ground_truth.json")

    summary = tester.run_batch(
        image_dir="data/raw",
        gt_dict=gt,
        output_report="reports/functional_report.json"
    )

    return summary


if __name__ == "__main__":
    run_functional_test()