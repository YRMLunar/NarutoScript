from typing import Callable

from module.base.base import ModuleBase
from module.base.utils import color_similarity_2d
from module.logger import logger
# from tasks.base.assets.assets_base_page import BACK, CLOSE
from tasks.base.assets.assets_base_popup import *


class PopupHandler(ModuleBase):
    pass



    # def handle_ui_close(self, appear_button: ButtonWrapper | Callable, interval=2) -> bool:
    #     """
    #     Args:
    #         appear_button: Click if button appears
    #         interval:
    #
    #     Returns:
    #         If handled.
    #     """
    #     if callable(appear_button):
    #         if self.interval_is_reached(appear_button, interval=interval) and appear_button():
    #             logger.info(f'{appear_button.__name__} -> {CLOSE}')
    #             self.device.click(CLOSE)
    #             self.interval_reset(appear_button, interval=interval)
    #             return True
    #     else:
    #         if self.appear(appear_button, interval=interval):
    #             logger.info(f'{appear_button} -> {CLOSE}')
    #             self.device.click(CLOSE)
    #             return True
    #
    #     return False
    #
    # def handle_ui_back(self, appear_button: ButtonWrapper | Callable, interval=2) -> bool:
    #     """
    #     Args:
    #         appear_button: Click if button appears
    #         interval:
    #
    #     Returns:
    #         If handled.
    #     """
    #     if callable(appear_button):
    #         if self.interval_is_reached(appear_button, interval=interval) and appear_button():
    #             logger.info(f'{appear_button.__name__} -> {BACK}')
    #             self.device.click(BACK)
    #             self.interval_reset(appear_button, interval=interval)
    #             return True
    #     else:
    #         if self.appear(appear_button, interval=interval):
    #             logger.info(f'{appear_button} -> {BACK}')
    #             self.device.click(BACK)
    #             return True
    #
    #     return False
