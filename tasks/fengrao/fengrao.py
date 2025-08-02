from tasks.base.ui import UI


class FengRao(UI):
    def run(self):
        self.device.screenshot()
        from tasks.fengrao.fight import FengRaoFight
        FengRaoFight(self.config,self.device).handle_feng_rao()
