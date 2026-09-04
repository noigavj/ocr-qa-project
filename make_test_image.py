# 从PIL图像处理库导入3个工具：
# Image：创建、打开、保存图片
# ImageDraw：在图片上画画、写字
# ImageFont：设置文字的字体和大小
from PIL import Image, ImageDraw, ImageFont

# 创建一张空白图片：
# 格式是RGB彩色，尺寸宽600像素、高200像素，背景填充白色
img = Image.new('RGB', (600, 200), color='white')

# 创建一个「画笔」对象，后续用它在空白图片上绘制文字
draw = ImageDraw.Draw(img)

# 加载字体（三级兜底，确保中文能正常显示）
try:
    # 方式1：直接尝试加载微软雅黑字体文件，字号40
    font = ImageFont.truetype("msyh.ttc", 40)
except:
    try:
        # 方式2：方式1失败的话，用Windows系统字体的完整路径加载
        font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 40)
    except:
        # 方式3：都失败就用PIL自带的默认字体（可能不支持中文）
        font = ImageFont.load_default()

# 在图片上写文字：
# 坐标(50, 70) = 文字左上角距离图片左边界50像素、上边界70像素
# 文字内容："Hello PaddleOCR 测试文字"
# 文字颜色：黑色
# 使用刚才加载的字体
draw.text((50, 70), "Hello PaddleOCR 测试文字", fill='black', font=font)

# 把画好的图片保存为 test.jpg，存在当前文件夹里
img.save("test.jpg")

# 控制台打印提示，告诉你生成完成
print("已生成 test.jpg，保存在 E:\\Ocrpy\\")
