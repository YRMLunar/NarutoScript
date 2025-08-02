import math
from functools import cached_property

import cv2
import numpy as np


from module.device.method.maatouch import MaatouchBuilder, retry as maatouch_retry
from module.device.method.minitouch import (
    CommandBuilder, insert_swipe, random_normal_distribution, retry as minitouch_retry)
from module.exception import ScriptError
from module.logger import logger




class JoystickContact:
    # Minimum radius 49px
    RADIUS_WALK = (25, 40)
    # Minimum radius 103px
    RADIUS_RUN = (105, 115)

    def __init__(self, main):
        """
        Args:
            main (MapControlJoystick):
        """
        self.main = main
        self.prev_point = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Lift finger when:
        - Walk event ends, JoystickContact ends
        - Any error is raised
        Can not lift finger when:
        - Process is force terminated
        """
        if self.is_downed:
            self.up()
            logger.info('JoystickContact ends')
        else:
            logger.info('JoystickContact ends but it was never downed')

    @property
    def is_downed(self):
        return self.prev_point is not None

    @cached_property
    def builder(self):
        """
        Initialize a command builder
        """
        method = self.main.config.Emulator_ControlMethod
        if method == 'MaaTouch':
            # Get the very first builder to initialize MaaTouch
            _ = self.main.device.maatouch_builder
            builder = MaatouchBuilder(self.main.device, contact=1)
        elif method == 'minitouch':
            # Get the very first builder to initialize minitouch
            _ = self.main.device.minitouch_builder
            builder = CommandBuilder(self.main.device, contact=1)
        else:
            raise ScriptError(f'Control method {method} does not support multi-finger, '
                              f'please use MaaTouch or minitouch instead')

        # def empty_func():
        #     pass
        #
        # # No clear()
        # builder.clear = empty_func
        # No delay
        builder.DEFAULT_DELAY = 0.

        return builder

    def with_retry(self, func):
        method = self.main.config.Emulator_ControlMethod
        if method == 'MaaTouch':
            retry = maatouch_retry
        elif method == 'minitouch':
            retry = minitouch_retry
        else:
            raise ScriptError(f'Control method {method} does not support multi-finger')

        return retry(func)(self)

    @classmethod
    def direction2screen(cls, direction, run=True):
        """
        Args:
            direction (int, float): Direction to goto (-180~180)
            run: True for character running, False for walking

        Returns:
            tuple[int, int]: Position on screen to control joystick
        """
        direction += random_normal_distribution(-5, 5, n=5)
        radius = cls.RADIUS_RUN if run else cls.RADIUS_WALK
        radius = random_normal_distribution(*radius, n=5)
        direction = math.radians(direction)

        # Contact at the lower is limited within `cls.CENTER[1] - half_run_radius`
        # or will exceed the joystick area
        # Random radius * multiplier makes the point randomly approaching the lower bound
        for multiplier in [1.0, 0.95, 0.90, 0.85, 0.80, 0.75]:
            point = (
                cls.CENTER[0] + radius * multiplier * math.sin(direction),
                cls.CENTER[1] - radius * multiplier * math.cos(direction),
            )
            point = (int(round(point[0])), int(round(point[1])))
            if point[1] <= cls.CENTER[1] - 101:
                return point
        return point

    def up(self):
        if not self.is_downed:
            return
        logger.info('JoystickContact up')
        builder = self.builder

        def _up(_self):
            builder.up().commit()
            builder.send()
        self.with_retry(_up)
        self.prev_point = None

    def set(self, direction, run=True):
        """
        Set joystick to given position

        Args:
            direction (int, float): Direction to goto (-180~180)
            run: True for character running, False for walking
        """
        logger.info(f'JoystickContact set to {direction}, run={run}')
        point = JoystickContact.direction2screen(direction, run=run)
        builder = self.builder

        if self.is_downed and not self.main.joystick_speed():
            if self.main.joystick_lost_timer.reached():
                logger.warning(f'Joystick contact lost: {self.main.joystick_lost_timer}, re-down')
                self.up()
        else:
            self.main.joystick_lost_timer.reset()

        if self.is_downed:
            points = insert_swipe(p0=self.prev_point, p3=point, speed=20)

            def _set(_self):
                for p in points[1:]:
                    builder.move(*p).commit().wait(10)
                builder.send()

            self.with_retry(_set)
        else:
            def _set(_self):
                builder.down(*point).commit()
                builder.send()

            self.with_retry(_set)
            # Character starts moving, RUN button is still unavailable in a short time.
            # Assume available in 0.3s
            # We still have reties if 0.3s is incorrect.
            self.main.map_run_2x_timer.set_current(0.7)
            self.main.joystick_lost_timer.reset()

        self.prev_point = point


