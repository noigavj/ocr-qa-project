import xml.etree.ElementTree as ET
import json
import os


def parse_voc_xml(xml_path):
    """解析 PascalVOC XML，提取所有 object/name 拼接为完整文字"""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    texts = []
    for obj in root.findall('object'):
        name_elem = obj.find('name')
        if name_elem is not None and name_elem.text:
            texts.append(name_elem.text.strip())

    # 用空格连接多个框的文字
    return ' '.join(texts)


def build_ground_truth(raw_dir, anno_dir, output_file):
    gt_dict = {}

    for img_name in sorted(os.listdir(raw_dir)):
        if not img_name.endswith(('.jpg', '.jpeg', '.png')):
            continue

        base_name = os.path.splitext(img_name)[0]
        xml_path = os.path.join(anno_dir, base_name + '.xml')

        if os.path.exists(xml_path):
            full_text = parse_voc_xml(xml_path)
            gt_dict[img_name] = full_text
            print(f"✓ {img_name}: {full_text[:40]}...")
        else:
            print(f"✗ {img_name}: 未找到对应 XML，跳过")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(gt_dict, f, ensure_ascii=False, indent=2)

    print(f"\n共处理 {len(gt_dict)} 张图像")
    print(f"真值文件保存至: {output_file}")


if __name__ == "__main__":
    build_ground_truth(
        raw_dir="data/raw",
        anno_dir="data/annotations",
        output_file="data/ground_truth.json"
    )