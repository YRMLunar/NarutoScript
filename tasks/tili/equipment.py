from module.base.button import match_template
from module.base.utils import crop
from module.logger import logger
from module.ocr.ocr import Digit, DigitCounter
from tasks.base.page import *
from tasks.base.ui import UI
from tasks.tili.assets.assets_tili_equipment import *

class Equipment(UI):
    def handle_equipment(self):
        self.device.screenshot()
        for _ in self.loop():
            self._equipment_enter()
            res=self._equipment_advance()
            if res=='TI_LI_SHORTAGE':
                break
        self._equipment_exit()
            
       


    def _equipment_enter(self):
        for _ in self.loop():
            if self.appear(EQUIPMENT_CHECK):
                if self.appear(EQUIPMENT_KNIFE):
                    self.device.click(EQUIPMENT_KNIFE)
                break
            if self.ui_page_appear(page_stuff):
                self.device.click(EQUIPMENT_EXIT)
                continue
            if self.ui_page_appear(page_sweep):
                self.device.click(EQUIPMENT_EXIT)
                continue
            if self.appear_then_click(MAIN_GOTO_EQUIPMENT):
                continue
            if self.appear_then_click(MAIN_GOTO_EQUIPMENT_LIST):
                continue

        for _ in self.loop():
            part = self.part_select()
            if not part:
                continue

                # 获取目标装备的位置信息
            target_value, target_position = part

            # 如果目标是第一个位置，直接认为已选中（因为已经初始化点击了KNIFE）
            if target_position == 0:
                logger.info("Target is first equipment (KNIFE), already selected")
                break

                # 对于其他位置，使用变化检测
            if not hasattr(self, '_initial_detail'):
                self._initial_detail = self.image_crop(EQUIPMENT_PART_DETAIL.area, copy=True)

            current_detail = self.image_crop(EQUIPMENT_PART_DETAIL.area, copy=False)
            if not match_template(current_detail, self._initial_detail, similarity=0.95):
                break

            if self.appear(part[0], interval=0.5):
                self.device.click(part[0])
                continue

    def part_select(self):
        self.device.screenshot()
        part_areas = [EQUIPMENT_KNIFE, EQUIPMENT_RING,EQUIPMENT_CAP, EQUIPMENT_SHIRT, EQUIPMENT_BOOK, EQUIPMENT_NECKLACE]
        image_list = [crop(self.device.image, area.area) for area in part_areas]
        ocr = Digit(part_areas[0])  # 使用第一个区域初始化
        results = ocr.ocr_multi_lines(image_list)
        part_values = []
        for i, (value, score) in enumerate(results):
            # value 已经是 int 类型，不需要再转换
            part_values.append(value)
            logger.info(f"Part {i+1}: {value}")
        for i, value in enumerate(part_values):
            if value < 72:  # 这里比较的是value（数值）
                # return part_areas[i],value
                return EQUIPMENT_KNIFE,0
        return None, None

    def _equipment_advance(self):
        for _ in self.loop():
            if self.appear(STUFF_EQUIPMENT_DIRECT):
                break
            if self.appear(STUFF_SWEEP_BUTTON):
                break
            if self.appear(STUFF_SYNTHETIC_BUTTON):
                break
            stuff=self.find_first_unclaimed_item()
            if not stuff:
                continue
            self.device.click(stuff)

        for _ in self.loop():
            if self.appear(EQUIPMENT_CHECK):
                break
            if self.appear_then_click(STUFF_SYNTHETIC_BUTTON):
                continue
            if self.appear_then_click(STUFF_EQUIPMENT):
                continue
            if self.appear_then_click(STUFF_EQUIPMENT_DIRECT):
                continue
            ocr=DigitCounter(STUFF_PART_1)
            current, remain, total = ocr.ocr_single_line(self.device.image)
            if remain>0:
                self.device.click(STUFF_PART_1)
                res=self.sweep()
                if res=='TI_LI_SHORTAGE':
                    return 'TI_LI_SHORTAGE'
                elif res=='STUFF_FULL':
                    continue
            elif remain<=0:
                break
        for _ in self.loop():
            if self.appear(EQUIPMENT_CHECK):
                break
            if self.appear_then_click(STUFF_SYNTHETIC_BUTTON):
                continue
            if self.appear_then_click(STUFF_EQUIPMENT):
                continue
            if self.appear_then_click(STUFF_EQUIPMENT_DIRECT):
                continue
            ocr=DigitCounter(STUFF_PART_2)
            current, remain, total = ocr.ocr_single_line(self.device.image)
            if remain>0:
                self.device.click(STUFF_PART_2)
                res=self.sweep()
                if res=='TI_LI_SHORTAGE':
                    return 'TI_LI_SHORTAGE'
                elif res=='STUFF_FULL':
                    continue
            elif remain<=0:
                break


        #todo 材料一材料二数量满足，识别合成并点击
        #todo 扫描是否可以进阶
        #todo 循环材料扫荡，直到体力不足返回false退出循环
        #todo  退出前判断是否可以进阶/升级
        #todo 开始前判断是否可以进阶/升级



    def find_first_unclaimed_item(self):

        """
        从左到右找到第一个未获得的物品

        Returns:
            int: 第一个未获得物品的位置索引（0-5），如果都已获得则返回-1
        """
        # 定义六个物品的区域（从左到右）
        item_areas = [STUFF_1, STUFF_2, STUFF_3, STUFF_4, STUFF_5, STUFF_6]
        for i, area in enumerate(item_areas):
            # 检测该区域是否有鲜艳颜色（已获得状态）
            # 根据实际情况调整颜色值和阈值
            bright_color_count = self.image_color_count(
                area,
                color=(255, 255, 255),  # 鲜艳颜色，需要根据实际调整
                threshold=200,          # 颜色相似度阈值
                count=50               # 最小像素数量
            )

            if not bright_color_count:
                # 没有检测到鲜艳颜色，说明是暗色（未获得）
                logger.info(f"Found first unclaimed item at position {i}")
                return item_areas[i]

        logger.info("All items have been claimed")
        return None

    def sweep(self):
        for _ in self.loop():
            if self.appear(SWEEP_DETAIL):
                break
            if self.appear_then_click(STUFF_SWEEP_BUTTON):
                continue
        for _ in self.loop():
            ocr=DigitCounter(TI_LI_REMAIN)
            current,remain,total= ocr.ocr_single_line(self.device.image)
            if current<5 :
                for _ in self.loop():
                    if self.appear(STUFF_CHECK):
                        break
                    if self.appear(SWEEP_CHECK):
                        self.device.click(EQUIPMENT_EXIT)
                return 'TI_LI_SHORTAGE'
            if STUFF_FULL.match_template(self.device.image,direct_match=True):
                for _ in self.loop():
                    if self.appear(STUFF_CHECK):
                        break
                    if self.appear(SWEEP_CHECK):
                        self.device.click(EQUIPMENT_EXIT)
                return 'STUFF_FULL'
            if SWEEP_RUNNING.match_template(self.device.image,direct_match=True):
                continue
            if self.appear(SWEEP_START):
                self.device.click(SWEEP_START)
                continue
            if self.appear(STUFF_SWEEP_BUTTON):
                self.device.click(STUFF_SWEEP_BUTTON)
                continue
        return 'TI_LI_SHORTAGE'

    def _equipment_exit(self):
        for _ in  self.loop():
            if self.ui_page_appear(page_main):
                break
            if self.ui_page_appear(page_sweep):
                self.device.click(EQUIPMENT_EXIT)
                continue
            if self.ui_page_appear(page_stuff):
                self.device.click(EQUIPMENT_EXIT)
                continue
            if self.ui_page_appear(page_equipment):
                self.device.click(EQUIPMENT_EXIT)
                continue


az=Equipment('alas',task='Alas')
az.handle_equipment()

