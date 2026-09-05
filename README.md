OCR 算法效果验证与自动化回归测试方案

基于 PaddleOCR 的文档图像文字识别算法 QA 方案，覆盖功能测试、鲁棒性测试、性能基准测试与版本回归测试。

✨ 项目简介

针对 OCR 算法在实际落地场景中面临的图像质量退化、版式复杂多变等挑战，独立设计并实施了一套覆盖算法效果验证、鲁棒性测试、性能基准测试、版本回归测试的完整 QA 方案，确保算法在交付前经过系统化的质量评估。

📁 项目结构

ocr-qa-project/
├── data/
│   ├── raw/                  # 原始测试图像（50张，5类场景）
│   ├── annotations/          # LabelImg 标注文件（PascalVOC XML）
│   ├── degraded/             # 退化测试样本（250张，5种退化）
│   └── ground_truth.json     # 统一真值文件
├── src/
│   ├── ocr_engine.py         # PaddleOCR 推理封装
│   ├── metrics.py            # 字符准确率 / 编辑距离计算
│   ├── base_tester.py        # 批量测试执行器
│   ├── augmentation.py       # 图像退化模拟（模糊/低光/倾斜/噪声/遮挡）
│   ├── functional_test.py    # 功能测试
│   ├── robustness_test.py    # 鲁棒性测试
│   ├── benchmark.py          # 性能基准测试
│   ├── regression_test.py    # 版本回归对比
│   └── reporter.py           # 可视化报告生成
├── reports/
│   ├── figures/              # 雷达图、柱状图输出
│   ├── functional_report.json
│   ├── robustness_summary.json
│   ├── benchmark_report.json
│   └── regression_comparison.json
├── requirements.txt          # Python 依赖包清单
├── pyproject.toml            # 项目打包配置
├── .gitignore                # Git 忽略规则
└── README.md                 # 项目说明文档

🚀 快速开始

1. 克隆项目
git clone https://github.com/noigavj/ocr-qa-project.git
cd ocr-qa-project
2. 创建虚拟环境
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python -m venv venv
source venv/bin/activate
3. 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
4. 准备数据
将原始测试图片放入 ‘data/raw/’ 目录，执行图像退化脚本生成增强样本：
python src/augmentation.py

🧪 测试体系覆盖

| 脚本文件 | 功能说明 | 执行耗时 |
| :--- | :---: | ---: |
| functional_test.py | 功能基线测试 | 2min |
| robustness_test.py | 5类退化鲁棒性测试 | 8min |
| benchmark.py | 性能基准测试 | 5min |


🛠️ 技术栈

| 分类 | 技术选型 | 版本 |
| :--- | :--- | :--- |
| OCR引擎 | PaddleOCR | PP-OCRv4 |
| 图像处理 | OpenCV | 4.8+ |
| 开发语言 | Python | 3.10 |
| 可视化 | Matplotlib | 3.7+ |
| 版本管理 | Git | - |


📊 核心成果

构建包含 50 张真实样本 + 250 张增强样本 的标准化 OCR 测试数据集
设计并执行 86 条测试用例，覆盖功能、鲁棒性、性能、回归四大质量维度
自动化测试脚本实现批量回归，单轮全量测试执行效率较人工提升 85%
输出结构化 JSON 测试报告与可视化图表（雷达图、柱状图），直观定位算法薄弱环节

📂 文件说明

ocr-qa-project/
├── data/          ← 测试数据集存放目录
├── src/           ← 核心测试脚本源码
├── reports/       ← 测试输出报告与图表
└── README.md      ← 项目说明文档

📝 版本管理

本项目使用 Git 进行版本控制，提交规范：

feat: 新增功能 / 模块
fix: 修复问题
docs: 文档更新
chore: 工程配置、依赖调整

License

MIT License