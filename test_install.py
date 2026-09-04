# 导入PaddleOCR的核心识别类
from paddleocr import PaddleOCR
# 导入OpenCV，用来读取图片文件
import cv2
# 导入系统模块，用来检查文件是否存在
import os

# 打印标题分割线，让输出更整齐
print("=" * 50)
print("PaddleOCR 安装验证")
print("=" * 50)

# 第一步：先检查当前目录下有没有测试图片 test.jpg
if not os.path.exists("test.jpg"):
    print("错误：找不到 test.jpg")
    exit(1)  # 找不到就直接退出程序

print("\n[1/3] 正在初始化 OCR 引擎...")
print("    （首次运行会自动下载模型，约 100MB，需要 2-5 分钟）")
try:
    # 创建OCR识别器，配置4个参数：
    ocr = PaddleOCR(
        use_angle_cls=True,      # 开启方向检测：图片歪了也能识别
        lang='ch',               # 识别语言：中文
        show_log=False,          # 关闭运行日志，输出更干净
        use_gpu=False            # 用CPU运行，不用显卡
    )
    print("    ✓ OCR 引擎初始化成功")
except Exception as e:
    # 初始化失败就打印错误并退出
    print(f"    ✗ 初始化失败: {e}")
    exit(1)

print("\n[2/3] 正在读取图片...")
# 用OpenCV读取test.jpg图片，读取后是像素数组
img = cv2.imread("test.jpg")
# 判断图片是否读取成功（失败会返回空值None）
if img is None:
    print("    ✗ 图片读取失败")
    exit(1)
# 打印图片尺寸：格式为(高度, 宽度, 颜色通道数)
print(f"    ✓ 图片尺寸: {img.shape}")

print("\n[3/3] 正在执行 OCR 推理...")
try:
    # 执行OCR识别，cls=True表示启用方向分类
    result = ocr.ocr("test.jpg", cls=True)

    # 判断是否识别到了文字
    if result and result[0]:
        print(f"\n✓ 识别成功！共识别到 {len(result[0])} 行文字：")
        print("-" * 50)
        # 逐行打印识别结果
        for idx, line in enumerate(result[0], 1):
            text = line[1][0]       # line[1][0] = 识别出的文字内容
            confidence = line[1][1] # line[1][1] = 置信度（0~1，越高越准）
            print(f"  {idx}. {text}")
            print(f"     置信度: {confidence:.4f}")
        print("-" * 50)
        print("\n🎉 Day 1 完成！环境搭建成功！")
    else:
        print("⚠ 未识别到文字")

except Exception as e:
    # 识别出错的话，打印错误详情
    print(f"    ✗ 识别失败: {e}")
    import traceback
    traceback.print_exc()
