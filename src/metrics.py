# 优先用 C 加速的 Levenshtein，如果没装则用纯 Python 备选
try:
    import Levenshtein


    def _edit_distance(a, b):
        return Levenshtein.distance(a, b)
except ImportError:
    # 纯 Python 动态规划实现（兼容中文）
    def _edit_distance(a, b):
        m, n = len(a), len(b)
        if m < n:
            m, n = n, m
            a, b = b, a
        prev = list(range(n + 1))
        for i in range(1, m + 1):
            curr = [i] + [0] * n
            for j in range(1, n + 1):
                cost = 0 if a[i - 1] == b[j - 1] else 1
                curr[j] = min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost)
            prev = curr
        return prev[n]


class OcrMetrics:
    """OCR 效果评估指标"""

    @staticmethod
    def char_accuracy(pred, gt):
        """字符级准确率 = 1 - 编辑距离 / 最大长度"""
        if not gt:
            return 1.0 if not pred else 0.0
        dist = _edit_distance(pred, gt)
        max_len = max(len(pred), len(gt))
        return max(0.0, 1.0 - dist / max_len) if max_len > 0 else 1.0

    @staticmethod
    def exact_match(pred, gt):
        """完全匹配率"""
        return pred == gt

    @staticmethod
    def compute_all(pred, gt):
        """计算全部指标，返回字典"""
        dist = _edit_distance(pred, gt)
        max_len = max(len(pred), len(gt))
        acc = max(0.0, 1.0 - dist / max_len) if max_len > 0 else 1.0

        return {
            "pred": pred,
            "gt": gt,
            "edit_distance": dist,
            "char_accuracy": round(acc, 4),
            "exact_match": pred == gt,
            "pred_len": len(pred),
            "gt_len": len(gt)
        }