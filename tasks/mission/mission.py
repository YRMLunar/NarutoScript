from dev_tools.button_extract import parse_grid
from module.base.timer import Timer
from module.logger.logger import logger

from module.base.utils import crop
import cv2

from module.ocr.ocr import TextBox
from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr, sav2Img, TxtBox
from module.ocr.utils import pair_buttons
from tasks.base.page import page_main, page_mission
from tasks.base.ui import UI
from tasks.mission.assets.assets_mission import MISSION_CHECK, MISSION_RED_DOT, WORK_FINISHED, WORK, \
    MISSION_REWARD_CLAIM_ALL, MISSION_REWARD, REWARD_CLAIM_DONE, TASK_AREA, CHARACTER_UNSELECTED, \
    CHARACTER_SELECTED_AUTO, CHARACTER_SELECTED, TASK_ACCEPT, ACCPET_BUTTON, CHARACTER_SELECTED_MANUAL, \
    MISSION_SELECTED_SUCCESS

from tasks.mission.priority import Mission_Selected_Priority, MissionTask

from tasks.mission.utils import getTaskName, result_time_fromat, generate_4x4_grid


class Mission(UI):
    def handle_mission(self):
        self.ui_ensure(page_main)
        if not self._mission_enter():
            return False
        self._mission_reward_claim()
        #self._mission_selected()
        self.config.task_delay(server_update=True)


    def _mission_enter(self):
        self.device.swipe_maatouch([180,322],[1141,314])
        logger.info("left swipe")
        timer = Timer(3,count=2).start()
        for _ in self.loop():
            if self.appear(MISSION_CHECK):
                self.wait_until_stable(MISSION_CHECK)
                logger.info('mission entered')
                timer.clear()
                return True
            if self.appear(MISSION_RED_DOT):
                logger.info("Found Mission")
                self.device.click(MISSION_RED_DOT)
                continue
            if timer.reached():
                timer.clear()
                return False
        # self.device.swipe_maatouch([1141,314],[180,322])
        # timer = Timer(1.5,count=2)
        # for _ in self.loop():
        #     if self.appear(MISSION_RED_DOT):
        #         self.wait_until_stable(MISSION_RED_DOT)
        #         self.device.click(MISSION_RED_DOT)
        #         timer.clear()
        #         return
        #     if timer.reached():
        #         timer.clear()
        #         break

    def _mission_reward_claim(self):
        self.ui_ensure(page_mission)
        model = ONNXPaddleOcr(use_angle_cls=True, use_gpu=False)
        self.device.screenshot()
        result=model.ocr(self.device.image)
        matched_res=model.matchKeys(result,['可领取'])
        if len(matched_res)<=0 and self.appear(REWARD_CLAIM_DONE):
            return True
        x_sorted_res=sorted(matched_res, key=lambda b:b.button[0])
        print(x_sorted_res)
        self.device.click(x_sorted_res[0])
        for _ in self.loop():
            if self.appear_then_click(MISSION_REWARD_CLAIM_ALL):
                continue
            if self.appear_then_click(MISSION_REWARD):
                return True
            if self.appear(REWARD_CLAIM_DONE):
                return True
            res=model.ocr(self.device.image)
            if model.matchArea(res,x_sorted_res[0].button):
                self.device.click(x_sorted_res[0])
    def _mission_selected(self):
        self.ui_ensure(page_mission)
        if self.appear(MISSION_SELECTED_SUCCESS):
            return True
        for _ in self.loop():
            if self.appear(MISSION_CHECK,interval=4):
                task=self._mission_select_priority()
                logger.info('task selected: {}'.format(task))
                self.device.click(task)
            if self.appear(TASK_ACCEPT):
                break
        for _ in self.loop():
            if self.appear(CHARACTER_SELECTED_AUTO):
                self.device.click(CHARACTER_SELECTED_AUTO)
                self.device.click(TASK_ACCEPT)
            if self.appear(CHARACTER_SELECTED_MANUAL):
                res=generate_4x4_grid()
                self.device.click(res[0])
            if self.appear(ACCPET_BUTTON):
                break
#todo 只做了领取一次任务，未循环
    # def scan_character_grids(self):
    #     self.device.screenshot()
    #     mc=MissionCharacter(name='rizhan',screenshot=self.device.image)
    #     res=mc._find_character()
    #     print(res)

    def _mission_select_priority(self):
        self.device.screenshot()
        #全屏ocr
        ocr = ONNXPaddleOcr(use_angle_cls=True, use_gpu=False)
        result=ocr.ocr(self.device.image)
        #时间格式化
        task_time_unformat=ocr.matchTime(result)
        task_time=result_time_fromat(task_time_unformat)
        print(task_time)
        #任务优先级列表
        priority=Mission_Selected_Priority
        #任务名称
        task_name=ocr.matchArea(result, TASK_AREA.search)
        print(task_name)
        #任务按钮
        task_buttons=ocr.matchKeys(result,'接取')
        print(task_buttons)
        currentTask=[]
        for name,time in pair_buttons(task_name,task_time, (-100, -50, 800, 50)):
            name.time=time.txt
            currentTask.append(name)
        task_with_button=[]
        for task,button in pair_buttons(currentTask,task_buttons,(-100, -50, 800, 110)):
            task.button=button.button
            task_with_button.append(task)
        logger.info(task_with_button)
        for prestTask in priority:
            for task in task_with_button:
                if task.txt==prestTask.name and task.time==prestTask.time:
                    task_matched=task
                    return task_matched
        logger.info("优先级匹配识别，默认第一个任务")
        if len(task_with_button)>=1:
            return task_with_button[0]


az=Mission('alas',task='Alas')
# a=TxtBox(button=(537,212.577,311),txt='1',threadhold=0.5)

az._mission_reward_claim()

# #
# # print(az.appear(MISSION_CHECK))

# az._mission_reward_claim()
# import os
# os.chdir(os.path.dirname(os.path.abspath(__file__)))
#
# img = cv2.imread('./1.jpg')
# rs=model.ocr(img)
# print(rs)

