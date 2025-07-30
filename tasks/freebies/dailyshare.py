from  module.base.timer import Timer
from module.exception import GameStuckError

from tasks.base.page import page_main, page_panel
from tasks.base.ui import UI
from tasks.freebies.assets.assets_freebies_dailyshare import MAIN_GOTO_PANEL, SHARE_BUTTON, SHARE_GOTO_QQ


class DailyShare(UI):
    def handle_daily_share(self):
        self.ui_ensure(page_main)
        self.ui_goto(page_panel)
        time=Timer(20,count=20).start()
        for _ in self.loop():
            if self.appear(SHARE_BUTTON):
                self.device.click(SHARE_BUTTON)
                continue
            if self.appear(SHARE_GOTO_QQ):
                self.device.click(SHARE_GOTO_QQ)
                continue
            if time.reached():
                raise GameStuckError("DailyShare Game stuck")
            if  self.device.app_is_running():
                continue
            else:
                self.device.app_stop_adb('com.tencent.mobileqq')
                break






az=DailyShare('alas',task='Alas')
# az.image_file=r'C:\Users\liuzy\Desktop\NarutoScript\tasks\freebies\MuMu12-20250728-165453.png'
# print(az.appear(SHARE_GOTO_QQ))
az.handle_daily_share()