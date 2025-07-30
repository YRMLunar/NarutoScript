import re

from module.base.timer import Timer
from module.logger import logger
from module.ocr.ocr import Digit, DigitCounter
from tasks.base.page import page_item
from tasks.item.assets.assets_item_data import OCR_DATA, OCR_RELIC
from tasks.item.keywords import KEYWORDS_ITEM_TAB
from tasks.item.ui import ItemUI
from tasks.planner.model import PlannerMixin







class DataUpdate(ItemUI, PlannerMixin):
    def _get_data(self):
        """
        Page:
            in: page_item, KEYWORDS_ITEM_TAB.UpgradeMaterials
        """
        credit, jade = 0, 0
        logger.attr('Credit', credit)
        logger.attr('StellarJade', jade)
        return credit, jade

    def _get_relic(self):
        """
        Page:
            in: page_item, KEYWORDS_ITEM_TAB.Relics
        """
        relic = 0
        logger.attr('Relic', relic)
        return relic

    def run(self):
        # 跳过实际的数据获取，直接设置空值
        credit, jade, relic = 0, 0, 0

        with self.config.multi_set():
            self.config.stored.Credit.value = credit
            self.config.stored.StallerJade.value = jade
            self.config.stored.Relic.value = relic
            self.config.task_delay(server_update=True)
