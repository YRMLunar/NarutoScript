from module.base import button
from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger

from tasks.base.page import  page_main, page_mail
from tasks.base.ui import UI
from tasks.freebies.assets.assets_freebies_mail import *


class MailReward(UI):
    def _mail_enter(self):
        """
        Pages:
            in: page_menu
            out: MAIL_CHECK
        """
        logger.info('Mail enter')
        time=Timer(4,count=8).start()
        for _ in self.loop():
            if self.appear(MAIL_CHECK):
                logger.info('Mail enter success')
                break
            if time.reached():
                raise GameStuckError("Mail enter failed")
            if self.appear_then_click(MAIL_RED_DOT,interval=2):
                continue

    def _mail_exit(self):
        """
        Pages:
            in: MAIL_CHECK
            out: page_menu
        """
        logger.info('Mail exit')

        time=Timer(4,count=8).start()
        for _ in self.loop():
            if self.ui_page_appear(page_main):
                logger.info('go to page main')
                break
            if  self.appear_then_click(MAIL_EXIT,interval=2):
                logger.info('Mail exit done')
                continue
            if time.reached():
                raise GameStuckError("Mail exit failed")





    def _mail_claim(self):
        """
        Pages:
            in: CLAIM_ALL
            out: CLAIM_ALL_DONE
        """
        self.ui_ensure(page_mail)
        logger.info('Mail claim all')
        time=Timer(4,count=8).start()
        for _ in self.loop():
            if self.appear(CLAIM_ALL,interval=1):
                self.device.click(CLAIM_ALL)
                continue

            if self.appear(CLAIM_ALL_DONE):
                break
            if time.reached():
                raise GameStuckError("Mail claim all failed")





    def handle_mail_reward(self):
        """
        Claim mails and exit

        Returns:
            bool: If claimed

        Pages:
            in: page_menu
            out: page_menu
        """

        self.ui_ensure(page_main)

        #MAIL_RED_DOT
        if self.appear(MAIL_RED_DOT):
            # claim all
            self._mail_enter()
            self._mail_claim()
            self._mail_exit()
            return True
        else:
            logger.info('Mail Not Found Red Dot')
            return False


    def _mail_delete(self):
        timeout = Timer(1.5, count=3).start()
        for _ in self.loop():
            if self.appear_then_click(CLAIM_DELETE,interval=1):
                continue
            if self.appear_then_click(CLAIM_DELETE_POPUP,interval=1):
                break
            if timeout.reached():
                break

az=MailReward('alas',task='Alas')
az.image_file=r'C:\Users\刘振洋\Desktop\StarRailCopilot\tasks\freebies\MuMu12-20250731-132002.png'
#print(az.ui_page_appear(page_mail))
# print(az.appear(MAIL_RED_DOT))
# print(az.appear(MAIN_GOTO_MAIL))
az.handle_mail_reward()

