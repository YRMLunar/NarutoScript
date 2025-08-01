from module.base.base import ModuleBase
from tasks.daily.reward import DailyRewardClaim


class Daily_Reward(ModuleBase):
    def run(self):
        if self.config.DailyReward_Daily:
            DailyRewardClaim(config=self.config, device=self.device).handle_daily_reward()


        self.config.task_delay(server_update=True)
        self.config.task_stop()
