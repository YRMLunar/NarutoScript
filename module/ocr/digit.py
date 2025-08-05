from module.logger import logger
from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr


class SimpleDigitOcr(ONNXPaddleOcr):
    """
    简化的数字识别类，一次执行
    """

    def __init__(self, **kwargs):
        kwargs.setdefault('use_angle_cls', True)
        kwargs.setdefault('use_gpu', False)
        kwargs.setdefault('rec_image_shape', "3, 48, 320")
        super().__init__(**kwargs)

        # 数字纠正映射
        self.digit_corrections = {
            'A': '4', 'a': '4', 'O': '0', 'o': '0',
            'I': '1', 'i': '1', 'l': '1', '|': '1',
            'S': '5', 's': '5', 'G': '6', 'g': '6',
            'T': '7', 't': '7', 'B': '8', 'b': '8',
            'g': '9', 'q': '9', 'Z': '2', 'z': '2',
        }

    def extract_digit_simple(self, image, area=None) -> int:
        """
        简单的一次性数字识别
        """
        try:
            # 裁剪区域
            if area:
                x1, y1, x2, y2 = area
                image = image[y1:y2, x1:x2]

                # OCR识别
            result = self.ocr(image)

            if not result:
                return 0

                # 提取并纠正文本
            all_text = ""
            for box in result:
                all_text += box.txt + " "

                # 应用字符纠正
            corrected_text = all_text
            for wrong_char, correct_char in self.digit_corrections.items():
                corrected_text = corrected_text.replace(wrong_char, correct_char)

                # 提取数字
            import re
            numbers = re.findall(r'\d+', corrected_text)
            if numbers:
                return int(numbers[0])

            return 0

        except Exception as e:
            logger.warning(f"数字识别失败: {e}")
            return 0