

from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.base.assets.assets_base_popup import EXIT_CONFIRM
from tasks.base.page import page_squad, page_squad_help_battle, page_main
from tasks.base.ui import UI
from tasks.squadraid.assets.assets_squadraid_fight import *
from tasks.squadraid.benefit import HelpBattleBenefit

class SquadRaidFight(UI):
    def handle_squad_raid(self):

        for _ in self.loop():
           if not self._squad_raid_fight():
               break
        if self.config.SquadRaid_SquadRaidBenefit:
            HelpBattleBenefit(self.config,self.device).handle_help_battle_benefit()
        self.exit_to_main()
    def _squad_raid_fight(self):
        if self._enter_squad_raid_screen():
            time=Timer(10,count=20).start()
            for _ in  self.loop():
                ocr=Digit(SQUAD_RAID_REMAIN_TIMES,lang='cn')
                res=ocr.ocr_single_line(self.device.image)
                if res==2 or res==1:
                    break
                if self.appear(SQUAD_RAID_HAVE_DONE):
                    return False
                if time.reached():
                    raise GameStuckError('SQUAD_RAID_REMAIN_TIMES DETECTED ERROR')
            self._help_battle_select()
            self._start_fight()
        else:
            return True
        return True
    def _help_battle_select(self):
        time=Timer(10,count=20).start()
        for _ in self.loop():
            if self.appear_then_click(SQUAD_GOTO_HELP_BATTLE):
                continue
            if HELP_BATTLE_SELECTED.match_template(self.device.image,direct_match=True):
                break
            wrong_buttons=HELP_BATTLE_NOT_BE_SELECTED.match_multi_template(self.device.image,direct_match=True)
            if wrong_buttons and len(wrong_buttons)==5:
                self.device.swipe( [263,594],[270,182])
                time.reset()
                continue
            HELP_BATTLE_SELECT_BUTTON.load_search((0, 0, 1280, 720))  # Full screen but bounded
            if self.appear_then_click(HELP_BATTLE_SELECT_BUTTON):
                continue
            if time.reached():
                raise GameStuckError("HELP_BATTLE_SELECT_STUCK")

    def _start_fight(self):
        time=Timer(60,8).start()
        for _ in self.loop():
            if self.appear_then_click(HELP_BATTLE_START_FIGHT):
                continue
            if self.appear(SQUAD_RAID_FIGHTING):
                continue
            if self.appear_then_click(SQUAD_RAID_FIGHT_SUCCESS):
                continue
            if self.appear(SQUAD_RAID_CHECK):
                return True
            if time.reached():
                raise GameStuckError("SQUAD_RAID_FIGHT_STUCK")

        return True

    def _enter_squad_raid_screen(self):
        if self.ui_page_appear(page_squad) or self.ui_page_appear(page_squad_help_battle):
            return True
        self.device.swipe( [1200, 314],[0, 322])
        move = True
        time = Timer(10, count=10).start()
        m=2
        for _ in self.loop():

            SQUAD_RAID_RED_DOT.load_search((0, 0, 1280, 720))  # Full screen but bounded
            if self.appear_then_click(SQUAD_RAID_RED_DOT, interval=1):
                continue
            if MAIN_GOTO_SQUAD_RAID.match_template(self.device.image,direct_match=True):
                move = False
                continue
            if self.appear(SQUAD_RAID_CHECK):
                return True
            if time.reached():
                if move and m%2==0:
                    self.device.swipe([0, 322], [1200, 314])
                    time.reset()
                    m=m+1
                elif move and m%2==1:
                    self.device.swipe( [1200, 314],[0, 322])
                    m=m+1
                    time.reset()
                elif m>5:
                    raise GameStuckError("Squad Raid enter Stucked")
        logger.info(f"Squad Raid entered")
        return True

    def exit_to_main(self):
        for _ in self.loop():
            if self.appear(EXIT_CONFIRM):
                self.device.click(EXIT_CONFIRM)
                continue
            if self.appear(SQUAD_RAID_EXIT):
                self.device.click(SQUAD_RAID_EXIT)
            if self.ui_page_appear(page_main):
                break
            self.device.click_record_clear()
