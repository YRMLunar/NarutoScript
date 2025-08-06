from datetime import timedelta

from module.config.utils import get_server_next_monday_update
from tasks.base.ui import UI
from tasks.trail.cultivation_mopup import CultivationMopUp

#周本要在config.py下添加任务名称来覆盖配置，否则会导致任务循环运行无法停止
class CultivationRoad(UI):
    def run(self):
        flag=CultivationMopUp(self.config,self.device).handle_cultivation_mop_up()
        if flag=='MOP_UP_RUNNING':
            self.config.task_delay(minute=120)
        elif flag=='MOP_UP_SUCCESS':
            monday = get_server_next_monday_update(self.config.Scheduler_ServerUpdate)
            self.config.task_delay(target=monday)
            # Explicitly disable to prevent hoarding interference
            self.config.modified[f'{self.config.task.command}.Scheduler.Enable'] = False
        else:
            self.config.task_delay(minute=120)
        self.config.task_stop()
