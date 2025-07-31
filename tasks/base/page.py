import traceback

from tasks.daily.assets.assets_daily import DAILY_CHECK, MAIN_GOTO_DAILY, DAILY_EXIT, WEEKLY_CLAIM, WEEKlY_BUTTON, \
    WEEKLY_CHECK, WEEKLY_EXIT
from tasks.mission.assets.assets_mission import MISSION_CHECK, MISSION_RED_DOT, MISSION_EXIT
from tasks.organization.assets.assets_organization import ORGANIZATION_PANEL, ORGANIZATION, ORGANIZATION_PRAY_CHECK, \
    PRAY_EXIT, ORGANIZATION_EXIT
from tasks.page.assets.assets_page import MAIN_GOTO_CHARACTER
from tasks.freebies.assets.assets_freebies_mail import *
from tasks.freebies.assets.assets_freebies_dailyshare import *
from tasks.freebies.assets.assets_freebies_friendgifts import *
from tasks.zhaocai.assets.assets_zhaocai import ZHAO_CAI_CHECK, MAIN_GOTO_ZHAO_CAI, ZHAO_CAI_GOTO_MAIN


class Page:
    # Key: str, page name like "page_main"
    # Value: Page, page instance
    all_pages = {}

    @classmethod
    def clear_connection(cls):
        for page in cls.all_pages.values():
            page.parent = None

    @classmethod
    def init_connection(cls, destination):
        """
        Initialize an A* path finding among pages.

        Args:
            destination (Page):
        """
        cls.clear_connection()

        visited = [destination]
        visited = set(visited)
        while 1:
            new = visited.copy()
            for page in visited:
                for link in cls.iter_pages():
                    if link in visited:
                        continue
                    if page in link.links:
                        link.parent = page
                        new.add(link)
            if len(new) == len(visited):
                break
            visited = new

    @classmethod
    def iter_pages(cls):
        return cls.all_pages.values()

    @classmethod
    def iter_check_buttons(cls):
        for page in cls.all_pages.values():
            yield page.check_button

    def __init__(self, check_button):
        self.check_button = check_button
        self.links = {}
        (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
        self.name = text[:text.find('=')].strip()
        self.parent = None
        Page.all_pages[self.name] = self

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def link(self, button, destination):
        self.links[destination] = button

#Main_Page
page_main=Page(MAIN_GOTO_CHARACTER)

#Mail
page_mail=Page(MAIL_CHECK)
page_mail.link(MAIL_EXIT,destination=page_main)
page_main.link(MAIN_GOTO_MAIL,destination=page_mail)
#Mission
page_mission=Page(MISSION_CHECK)
page_main.link(MISSION_RED_DOT,destination=page_mission)
page_mission.link(MISSION_EXIT,destination=page_main)
#DailyShare
page_panel=Page(PANEL_CHECK)
page_main.link(MAIN_GOTO_PANEL,destination=page_panel)
page_panel.link(PANEL_GOTO_MAIN,destination=page_main)
#Friend_Gifts
page_friend_panel=Page(FRIEND_PANEL_CHECK)
page_gifts_claim=Page(GIFTS_CLAIM_CHECK)
page_main.link(MAIN_GOTO_FRIEND_PANEL,destination=page_friend_panel)
page_friend_panel.link(FRIEND_PANEL_GOTO_MAIN,destination=page_main)
page_gifts_claim.link(GIFTS_CLAIM_CONFIRM,destination=page_friend_panel)
#Zhao_Cai
page_zhaocai=Page(ZHAO_CAI_CHECK)
page_main.link(MAIN_GOTO_ZHAO_CAI,destination=page_zhaocai)
page_zhaocai.link(ZHAO_CAI_GOTO_MAIN,destination=page_main)
#Organization
page_organization_panel=Page(ORGANIZATION_PANEL)
page_organization=Page(ORGANIZATION)
page_pray=Page(ORGANIZATION_PRAY_CHECK)
page_pray.link(PRAY_EXIT,destination=page_organization)
page_organization.link(ORGANIZATION_EXIT,destination=page_main)
#DailyReward
page_daily=Page(DAILY_CHECK)
page_main.link(MAIN_GOTO_DAILY,destination=page_daily)
page_daily.link(DAILY_EXIT,destination=page_main)
page_weekly=Page(WEEKLY_CHECK)
page_daily.link(WEEKlY_BUTTON,destination=page_weekly)
page_weekly.link(WEEKLY_EXIT,destination=page_daily)



