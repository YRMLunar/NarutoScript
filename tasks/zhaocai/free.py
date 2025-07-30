from module.exception import GameStuckError
from tasks.base.page import page_main, page_zhaocai
from tasks.base.ui import UI
from tasks.zhaocai.assets.assets_zhaocai import ZHAO_CAI_RED_DOT, ZHAO_CAI_FREE, ZHAO_CAI_PAIED
from module.logger.logger import logger
from module.base.timer import Timer

class ZhaoCaiFree(UI):
    def handle_zhao_Cai(self):
        self.ui_ensure(page_main)
        if self.appear(ZHAO_CAI_RED_DOT):
            self.ui_goto(page_zhaocai)
            self.freezhaocai()
        self.ui_ensure(page_main)


    def freezhaocai(self):
        time=Timer(20,count=20).start()
        for _ in self.loop():
            if self.appear_then_click(ZHAO_CAI_FREE,interval=2):
                continue
            if self.appear(ZHAO_CAI_PAIED):
                self.ui_goto_main()
                break
            if time.reached():
                logger.warning("ZhaoCai timeout")
                raise GameStuckError("ZhaoCai timeout after 20 seconds")

