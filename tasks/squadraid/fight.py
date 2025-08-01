

from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger
from tasks.base.page import page_squad, page_squad_help_battle
from tasks.base.ui import UI
from tasks.squadraid.assets.assets_squadraid import SQUAD_RAID_RED_DOT, MAIN_GOTO_SQUAD_RAID, SQUAD_RAID_CHECK, \
    HELP_BATTLE_SLECT_BUTTON, HELP_BATTLE_SELECTED, HELP_BATTLE_START_FIGHT, \
    SQUAD_RAID_FIGHTING, SQUAD_RAID_FIGHT_SUCCESS, SQUAD_RAID_HAVE_DONE, SQUAD_GOTO_HELP_BATTLE
from tasks.squadraid.benefit import HelpBattleBenefit

class SquadRaidFight(UI):
    def handle_squad_raid(self):
        self._squad_raid_fight()
        self._squad_raid_fight()
        if self.config.SquadRaid_SquadRaidBenefit:
            HelpBattleBenefit(self.config,self.device).handle_help_battle_benefit()
        self.ui_goto_main()


    def _squad_raid_fight(self):
        if self._enter_squad_raid_screen():
            time=Timer(1,count=2)
            for _ in  self.loop():
                if self.appear(SQUAD_RAID_HAVE_DONE):
                    return
                if time.reached():
                    return
            self._help_battle_select()
            self._start_fight()
    def _help_battle_select(self):
        self.device.screenshot()
        time=Timer(5,8).start()
        select_times=0
        for _ in self.loop():
            if self.appear_then_click(SQUAD_GOTO_HELP_BATTLE):
                continue
            HELP_BATTLE_SLECT_BUTTON.load_search([333, 137, 473, 654])
            if self.appear_then_click(HELP_BATTLE_SLECT_BUTTON):
                select_times += 1
                continue
            HELP_BATTLE_SELECTED.load_search([333, 137, 473, 654])
            if self.appear(HELP_BATTLE_SELECTED):
                break
            if time.reached():
                if select_times<=0:
                    self.device.swipe( [263,594],[270,182])
                    time.reset()
                else:
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
        self.device.screenshot()
        if self.ui_page_appear(page_squad) or self.ui_page_appear(page_squad_help_battle):
            return True
        self.device.screenshot()
        self.device.swipe( [1200, 314],[0, 322])
        move = True
        time = Timer(10, count=10).start()
        m=2
        for _ in self.loop():
            SQUAD_RAID_RED_DOT.load_search((200, 100, 1100, 400))
            if self.appear_then_click(SQUAD_RAID_RED_DOT):
                continue
            MAIN_GOTO_SQUAD_RAID.load_search((200, 100, 1100, 400))
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