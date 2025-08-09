from module.base.timer import Timer
from module.exception import GameStuckError
from module.ocr.ocr import Digit
from tasks.base.assets.assets_base import TILI_REMAIN
from tasks.base.page import page_main
from tasks.base.ui import UI
from tasks.tili.assets.assets_tili_dungeon import *

class Dungeon(UI):
    def handle_dungeon(self):
        self.device.screenshot()
        ocr=Digit(TILI_REMAIN,lang='cn')
        tili=ocr.ocr_single_line(self.device.image)
        self.config.TiLi_TiLiRemain=tili
        if tili<10:
            return
        self._dungeon_enter()
        self._dungeon_exit()
    def _dungeon_enter(self):
        self.device.click_record_clear()
        time=Timer(20,count=30).start()
        for _ in self.loop():
            if SWEEP_RUNNING.match_template(self.device.image,direct_match=True):
                break
            if self.appear(SWEEP_DONE):
                break
            if self.appear_then_click(SWEEP_CONFIRM_BUTTON):
                continue
            if self.appear_then_click(SWEEP_BUTTON):
                continue
            if self.appear_then_click(CONVENIENT_SWEEP):
                continue
            if self.appear(SWITCH_TO_DUNGEON):
                self.device.click(SWITCH_TO_DUNGEON)
                continue
            if self.appear(MAIN_GOTO_DUNGEON):
                self.device.click(MAIN_GOTO_DUNGEON)
                continue
            if  time.reached():
                raise GameStuckError('Dungeon Sweep Stucked')

    def _dungeon_exit(self):
        time=Timer(10,count=20).start()
        self.device.click_record_clear()
        for _ in self.loop():
            if self.ui_page_appear(page_main):
                break
            if self.appear(SWEEP_END_CONFIRM):
                self.device.click(DUNGEON_EXIT)
                continue
            if SWEEP_RUNNING.match_template(self.device.image,direct_match=True):
                self.device.click(DUNGEON_EXIT)
                self.device.click_record_remove(DUNGEON_EXIT)
                continue
            if self.appear(SWEEP_BUTTON):
                self.device.click(DUNGEON_EXIT)
                continue
            if self.appear(DUNGEON_EXIT):
                self.device.click(DUNGEON_EXIT)
                continue
            if  time.reached():
                raise GameStuckError('Dungeon Exit Stucked')
az=Dungeon('alas',task='Alas')
az.handle_dungeon()


