import numpy as np

from module.base.utils import load_image, image_size,crop
from module.logger import logger
import cv2

from tasks.mission.assets.assets_mission import MISSION_CHARACTER_GRID


def get_position_in_original_image(position_in_croped_image, crop_area):
    """
    Returns:
        tuple: (x, y) of position in original image
    """
    return (
        position_in_croped_image[0] + crop_area[0],
        position_in_croped_image[1] + crop_area[1]) if position_in_croped_image else None

class MissionCharacter:
    _image_cache = {}
    _crop_area = MISSION_CHARACTER_GRID.matched_button.area

    def __init__(self, name, screenshot, similarity=0.75):
        self.name = name
        self.image = self._scale_character()
        self.screenshot = crop(screenshot, MissionCharacter._crop_area, copy=False)
        self.similarity = similarity
        self.button = self._find_character()

    def __bool__(self):
        # __bool__ is called when use an object of the class in a boolean context
        return self.button is not None

    def __str__(self):
        return f'SupportCharacter({self.name})'

    __repr__ = __str__

    @classmethod
    def load_image(cls, file):
        image = load_image(file)
        size = image_size(image)
        # Template from support page
        if size == (86, 81):
            return image
        # Template from character list page
        if size == (95, 89):
            image = cv2.resize(image, (86, 81))
            return image
        # Unexpected size, resize anyway
        logger.warning(f'Unexpected shape from support template {file}, image size: {size}')
        cv2.resize(image, (86, 81))
        return image

    def _scale_character(self):
        """
        Returns:
            Image: Character image after scaled
        """

        if self.name in MissionCharacter._image_cache:
            logger.info(f"Using cached image of {self.name}")
            return MissionCharacter._image_cache[self.name]

        image = self.load_image(f"assets/character/{self.name}.png")
        MissionCharacter._image_cache[self.name] = image
        logger.info(f"Character {self.name} image cached")
        return image

    def _find_character(self):
        character = np.array(self.image)
        support_list_img = self.screenshot
        res = cv2.matchTemplate(
            character, support_list_img, cv2.TM_CCOEFF_NORMED)

        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        max_loc = get_position_in_original_image(
            max_loc, MissionCharacter._crop_area)
        character_width = character.shape[1]
        character_height = character.shape[0]

        return (max_loc[0], max_loc[1], max_loc[0] + character_width, max_loc[1] + character_height) \
            if max_val >= self.similarity else None

    def selected_icon_search(self):
        """
        Returns:
            tuple: (x1, y1, x2, y2) of selected icon search area
        """
        # Check the left of character avatar
        return 0, self.button[1], self.button[0], self.button[3]
