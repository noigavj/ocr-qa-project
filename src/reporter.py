import json
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.pyplot as plt

# ==========增加中文支持配置==========
plt.rcParams["font.family"] = ["SimHei"]  # 黑体，Windows自带
plt.rcParams["axes.unicode_minus"] = False # 解决负号显示方块
# ====================================

# 下面是你原来画图代码

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestReporter:
    def __init__(self):
        self.fig_dir = os.path.join(PROJECT_ROOT, "reports", "figures")
        os.makedirs(self.fig_dir, exist_ok=True)

    def plot_radar(self, summary_path, output_name):
        """鲁棒性雷达图"""
        with open(os.path.join(PROJECT_ROOT, summary_path), 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 读取功能测试作为基准
        func_path = os.path.join(PROJECT_ROOT, "reports", "functional_report.json")
        func_acc = 0.61  # 默认值
        if os.path.exists(func_path):
            with open(func_path, 'r', encoding='utf-8') as f:
                func = json.load(f)
                func_acc = func.get("avg_accuracy", 0.61)

        categories = ["标准场景"] + list(data.keys())
        values = [func_acc] + [data[k]["avg_accuracy"] for k in data.keys()]

        # 雷达图需要闭合
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        values_plot = values + values[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        ax.plot(angles, values_plot, 'o-', linewidth=2, color='#2E86AB', label='准确率')
        ax.fill(angles, values_plot, alpha=0.25, color='#2E86AB')
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=11)
        ax.set_ylim(0, 1)
        ax.set_title("OCR 算法鲁棒性评估雷达图", fontsize=15, pad=20)
        ax.grid(True, linestyle='--', alpha=0.7)

        out_path = os.path.join(self.fig_dir, output_name)
        plt.tight_layout()
        plt.savefig(out_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"✓ 雷达图已保存: reports/figures/{output_name}")

    def plot_bar(self, summary_path, output_name):
        """准确率柱状图对比"""
        with open(os.path.join(PROJECT_ROOT, summary_path), 'r', encoding='utf-8') as f:
            data = json.load(f)

        categories = list(data.keys())
        values = [data[k]["avg_accuracy"] * 100 for k in categories]

        # 颜色：低于50%红色，50-60%橙色，高于60%绿色
        colors = ['#C73E1D' if v < 50 else '#F18F01' if v < 60 else '#2E86AB' for v in values]

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(categories, values, color=colors, edgecolor='black', linewidth=1.2, width=0.6)

        ax.set_ylabel("字符准确率 (%)", fontsize=12)
        ax.set_title("各退化场景 OCR 识别准确率对比", fontsize=14)
        ax.set_ylim(0, 100)
        ax.axhline(y=60, color='green', linestyle='--', alpha=0.5, label='基准线(60%)')
        ax.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='预警线(50%)')
        ax.legend(loc='upper right')

        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                    f"{val:.1f}%", ha='center', va='bottom', fontsize=11, fontweight='bold')

        out_path = os.path.join(self.fig_dir, output_name)
        plt.tight_layout()
        plt.savefig(out_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"✓ 柱状图已保存: reports/figures/{output_name}")


if __name__ == "__main__":
    reporter = TestReporter()
    reporter.plot_radar("reports/robustness_summary.json", "radar_chart.png")
    reporter.plot_bar("reports/robustness_summary.json", "accuracy_bar.png")
    print("\n✓ 全部可视化报告生成完毕")