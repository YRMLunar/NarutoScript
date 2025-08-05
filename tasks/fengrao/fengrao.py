from tasks.base.ui import UI
from tasks.fengrao.fight import FengRaoFight

class FengRao(UI):
    def run(self):
        FengRaoFight(self.config,self.device).handle_feng_rao()
