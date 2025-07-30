from module.base import button


class MissionTask:
    def __init__(self, name, time,area=None):
        self.name = name
        self.time = time
        self.area = area
    def __str__(self):
        """返回任务的友好字符串表示"""
        area_info = f", 区域: {self.area}" if self.area else ""
        return f"任务: {self.name}, 时间: {self.time}{area_info}"

    def __repr__(self):
        """返回任务的官方字符串表示，用于调试和列表打印"""
        return str(self)  # 复用 __str__ 的实现

mission_dic={
    "羁绊任务":2,
    "帮助一乐大叔":1,
    "打扫卫生":1,
    "雷之国护送":1,
    "面粉紧缺":1,
    "巡查":1,
    "腰痛治疗法":1,
    "辅导":1,
    "调查":1,
    "查克拉控制":1,
"木叶游记":1
}

Mission_Selected_Priority = [
    MissionTask("师徒任务", '12时0分'),
    MissionTask("白银", '6时0分'),
    MissionTask("羁绊任务", '12时0分'),
    MissionTask("帮助一乐大叔", '3时0分'),
    MissionTask("打扫卫生", '12时0分'),
    MissionTask("调查", '12时0分'),
    MissionTask("羁绊任务", '6时0分'),
    MissionTask("巡查", '6时0分'),
    MissionTask("辅导", '6时0分'),
    MissionTask("雷之国护送", '6时0分'),
    MissionTask("面粉紧缺", '3时0分'),
    MissionTask("巡查", '3时0分'),
    MissionTask("消灭山贼", '3时0分'),
    MissionTask("腰痛治疗法", '12时0分'),
    MissionTask("辅导", '3时0分'),
    MissionTask("腰痛治疗法", '6时0分'),
    MissionTask("查克拉控制", '3时0分'),
    MissionTask("查克拉控制", '12时0分'),
    MissionTask("羁绊任务", '3时0分'),
    MissionTask("木叶游记", '6时0分'),
    MissionTask("木叶游记", '12时0分'),
    MissionTask("羁绊任务", '8时0分'),

]
