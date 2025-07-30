from module.config.stored.classes import (
    StoredAssignment,
    StoredBase,
    StoredBattlePassLevel,
    StoredBattlePassQuestCalyx,
    StoredBattlePassQuestCavernOfCorrosion,
    StoredBattlePassQuestCredits,
    StoredBattlePassQuestEchoOfWar,
    StoredBattlePassQuestStagnantShadow,
    StoredBattlePassQuestSynthesizeConsumables,
    StoredBattlePassQuestTrailblazePower,
    StoredBattlePassSimulatedUniverse,
    StoredBattlePassWeeklyQuest,
    StoredCounter,
    StoredDaily,
    StoredDailyActivity,
    StoredDungeonDouble,
    StoredEchoOfWar,
    StoredExpiredAt0400,
    StoredExpiredAtMonday0400,
    StoredImmersifier,
    StoredInt,
    StoredPlanner,
    StoredPlannerOverall,
    StoredRelic,
    StoredResersed,
    StoredSimulatedUniverse,
    StoredSimulatedUniverseElite,
    StoredTrailblazePower,
)


# This file was auto-generated, do not modify it manually. To generate:
# ``` python -m module/config/config_updater.py ```

class StoredGenerated:
    # Credit = StoredInt("DataUpdate.ItemStorage.Credit")
    # StallerJade = StoredInt("DataUpdate.ItemStorage.StallerJade")
    # Planner items - 设为固定值 0
    PlannerOverall = 0
    Item_Credit = 0
    Item_Trailblaze_EXP = 0
    Item_Traveler_Guide = 0
    # ... 所有 Item_ 开头的项目都设为 0

    # Storage items - 设为固定值
    TrailblazePower = 240  # 固定开拓力值
    Reserved = 0
    Fuel = 0
    Immersifier = 0
    DungeonDouble = 0
    EchoOfWar = 3  # 固定每周次数
    SimulatedUniverse = 0
    Relic = 1500  # 固定遗器数量

    # Daily items
    DailyActivity = 500  # 固定每日活跃度
    DailyQuest = 0

    # Battle Pass items
    BattlePassLevel = 50  # 固定战令等级
    BattlePassWeeklyQuest = 0
    # ... 其他战令任务设为 0

    # Assignment
    Assignment = 0

    # DataUpdate items
    Credit = 1000000  # 固定信用点
    StallerJade = 5000   # 固定星琼
    CloudRemainSeasonPass = 0
    CloudRemainPaid = 0
    CloudRemainFree = 0

    # Rogue
    SimulatedUniverseFarm = 100
