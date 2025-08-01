from module.base.timer import Timer

from tasks.base.page import page_squad_help_battle_mine
from tasks.base.ui import UI
from tasks.squadraid.assets.assets_squadraid import HELP_BATTLE_MINE_BENEFIT_CLAIM, HELP_BATTLE_MINE_BENEFIT_CLAIM_DONE



class HelpBattleBenefit(UI):
    def handle_help_battle_benefit(self):
        self.ui_goto(page_squad_help_battle_mine)
        time=Timer(5,count=10).start()
        for _ in self.loop():
            if self.appear_then_click(HELP_BATTLE_MINE_BENEFIT_CLAIM):
                continue
            if self.appear(HELP_BATTLE_MINE_BENEFIT_CLAIM_DONE):
                break
            if time.reached():
                break
        return True
