'''
------------------------------------------------------------------------------
-- MODULES AND PACKAGES --
------------------------------------------------------------------------------
'''

import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import urllib.request
from PIL import Image
import numpy as np

# LOCAL DATABASES
from databases.characters import characters_data as chrData
from databases.weapons import weapons_data as wpnData
from databases.pfps import pfp_data as pfpData
from databases.namecards import namecards_data as nmcData
from databases.definations import prop, fightProp, itemType, equipType, appendProp
from databases.charsInfo import characters as chr


'''
------------------------------------------------------------------------------
-- FUNCTIONS --
------------------------------------------------------------------------------
'''


# FUNCTION TO DISPLAY AN IMAGE FROM URL (USES urllib, numpy, PIL, matplolib)
def display_image(url):
    # Set up a request with a User-Agent header to mimic a browser
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    
    # Open the URL and read the image with Pillow
    with urllib.request.urlopen(req) as response:
        img = Image.open(response)

    img.show()
    



def fetch_user_data_by_uid(uid):
    url = "https://enka.network/api/uid/" + uid + "/"
    response_string = requests.get(url)
    
    # HANDLING ERRORS
    if response_string.status_code == 400:
        raise Exception("Wrong UID format")
    elif response_string.status_code == 404:
        raise Exception("Player does not exist (MiHoYo server said that)")
    elif response_string.status_code == 424:
        raise Exception("Game maintenance")
    elif response_string.status_code == 429:
        raise Exception("Too many requests")
    elif response_string.status_code == 500:
        raise Exception("General Server Error")
    else:
        response = response_string.json()

        if response['uid'] == uid and "playerInfo" in response:
            return response
        else:
            raise Exception("Failed to fetch data :(")
        
def create_player_object(response):
    # SIGNATURE
    if 'signature' not in response:
        signature = 'No signature'
    else:
        signature = response['signature']
    
    # WORLD LEVEL
    if 'worldLevel' not in response:
        if data['level'] < 20:
            worldLevel = 0
        elif data['level'] >= 20:
            worldLevel = 1
    else:
        worldLevel = response['worldLevel']

    # SPIRAL ABYSS
    if 'towerFloorIndex' not in response:
        abyssFloor = 'No record found'
        abyssChamber = ''
        abyssStars = ''
    else:
        abyssFloor = data['towerFloorIndex']
        abyssChamber = data['towerLevelIndex']
        abyssStars = data['towerStarIndex']

    # IMAGINARIUM THEATRE
    if 'theaterActIndex' not in response:
        theaterAct = 'No record found'
        theaterStars = ''
    else:
        theaterAct = data['theaterActIndex']
        theaterStars = data['theaterStarIndex']


    # object creation
    player = Player(uid, response['nickname'], signature, response['level'], worldLevel, response['nameCardId'], response['finishAchievementNum'], abyssFloor, abyssChamber, abyssStars, theaterAct, theaterStars)
    return player


# Character Showcase
def char_showcase_brief(response):
    if "avatarInfoList" not in response:
        print("Unable to fetch data from character showcase. Make sure ur showcase is PUBLIC and it is having atleast 1 character.")
    else:
        for i in response["avatarInfoList"]:
            avatarId = i["avatarId"]    # int
            characterName = chr[str(avatarId)]['Name']
            characterLevel = i['propMap']['4001']['val']
            

    pass



   
'''
------------------------------------------------------------------------------
-- CLASSES AND OBJECTS --
------------------------------------------------------------------------------
'''



class Player:
    def __init__(self, uid, name, signature, level, worldLevel, nameCardId, achievement, abyssFloor, abyssChamber, abyssStars, theatreAct, theatreStar):
        self.uid = uid
        self.name = name
        self.signature = signature
        self.level = level
        self.worldLevel = worldLevel
        self.nameCardId = nameCardId
        self.achievement = achievement
        self.abyssFloor = abyssFloor
        self.abyssChamber = abyssChamber
        self.abyssStars = abyssStars
        self.theatreAct = theatreAct
        self.theatreStar = theatreStar

    def displayBriefInfo(self):
        print("\nShowing brief info...")
        print("========================================")
        print(f"UID : {self.uid}\nName : {self.name}\nLevel : {self.level}\nWorld Level : {self.worldLevel}\nAchievements : {self.achievement}")

    def displayDetailedInfo(self):
        print("\nShowing detailed info...")
        print("========================================")
        if self.abyssFloor == 'No record found' and self.theatreAct == 'No record found':
            print(f"UID : {self.uid}\nName : {self.name}\nSignature : {self.signature}\nLevel : {self.level}\nWorld Level : {self.worldLevel}\nAchievements : {self.achievement}\nSpiral Abyss : {self.abyssFloor}\nImaginarium Theatre : {self.theatreAct}")
        elif self.abyssFloor == 'No record found':
            print(f"UID : {self.uid}\nName : {self.name}\nSignature : {self.signature}\nLevel : {self.level}\nWorld Level : {self.worldLevel}\nAchievements : {self.achievement}\nSpiral Abyss : {self.abyssFloor}\nImaginarium Theatre : Act {self.theatreAct} | {self.theatreStar}☆")
        elif self.theatreAct == 'No record found':
            print(f"UID : {self.uid}\nName : {self.name}\nSignature : {self.signature}\nLevel : {self.level}\nWorld Level : {self.worldLevel}\nAchievements : {self.achievement}\nSpiral Abyss : Floor {self.abyssFloor} Chamber {self.abyssChamber} | {self.abyssStars}☆\nImaginarium Theatre : {self.theatreAct}")
        else:
            print(f"UID : {self.uid}\nName : {self.name}\nSignature : {self.signature}\nLevel : {self.level}\nWorld Level : {self.worldLevel}\nAchievements : {self.achievement}\nSpiral Abyss : Floor {self.abyssFloor} Chamber {self.abyssChamber} | {self.abyssStars}☆\nImaginarium Theatre : Act {self.theatreAct} | {self.theatreStar}☆")





# ================================================================================
# MAIN
print("Welcome to HoYo-X!")
uid = input("Enter Genshin UID: ")  # Me: 1801549844  IO: 812426168
print("Fetching data from server...")
print("Please wait...")

try:
    response = fetch_user_data_by_uid(uid)
    data = response['playerInfo']
    player = create_player_object(data)
    
except Exception as error:
    print(error)


# display_image("https://enka.network/ui/UI_Gacha_AvatarImg_Nahida.png")

# MENU DRIVEN
# while True:
#     print("\nMenu:")
#     print("1. Display account info")
#     print("2. Display character showcase")
#     print("3. Show detailed character builds")
# player.displayBriefInfo()
# player.displayDetailedInfo()
# ================================================================================

