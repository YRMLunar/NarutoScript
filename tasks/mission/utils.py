from module.base.utils import corner2area, area_center
from tasks.mission.assets.assets_mission import MISSION_CHARACTER_GRID
from tasks.mission.priority import Mission_Selected_Priority
import re

import cv2
import numpy as np
def getTaskName(result):
    taskName=[]
    for task_priority in Mission_Selected_Priority:
        for res in result:
            if res.txt==task_priority.name:
                taskName.append(res)
    return taskName
def result_time_fromat(result):
    pattern = r'(0?[0-9]|1[0-9]|2[0-3])时([0-5]?[0-9])分'
    for res in result:
        match=re.search(pattern,res.txt)  # 匹配"时间"后接冒号或空格，然后移除
        if match:
            res.txt=match.group(0)

        else:
            return None
    return result


def generate_4x4_grid(grid_area=MISSION_CHARACTER_GRID.area, spacing=20):
    """
    生成4*4网格位置

    Args:
        grid_area: 整个网格区域 (x1, y1, x2, y2)
        spacing: 正方形之间的间距
    """

    x1, y1, x2, y2 = grid_area
    total_width = x2 - x1
    total_height = y2 - y1

    # 计算每个正方形的大小（考虑间距）
    square_width = (total_width - 3 * spacing) // 4
    square_height = (total_height - 3 * spacing) // 4

    grid_positions = {}
    for row in range(4):
        for col in range(4):
            start_x = x1 + col * (square_width + spacing)
            start_y = y1 + row * (square_height + spacing)
            end_x = start_x + square_width
            end_y = start_y + square_height
            grid_positions[(col, row)] = (start_x, start_y, end_x, end_y)

    return grid_positions

res=generate_4x4_grid()
print(res)