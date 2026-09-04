import json

with open("reports/test_raw.json", "r", encoding="utf-8") as f:
    result = json.load(f)

print(f"准确率: {result['avg_accuracy'] * 100:.2f}%")
print(f"完全匹配率: {result['exact_match_rate'] * 100:.2f}%")
