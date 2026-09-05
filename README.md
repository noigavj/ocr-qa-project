# 📄 OCR 算法效果验证与自动化回归测试方案

基于 PaddleOCR 的文档图像文字识别算法 QA 方案，覆盖功能测试、鲁棒性测试、性能基准测试与版本回归测试。

## ✨ 使用前准备
---

首次使用需要配置 Python 运行环境（一次性操作）：

1. 克隆项目到本地，进入项目根目录
2. 创建 Python 虚拟环境并激活
3. 执行依赖安装命令，等待安装完成
4. 将测试图片放入 `data/raw/` 目录，准备真值标注

推荐镜像源：
- 清华镜像：https://pypi.tuna.tsinghua.edu.cn/simple（国内速度最快）
- 阿里镜像：https://mirrors.aliyun.com/pypi/simple
- 中科大镜像：https://pypi.mirrors.ustc.edu.cn/simple
- PyPI 官方：https://pypi.org/simple

## 📁 功能说明
---

| 模块 | 说明 |
| :---: | :--- |
| 功能测试 | 50 张标准原始样本，输出字符准确率、完全匹配率基线 |
| 鲁棒性测试 | 5 类图像退化场景，量化算法在复杂环境下的抗干扰能力 |
| 性能基准测试 | 30 轮重复推理，统计平均耗时、P95、P99 性能指标 |
| 版本回归测试 | 双版本结果对比，输出准确率差值与回归判定结果 |
| 图像退化模拟 | 支持模糊、低光、倾斜、噪声、遮挡 5 种数据增强方式 |
| 可视化报告 | 自动生成柱状图、雷达图与结构化 JSON 测试报告 |
| 批量执行器 | 一键顺序执行全部测试，无需逐条运行脚本 |
| 真值管理 | 统一 ground_truth.json 格式，支持批量导入标注数据 |

## 🚀 快速开始
---

### 1. 克隆项目

git clone https://github.com/noigavj/ocr-qa-project.git
cd ocr-qa-project

### 2. 创建虚拟环境

#### Windows

python -m venv venv
venv\Scripts\activate

#### Mac / Linux

python -m venv venv
source venv/bin/activate

### 3. 安装依赖

推荐使用清华镜像源加速国内安装：

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

### 4. 准备测试数据

1. 将原始测试图像放入 `data/raw/` 目录
2. 执行图像退化脚本，自动生成 5 类增强测试样本：

python src/augmentation.py

### 5. 执行测试

可按需选择执行对应测试脚本：

| 命令 | 说明 |
| :--- | :--- |
| python src/functional_test.py | 功能测试 - 标准场景基线准确率 |
| python src/robustness_test.py | 鲁棒性测试 - 5 类退化场景效果 |
| python src/benchmark.py |	性能基准测试 - 推理耗时统计 |
| python src/regression_test.py | 回归测试 - 版本对比验证 |

### 6. 生成可视化报告

全部测试完成后，执行脚本生成结构化报告与图表：

python src/reporter.py

## 🛠️ 技术栈
---

| 分类 | 说明 |
| :---: | :--- |
| OCR 引擎 | PaddleOCR PP-OCRv4 |
| 图像处理 | OpenCV 4.8+ |
| 开发语言 | Python 3.10 |
| 可视化 | Matplotlib 3.7+ |
| 评估指标 | Levenshtein 编辑距离、字符级准确率、完全匹配率 |
| 版本管理 | Git |

## ⚙️ 参数配置表
---

| 参数项 | 默认值 | 说明 |
| :---: | :---: | :--- |
| 模糊程度 | 3 | 高斯模糊核大小，数值越大越模糊 |
| 噪声强度 | 0.05 | 椒盐噪声占比 |
| 倾斜角度 | ±15° | 随机旋转角度范围 |
| 推理批次 | 1 | 批量推理图片数量 |

## License
---

MIT License
