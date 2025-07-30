from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr

#todo 任务集会所专用OCR  对task识别结果处理， 通过dic 对ocr结果进行修正
# class MissionOcr(ONNXPaddleOcr):

import cv2
import numpy as np
import re
from typing import List, Dict, Tuple, Optional
from tasks.mission.priority import mission_dic
class MissionOcr(ONNXPaddleOcr):
    def __init__(self, **kwargs):
        """
        初始化 MissionOcr 类，继承自 ONNXPaddleOcr 并添加预处理和后处理功能

        Args:
            preprocess_config: 预处理配置参数
            postprocess_config: 后处理配置参数
            **kwargs: 其他传递给父类的参数
        """
        super().__init__(**kwargs)




    def postprocess(self, boxes: List) -> List:
        """
        OCR 结果后处理，包括任务名称修正、时间格式标准化等

        Args:
            boxes: OCR 识别结果列表 (TxtBoxList)

        Returns:
            后处理后的结果列表
        """
        if not boxes:
            return []

        # 1. 修正任务名称（基于字典的模糊匹配）
        corrected_boxes = []
        for box in boxes:
            original_text = box.txt
            corrected_text = self.correct_task_name(original_text)

            # 更新文本
            if corrected_text != original_text:
                box.txt = corrected_text
                # 标记为已修正

            corrected_boxes.append(box)



        # 3. 其他后处理操作...

        return corrected_boxes

    def correct_task_name(self, text: str) -> str:
        """
        根据任务字典修正 OCR 识别的任务名称

        Args:
            text: OCR 识别的原始文本

        Returns:
            修正后的任务名称，如果没有匹配则返回原文
        """
        # 简单预处理
        text = text.strip().replace(" ", "")

        # 如果直接匹配，返回原结果
        if text in mission_dic:
            return text

        # 使用相似度匹配（简化版，实际可使用 Levenshtein 等算法）
        best_match = None
        highest_similarity = 0

        for task_name in mission_dic:
            similarity = self.calculate_similarity(text, task_name)
            if similarity > highest_similarity and similarity >= 0.6:  # 设置阈值
                highest_similarity = similarity
                best_match = task_name

        return best_match or text

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        计算两个字符串的相似度（简化版，实际可替换为更复杂的算法）

        Args:
            text1, text2: 待比较的字符串

        Returns:
            相似度得分 (0.0-1.0)
        """
        # 这里使用简单的字符匹配率，实际可使用 Levenshtein 距离等
        common_chars = set(text1) & set(text2)
        return len(common_chars) / max(len(set(text1)), len(set(text2)))

    def standardize_time_format(self, boxes: List) -> List:
        """
        标准化时间格式（例如："9时30分" → "09:30"）

        Args:
            boxes: OCR 识别结果列表

        Returns:
            时间格式标准化后的结果列表
        """
        pattern = r'(0?[0-9]|1[0-9]|2[0-3])时([0-5]?[0-9])分'

        for box in boxes:
            match = re.search(pattern, box.txt)
            if match:
                hour = match.group(1).zfill(2)  # 补零到两位
                minute = match.group(2).zfill(2)
                standardized_time = f"{hour}:{minute}"

                # 替换原文本中的时间部分
                box.txt = re.sub(pattern, standardized_time, box.txt)

        return boxes

    def ocr(self, img, det=True, rec=True, cls=True):
        """
        重写 OCR 方法，添加预处理和后处理步骤

        Args:
            img: 输入图像
            det: 是否进行文本检测
            rec: 是否进行文本识别
            cls: 是否进行文本方向分类

        Returns:
            后处理后的 OCR 结果
        """
        # 1. 预处理图像
        processed_img = self.preprocess(img)

        # 2. 调用父类的 OCR 方法
        boxes = super().ocr(processed_img, det, rec, cls)

        # 3. 后处理结果
        postprocessed_boxes = self.postprocess(boxes)

        return postprocessed_boxes