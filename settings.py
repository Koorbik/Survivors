# game setup
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64
LEVEL = 0
WAVE_SIZE = 0
enemies = []

BAR_HEIGHT = 20
BAR_WIDTH = 200
UI_FONT = 'graphics/Font/Baron Neue.otf'
UI_FONT_SIZE = 30

# colors
UI_BG_COLOR = (54, 51, 51)
UI_TEXT_COLOR = (255, 255, 255)
UI_BORDER_COLOR = (255, 255, 255)
HEALTH_COLOR = (255, 0, 0)
UI_BORDER_COLOR = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'


# weapons
weapon_data = {
    'tornado': {'cooldown': 20, 'damage': 20}}

# enemy
enemies = []
enemy_data = {
    'tomato': {'health': 100, 'damage': 12, 'speed': 3, 'resistance': 5, 'attack_radius': 50},
    'slug': {'health': 200, 'damage': 5, 'speed': 2, 'resistance': 5, 'attack_radius': 40},
    'spirit': {'health': 100, 'damage': 8,  'speed': 4, 'resistance': 5, 'attack_radius': 30},
    'devil': {'health': 70, 'damage': 6,  'speed': 3, 'resistance': 5, 'attack_radius': 30}}
