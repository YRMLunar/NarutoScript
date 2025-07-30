from logging import setLogRecordFactory

from module.exception import GameStuckError
from tasks.base.page import page_main, page_friend_panel
from tasks.base.ui import UI
from tasks.freebies.assets.assets_freebies_friendgifts import MAIN_GOTO_FRIEND_PANEL, GIFTS_GIVE, GIFTS_CLAIM, \
    GIFTS_CLAIM_CHECK, GIFTS_CLAIM_CONFIRM, FRIEND_PANEL_RED_DOT, GIVE_DONE
from module.base.timer import Timer
from module.logger.logger import logger

class FriendGifts(UI):
    def handle_friend_gifts(self):
        self.ui_ensure(page_main)
        if  True:    #self.appear(FRIEND_PANEL_RED_DOT):
            self.ui_goto(page_friend_panel)
            self._friend_gifts_give()
            self._friend_gifts_claim()
        self.ui_goto_main()

    def _friend_gifts_give(self):
       time=Timer(4,count=8).start()
       for _ in self.loop():
        if self.appear(GIFTS_GIVE,interval=1):
            self.device.click(GIFTS_GIVE)
            continue
        if self.appear(GIVE_DONE):
            break
        if time.reached():
            raise GameStuckError("friend gifts give failed")

    def _friend_gifts_claim(self):
        time=Timer(4,count=8).start()
        for _ in self.loop():
            if self.appear(GIFTS_CLAIM,interval=1):
                self.device.click(GIFTS_CLAIM)
                continue
            if self.appear(GIFTS_CLAIM_CONFIRM,interval=1):
                self.device.click(GIFTS_CLAIM_CONFIRM)
                continue
            if self.appear(GIFTS_CLAIM_CHECK):
                break
            if time.reached():
                raise GameStuckError("friend gifts claim failed")

az=FriendGifts('alas',task='Alas')
az.handle_friend_gifts()