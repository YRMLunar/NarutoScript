import cv2

from module.base.utils import area2corner, corner2area
from .onnxocr.onnx_paddleocr import ONNXPaddleOcr
from collections import defaultdict


class TextBox:
    def __init__(self, text, box):
        self.text = text
        self.box = box
        self.button=corner2area(box)# [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]

    def center_y(self):
        return sum([point[1] for point in self.box]) / 4

    def center_x(self):
        return sum([point[0] for point in self.box]) / 4

    def __repr__(self):
        return f"TextBox(text='{self.text}', box={self.box})"


class CommonOCR:
    def __init__(self, ocr_model, conf_threshold=0.5):
        self.ocr_model = ocr_model
        self.conf_threshold = conf_threshold


    def run(self, img):
        raw_result = self.ocr_model.ocr(img)
        textboxes = []

        for box, (text, score) in raw_result[0]:
            if score >= self.conf_threshold:
                textboxes.append(TextBox(text, box))

        return textboxes

    def filter_by_keywords(self, textboxes, keywords):
        keywords = [kw.lower() for kw in keywords]
        return [tb for tb in textboxes if any(kw in tb.text.lower() for kw in keywords)]

    def group_by_rows(self, textboxes, y_threshold=10):
        rows = defaultdict(list)
        for tb in textboxes:
            y_center = tb.center_y()
            matched_row = None
            for row_y in rows:
                if abs(row_y - y_center) <= y_threshold:
                    matched_row = row_y
                    break
            if matched_row is None:
                matched_row = y_center
            rows[matched_row].append(tb)

        # 每一行按 x 坐标从左往右排序
        sorted_rows = []
        for row_y in sorted(rows):
            row = sorted(rows[row_y], key=lambda tb: tb.center_x())
            sorted_rows.append(row)
        return sorted_rows


# ✅ 示例使用
if __name__ == "__main__":
    image_path = r"./test.png"
    img = cv2.imread(image_path)

    # 正确传入 OCR 模型
    ocr_model = ONNXPaddleOcr(use_angle_cls=True, use_gpu=False)
    common_ocr = CommonOCR(ocr_model=ocr_model, conf_threshold=0.6)

    # 获取识别结果
    textboxes = common_ocr.run(img)

    print("✅ 识别文字:")
    for tb in textboxes:
        print(f"- {tb.text}  坐标: {tb.box}  边界值:{tb.button}"  )

    print("\n✅ 按行排序:")
    sorted_rows = common_ocr.group_by_rows(textboxes)
    for row in sorted_rows:
        print(" | ".join(tb.text for tb in row))

    print("\n✅ 关键词匹配:")
    matched = common_ocr.filter_by_keywords(textboxes, ["账号", "登录", "验证码"])
    for tb in matched:
        print(f"匹配项: {tb.text}  坐标: {tb.box}")