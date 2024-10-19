import json
import time
import requests
from disnake.ext import commands

from scrts import BOT_TOKEN, HYPIXEL_API_KEY


HYPIXEL_GUILD_ID: str = "639d0c668ea8c9185c70caf9"

BOT_DEVELOPER_ID: int = 447861538095759365
BOT_DEVELOPER_MENTION: str = f"<@{BOT_DEVELOPER_ID}>"

STAFF_ROLE: int = 1244837447846592535

VERIFICATION_CHANNEL: int = 1240047359946133624
VERIFICATION_LOG_CHANNEL: int = 1293009280261427330
STAFF_CHANNEL: int = 1183198328045977721
BOT_DEV_CHANNEL: int = 1263673819239809135
LOG_CHANNEL: int = 1264027690332323941

GUILD_ID = 934240413974417439

VERIFIED_ROLE: int = 1240044060102623394
POSSIBLE_SCAMMER_ROLE: int = 935288721199214612
GUILD_MEMBER_ROLE: int = 1249863227014250527

DCTR_SPACE_HELM_ROLE: int = 1134970805810385017
SPACE_HELM_ROLE: int = 1261200854132985967
RAFFLE_SPACE_HELM_ROLE: int = 1261200915109773405

ITEM_ID_ROLES: dict[str, int] = {
    "KLOONBOAT": 1217172737160904715, # @Kloonboat
    "ANCIENT_ELEVATOR": 1134970925784256572, # @Ancient Elevator
    "CREATIVE_MIND": 1201988405420888155, # @Creative Mind
    "GAME_BREAKER": 1221149287484887141, # @Gamebreaker
    "POTATO_BASKET": 1261201356073603072, # @Basket of Hope
    "DEAD_BUSH_OF_LOVE": 1245118825746268190, # @Dead Bush of Love*
    "SNOW_SNOWGLOBE": 1221630825830027325, # @Snowglobe
    "WIKI_JOURNAL": 1296881300711538749, # @Wiki Editor
    "EDITOR_PENCIL": 1296881300711538749, # @Wiki Editor
    "GAME_ANNIHILATOR": 1295563935096766485, # @Game Annihilator
    "SHINY_RELIC": 1295569295195242586, # @Shiny Relic
    "POTATO_SILVER_MEDAL": 1295569723118981171, # @Potato War Silver Medal
    "POTATO_CROWN": 1295569723118981171, # @Potato War Silver Medal (this gives the same role because I wanted to for fun, but i cba to make a seperate role for it)
    
    # You must have ALL of these items:
    "MAGIC_CUBE_FLUX,GOLDEN_ANCIENT_EGG_FLUX,PIRATE_BOMB_FLUX,GLISTENING_MELON_FLUX,GOLDEN_APPLE_FLUX,GLOWING_GRAPE_FLUX,MYSTIC_MOON_FLUX,BEACH_BALL_FLUX,CHERRY_BLOSSOM_FLUX,POLAR_LIGHTS_FLUX": 1132783153044529283, # @Power Orb Skins
    "PET_SKIN_SHEEP_NEON_BLUE,PET_SKIN_SHEEP_NEON_GREEN,PET_SKIN_SHEEP_ORANGE,PET_SKIN_SHEEP_WHITE,PET_SKIN_SHEEP_RED,PET_SKIN_SHEEP_GREEN,PET_SKIN_SHEEP_LIGHT_GREEN,PET_SKIN_SHEEP_LIGHT_GRAY,PET_SKIN_SHEEP_LIGHT_BLUE,PET_SKIN_SHEEP_BLUE,PET_SKIN_SHEEP_BLACK,PET_SKIN_SHEEP_YELLOW,PET_SKIN_SHEEP_GRAY,PET_SKIN_SHEEP_PURPLE,PET_SKIN_SHEEP_NEON_RED,PET_SKIN_SHEEP_BROWN,PET_SKIN_SHEEP_PINK,PET_SKIN_SHEEP_MAGENTA,PET_SKIN_SHEEP_NEON_YELLOW,PET_SKIN_SHEEP_AQUA": 934254703578079292, # @Sheep Skins
    "PET_SKIN_SHEEP_NEON_BLUE,PET_SKIN_SHEEP_NEON_GREEN,PET_SKIN_SHEEP_NEON_RED,PET_SKIN_SHEEP_NEON_YELLOW": 934837443964842045, # @Neon Skins
    "PET_SKIN_ROCK_COOL,PET_SKIN_ROCK_THINKING,PET_SKIN_ROCK_DERP,PET_SKIN_ROCK_EMBARRASSED,PET_SKIN_ROCK_LAUGH,PET_SKIN_ROCK_SMILE": 934254691796262992, # @Rock Skins
    "HOLY_BABY,YOUNG_BABY,STRONG_BABY,UNSTABLE_BABY,OLD_BABY,WISE_BABY,PROTECTOR_BABY,SUPERIOR_BABY,PET_SKIN_MEGALODON_BABY": 934254704026857483, # @Baby Skins
    "PET_SKIN_ELEPHANT_BLUE,PET_SKIN_ELEPHANT_MONOCHROME,PET_SKIN_ELEPHANT_GREEN,PET_SKIN_ELEPHANT_RED,PET_SKIN_ELEPHANT_PINK,PET_SKIN_ELEPHANT_ORANGE,PET_SKIN_ELEPHANT_PURPLE": 934254929957224568, # @Elephant Skins
    "HOLY_SHIMMER,STRONG_SHIMMER,SUPERIOR_SHIMMER,WISE_SHIMMER,UNSTABLE_SHIMMER,PROTECTOR_SHIMMER,YOUNG_SHIMMER,OLD_SHIMMER": 934255771162669107, # @Shimmer Skins
    "RABBIT_JERRY_ONESIE,PET_SKIN_JERRY_LEPRECHAUN,PET_SKIN_JERRY_KING,PET_SKIN_JERRY_HANDSOME,PET_SKIN_JERRY_FROZEN": 1218028528298102834, # @Jerry Skins
}

RANK_ROLES: dict[str, int] = {
    "YOUTUBER": 935002292791427092, # @Content Creator
    "ADMIN": 1295140666640171018, # @Hypixel Staff
    "GAMEMASTER": 1295140666640171018 # @Hypixel Staff
}

REQUIRES_VERIFICATION: list[int] = [
    VERIFIED_ROLE,
    GUILD_MEMBER_ROLE,
    DCTR_SPACE_HELM_ROLE,
    SPACE_HELM_ROLE,
    RAFFLE_SPACE_HELM_ROLE
]\
    + list(ITEM_ID_ROLES.values())\
    + list(RANK_ROLES.values())


response = None
while response is None or response.status_code != 200:
    print('getting guild data...')
    response = requests.get(f'https://api.hypixel.net/v2/guild?key={HYPIXEL_API_KEY}&id={HYPIXEL_GUILD_ID}')
    if response.status_code != 200:
        print(response.status_code, json.dumps(response.json(), indent=2))
        time.sleep(2)
guild_members: list[str] = [member['uuid'] for member in response.json()['guild']['members']]
