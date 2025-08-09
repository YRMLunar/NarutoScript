import traceback

from tasks.base.assets.assets_base_page import *
from tasks.daily.assets.assets_daily_daily import *
from tasks.daily.assets.assets_daily_weekly import *
from tasks.organization.assets.assets_organization_pray import *
from tasks.organization.assets.assets_organization_replacement import *
from tasks.organization.assets.assets_organization_boxclaim import *
from tasks.tili.assets.assets_tili_equipment import *
from tasks.trail.assets.assets_trail import *
from tasks.trail.assets.assets_trail_survival import *
from tasks.trail.assets.assets_trail_cultivation import *
from tasks.zhaocai.assets.assets_zhaocai import *
from tasks.fengrao.assets.assets_fengrao import *
from tasks.squadraid.assets.assets_squadraid_fight import *
from tasks.squadraid.assets.assets_squadraid_benefit import *
from tasks.mission.assets.assets_mission import *
from tasks.freebies.assets.assets_freebies_mail import *
from tasks.freebies.assets.assets_freebies_dailyshare import *
from tasks.freebies.assets.assets_freebies_friendgifts import *
from tasks.login.assets.assets_login import *



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
#SquadRaid
page_squad=Page(SQUAD_RAID_CHECK)
page_main.link(MAIN_GOTO_SQUAD_RAID,destination=page_squad)
page_squad_help_battle=Page(HELP_BATTLE_GOTO_MINE)
page_squad_help_battle_mine=Page(HELP_BATTLE_MINE_CHECK)
page_squad.link(SQUAD_GOTO_HELP_BATTLE,destination=page_squad_help_battle)
page_squad_help_battle.link(HELP_BATTLE_GOTO_MINE,destination=page_squad_help_battle_mine)
page_squad_help_battle_mine.link(HELP_BATTLE_MINE_EXIT,destination=page_squad_help_battle)
page_squad_help_battle.link(SQUAD_RAID_EXIT,destination=page_squad)
page_squad.link(SQUAD_RAID_EXIT,destination=page_main)
#FengRao
page_feng_rao=Page(FENG_RAO_CHECK)
page_main.link(MAIN_GOTO_FENG_RAO,destination=page_feng_rao)
page_feng_rao.link(FENG_RAO_EXIT,destination=page_main)
#SurvivalTrail
page_trail=Page(TRAIL_SURVIVAL_CHECK)
page_survival_trail=Page(SURVIVAL_PAGE_CHECK)
page_trail.link(TRAIL_SURVIVAL_CHECK,destination=page_survival_trail)
page_survival_trail.link(SURVIVAL_EXIT,destination=page_trail)
page_trail.link(TRAIL_EXIT,destination=page_main)
#CultivationRoad
page_cultivation=Page(CULTIVATION_PAGE_CHECK)
page_cultivation_box=Page(CULTIVATION_BOX_CHECK)
page_trail.link(TRAIL_CULTIVATION_CHECK,destination=page_cultivation)
page_cultivation_box.link(CULTIVATION_EXIT,page_cultivation)
page_cultivation.link(CULTIVATION_BOX,destination=page_cultivation_box)

#Equipment
page_equipment=Page(EQUIPMENT_CHECK)
page_stuff=Page(STUFF_CHECK)
page_sweep=Page(SWEEP_CHECK)
page_sweep.link(EQUIPMENT_EXIT,destination=page_stuff)
page_stuff.link(EQUIPMENT_EXIT,destination=page_equipment)
page_equipment.link(EQUIPMENT_EXIT,destination=page_main)


