from module.base import button
from module.base.timer import Timer
from module.base.utils import color_similarity_2d
from module.exception import GameStuckError
from tasks.base.page import page_main
from tasks.base.ui import UI
from tasks.organization.assets.assets_organization_pray import *
from tasks.organization.assets.assets_organization_boxclaim import *
from tasks.organization.assets.assets_organization_replacement import *
from module.logger import  logger

class Pray(UI):
    def handle_Organization_Pray(self):
        self.ui_ensure(page_main)
        self._organization_panel_enter()
        self._enter_pray_panel()
        self.pray()
        self._pray_box_replacement()
        self.pray_box_claim()
        self.ui_goto_main()
    def _organization_panel_enter(self):
        self.device.swipe([0, 322], [1280, 314])
        move = True
        time = Timer(10, count=10).start()
        m=2
        for _ in self.loop():
            ORGANIZATION_RED_DOT.load_search((200, 100, 1100, 400))
            if self.appear_then_click(ORGANIZATION_RED_DOT):
                continue
            MAIN_GOTO_ORGANIZATION.load_search((200, 100, 1100, 400))
            if MAIN_GOTO_ORGANIZATION.match_template(self.device.image,direct_match=True):
                move = False
                continue
            if self.appear(ORGANIZATION_PANEL):
                return True
            if time.reached():
                if move and m%2==0:
                    self.device.swipe( [1200, 314],[0, 322])
                    time.reset()
                    m=m+1
                elif move and m%2==1:
                    self.device.swipe([0, 322], [1200, 314])
                    m=m+1
                    time.reset()
                elif m>5:
                    raise GameStuckError("Organization Pray Stucked")
        logger.info(f"Organization Panel entered")

    def _enter_pray_panel(self):
        time=Timer(8, count=10).start()
        for _ in self.loop():
            if self.appear_then_click(ORGANIZATION_PLAY_PANEL):
                continue
            if self.appear_then_click(ORGANIZATION_GOTO_PRAY):
                continue
            if self.appear(ORGANIZATION_PRAY_CHECK):
                break
            if time.reached():
                raise GameStuckError("Organization Pray Stucked")

    def pray(self):
        time=Timer(6, count=10).start()
        for _ in self.loop():
            if self.appear_then_click(PRAY_BUTTON,interval=1):
                continue
            if self.appear(PRAY_SUCCESS,interval=1):
                self.device.click(PRAY_SUCCESS)
                break
            if self.appear(PRAY_HAVE_DONE,interval=1):
                self.device.click(PRAY_HAVE_DONE)
                break
            if time.reached():
                raise GameStuckError("Organization Pray Stucked")

    def pray_box_claim(self):
        time=Timer(5, count=10).start()
        self.device.screenshot()
        print(self.match_template_luma(button=PRAY_BOX_CLAIM_15,similarity=0.99))

    def _pray_box_replacement(self):
        self.device.screenshot()
        for _ in self.loop():
            if self.appear(PRAY_BOX_REPLACEMENT,interval=1):
                self.device.click(PRAY_BOX_REPLACEMENT)
            if self.appear(PRAY_BOX_REPLACEMENT_CHECK):
                break
        for _ in self.loop():
            PRAY_BOX_REPLACEMENT_HAVE_CLAIMED.load_search(PRAY_BOX_REPLACEMENT_LIST.area)
            success = PRAY_BOX_REPLACEMENT_HAVE_CLAIMED.match_multi_template(self.device.image)
            if success and len(success) == 3:
                break

            PRAY_BOX_REPLACEMENT_BUTTON.load_search(PRAY_BOX_REPLACEMENT_LIST.area)
            buttons = PRAY_BOX_REPLACEMENT_BUTTON.match_multi_template(self.device.image)
            if buttons:
                for button in buttons:
                    self.device.click(button)
        for _ in self.loop():
            if self.appear(PRAY_BUTTON,interval=1):
                break
            if self.appear(PRAY_BOX_REPLACEMENT_HAVE_CLAIMED):
                self.device.click(PRAY_BOX_REPLACEMENT_HAVE_CLAIMED)
