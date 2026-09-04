import json

with open("reports/test_raw.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 60)
print("错误样例分析（准确率 < 80% 或完全未匹配）")
print("=" * 60)

count = 0
for item in data["details"]:
    acc = item["char_accuracy"]
    if acc < 0.8 or not item["exact_match"]:
        count += 1
        if count > 10:  # 只看前10个
            print("\n... 仅展示前10条")
            break
        print(f"\n图片: {item['image']}")
        print(f"  真值: [{item['gt']}]")
        print(f"  预测: [{item['pred']}]")
        print(f"  准确率: {acc*100:.1f}%")

print(f"\n共 {count} 张有问题（仅显示前10张）")