from module.base.timer import Timer
from module.base.utils import color_bar_percentage, get_color, color_similarity_2d
from module.exception import GameStuckError
from module.ocr.models import OcrModel
from module.ocr.ocr import Ocr
from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr
from tasks.base.page import page_main, page_daily
from tasks.base.ui import UI
from tasks.daily.assets.assets_daily import DAILY_REWARD_10, DAILY_BAR, DAILY_PROGRESS, DAILY_REWARD_40, \
    DAILY_REWARD_80, DAILY_REWARD_100, DAILY_REWARD_10_DONE, WEEKlY_BUTTON, WEEKLY_CLAIM, WEEKLY_CLAIM_DONE
import cv2
import numpy as np

from tasks.daily.utils import daily_utils


class DailyRewardClaim(UI,daily_utils):
    def handle_daily_reward(self):
        self.ui_ensure(page_main)
        self.ui_goto(page_daily)
        if self.config.DailyReward_Daily:
            self._reward_daily_claim()
        if self.config.DailyReward_Weekly:
            self._reward_weekly_claim()
        self.ui_goto_main()
    def _reward_weekly_claim(self):
        self.device.screenshot()
        time=Timer(5,10).start()
        for _ in self.loop():
            if self.appear_then_click(WEEKlY_BUTTON,interval=3):
                continue
            if self.appear_then_click(WEEKLY_CLAIM):
                continue
            if self.appear(WEEKLY_CLAIM_DONE):
                break
            if time.reached():
                break
    def _reward_daily_claim(self):
        self.device.screenshot()
        times=0;
        timer = Timer(10,15).start()
        for _ in self.loop():
            if self.detect_ring_golden_glow(DAILY_REWARD_10):
                self.device.click(DAILY_REWARD_10)
                continue
            if self.detect_ring_golden_glow(DAILY_REWARD_40):
                self.device.click(DAILY_REWARD_40)
                continue
            if self.detect_ring_golden_glow(DAILY_REWARD_80):
                self.device.click(DAILY_REWARD_80)
                continue
            if self.detect_ring_golden_glow(DAILY_REWARD_100):
                self.device.click(DAILY_REWARD_100)
                continue
            if not self.detect_golden_box():
                times += 1
                if times >=3:
                    break
            if timer.reached():
                break
    def detect_ring_golden_glow(self, chest_area, inner_radius=35, outer_radius=70):
        """在圆环区域内检测金光效果"""
        image, ring_mask, detection_area = self.create_ring_mask(chest_area, inner_radius, outer_radius)

        # 检测金色区域
        golden_similarity = color_similarity_2d(image, color=(252, 209, 123))

        # 应用圆环遮罩
        masked_golden = cv2.bitwise_and(golden_similarity, golden_similarity, mask=ring_mask.astype(np.uint8))

        # 阈值化处理
        cv2.inRange(masked_golden, 200, 255, dst=masked_golden)

        # 统计圆环内的金光像素
        glow_pixels = cv2.countNonZero(masked_golden)
        ring_pixels = cv2.countNonZero(ring_mask.astype(np.uint8))

        # 计算金光像素占圆环面积的比例
        if ring_pixels > 0:
            glow_ratio = glow_pixels / ring_pixels
            return glow_ratio > 0.01  # 5%以上认为有金光

        return False
    def detect_golden_box(self):
       not_golden_box=self.detect_ring_golden_glow(DAILY_REWARD_10) or self.detect_ring_golden_glow(DAILY_REWARD_40) or self.detect_ring_golden_glow(DAILY_REWARD_80) or self.detect_ring_golden_glow(DAILY_REWARD_100)
       return not_golden_box

az=DailyRewardClaim('alas',task='Alas')

az.handle_daily_reward()