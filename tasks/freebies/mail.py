from module.base import button
from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger
from tasks.base.assets.assets_base_page import MAIN_GOTO_MAIL, MAIN_GOTO_CHARACTER
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

            if self.appear_then_click(MAIN_GOTO_MAIL,interval=2):
                continue
            if time.reached():
                raise GameStuckError("Mail enter failed")



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



        #MAIL_RED_DOT
        if not self.appear(MAIL_RED_DOT):
            logger.info("NOT FOUND MAIL_RED_DOT")
            return False


        # claim all
        self._mail_enter()

        self._mail_claim()
        self._mail_exit()


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
az.image_file=r'C:\Users\liuzy\Desktop\NarutoScript\tasks\freebies\1.png'
#print(az.ui_page_appear(page_mail))
# print(az.appear(MAIL_RED_DOT))
# print(az.appear(MAIN_GOTO_MAIL))
az.handle_mail_reward()

