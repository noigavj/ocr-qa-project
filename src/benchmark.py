import time
import statistics
import json
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from src.ocr_engine import OcrEngine


def benchmark_inference(image_path, runs=30):
    """性能基准测试：单图多次推理，统计耗时分布"""
    print("=" * 50)
    print("性能测试 - 推理耗时基准")
    print("=" * 50)

    full_path = os.path.join(PROJECT_ROOT, image_path)
    if not os.path.exists(full_path):
        print(f"✗ 图片不存在: {full_path}")
        return None

    engine = OcrEngine()

    # 预热（排除首次加载干扰）
    print("预热中...")
    engine.predict(full_path)

    # 正式测试
    times = []
    print(f"开始测试: {runs} 轮推理")
    for i in range(runs):
        start = time.perf_counter()
        engine.predict(full_path)
        elapsed = (time.perf_counter() - start) * 1000  # 转毫秒
        times.append(elapsed)

    report = {
        "image": image_path,
        "runs": runs,
        "avg_ms": round(statistics.mean(times), 2),
        "min_ms": round(min(times), 2),
        "max_ms": round(max(times), 2),
        "median_ms": round(statistics.median(times), 2),
        "p95_ms": round(sorted(times)[int(runs * 0.95)], 2),
        "p99_ms": round(sorted(times)[int(runs * 0.99)], 2),
        "std_ms": round(statistics.stdev(times), 2) if len(times) > 1 else 0
    }

    print(f"\n结果:")
    print(f"  平均耗时: {report['avg_ms']} ms")
    print(f"  中位数:   {report['median_ms']} ms")
    print(f"  P95:      {report['p95_ms']} ms")
    print(f"  P99:      {report['p99_ms']} ms")
    print(f"  标准差:   {report['std_ms']} ms")

    return report


if __name__ == "__main__":
    os.makedirs(os.path.join(PROJECT_ROOT, "reports"), exist_ok=True)

    # 用 doc_01.jpg 做基准
    report = benchmark_inference("data/raw/doc_01.jpg", runs=30)

    if report:
        out_path = os.path.join(PROJECT_ROOT, "reports", "benchmark_report.json")
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n报告保存: reports/benchmark_report.json")