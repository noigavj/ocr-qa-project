import json
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def compare_reports(old_path, new_path, output_path):
    """对比两个版本的测试报告"""
    print("=" * 50)
    print("回归测试 - 版本效果对比")
    print("=" * 50)

    with open(os.path.join(PROJECT_ROOT, old_path), 'r', encoding='utf-8') as f:
        old = json.load(f)
    with open(os.path.join(PROJECT_ROOT, new_path), 'r', encoding='utf-8') as f:
        new = json.load(f)

    comparison = {
        "old_version": {
            "avg_accuracy": old.get("avg_accuracy", 0),
            "exact_match_rate": old.get("exact_match_rate", 0)
        },
        "new_version": {
            "avg_accuracy": new.get("avg_accuracy", 0),
            "exact_match_rate": new.get("exact_match_rate", 0)
        },
        "delta_accuracy": round(new.get("avg_accuracy", 0) - old.get("avg_accuracy", 0), 4),
        "delta_exact_match": round(new.get("exact_match_rate", 0) - old.get("exact_match_rate", 0), 4),
        "status": "PASS" if new.get("avg_accuracy", 0) >= old.get("avg_accuracy", 0) else "REGRESSION"
    }

    print(f"\n对比结果:")
    print(f"  旧版准确率: {comparison['old_version']['avg_accuracy'] * 100:.2f}%")
    print(f"  新版准确率: {comparison['new_version']['avg_accuracy'] * 100:.2f}%")
    print(f"  变化:        {comparison['delta_accuracy'] * 100:+.2f}%")
    print(f"  结论:        {comparison['status']}")

    out_full = os.path.join(PROJECT_ROOT, output_path)
    with open(out_full, 'w', encoding='utf-8') as f:
        json.dump(comparison, f, ensure_ascii=False, indent=2)

    print(f"\n报告保存: {output_path}")
    return comparison


if __name__ == "__main__":
    import shutil

    # 演示：把当前功能测试报告复制一份模拟"旧版本"
    # 实际场景中，old 是上个版本的报告，new 是当前版本
    old_file = os.path.join(PROJECT_ROOT, "reports", "v1_functional_report.json")
    new_file = os.path.join(PROJECT_ROOT, "reports", "functional_report.json")

    if os.path.exists(new_file) and not os.path.exists(old_file):
        shutil.copy(new_file, old_file)
        print("已复制当前报告作为'旧版本'基准")

    if os.path.exists(old_file) and os.path.exists(new_file):
        compare_reports(
            "reports/v1_functional_report.json",
            "reports/functional_report.json",
            "reports/regression_comparison.json"
        )
    else:
        print("缺少对比文件，请先完成功能测试")