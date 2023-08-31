# This file is just pass-through functions. OCTGN uses simple calls from the table that cannot 
# pass any other arguments, so we call these functions from the table, and use these to pass the 
# arguments we need for various functions. 


# These functions send a die to a specific army

def send_to_dua(die, x=0, y=0):
    mute()
    move_to_army("DUA", die)


def send_to_bua(die, x=0, y=0):
    mute()
    move_to_army("BUA", die)


def send_to_home(die, x=0, y=0):
    mute()
    move_to_army("Home Army", die)
    
    
def send_to_campaign(die, x=0, y=0):
    mute()
    move_to_army("Campaign Army", die)


def send_to_horde(die, x=0, y=0):
    mute()
    move_to_army("Horde Army", die)


def send_to_summoning(die, x=0, y=0):
    mute()
    move_to_army("Summoning Pool", die)


def send_to_reserves(die, x=0, y=0):
    mute()
    move_to_army("Reserves", die)


# These functions reset the arrangement and faces of all dice in an area

def reset_location(table, x, y):
    location = zone_check(x, y)
    if location == None:
        whisper("You didn't select a valid area. Please try again.")
        return
    reset_army(location)

    
# These functions pass all the dice in an army to all be rolled together

def roll_home(*args):
    mute()
    roll_army("Home Army")
    

def roll_campaign(*args):
    mute()
    roll_army("Campaign Army")


def roll_horde(*args):
    mute()
    roll_army("Horde Army")
    
    
def roll_reserve(*args):
    mute()
    roll_army("Reserves")
    

# These functions pass an army and action type to roll and calculate
    
def melee_roll(table, x, y):
    location = zone_check(x, y)
    if location == None:
        whisper("You didn't select a valid area. Please try again.")
        return
    roll_army(location)
    calculate_army(location, MELEE, "Melee")


def missile_roll(table, x, y):
    location = zone_check(x, y)
    if location == None:
        whisper("You didn't select a valid area. Please try again.")
        return
    roll_army(location)
    calculate_army(location, MISSILE, "Missile")
    

def magic_roll(table, x, y):
    location = zone_check(x, y)
    if location == None:
        whisper("You didn't select a valid area. Please try again.")
        return
    roll_army(location)
    calculate_army(location, MAGIC, "Magic")
    
    
def maneuver_roll(table, x, y):
    location = zone_check(x, y)
    if location == None:
        whisper("You didn't select a valid area. Please try again.")
        return
    roll_army(location)
    calculate_army(location, MANEUVER, "Maneuver")
    
    
def save_roll(table, x, y):
    location = zone_check(x, y)
    if location == None:
        whisper("You didn't select a valid area. Please try again.")
        return
    roll_army(location)
    calculate_army(location, SAVE, "Save")
    

# These functions figure out which actions are available to us automatically

def terrain_check_melee(table, x=0, y=0):
    pass
    # action_list = terrain_actions(x, y)
    # if "Melee" in action_list:
        # return True
    # else:
        # return False
        
        
def terrain_check_missile(table, x=0, y=0):
    pass
    # action_list = terrain_actions(x, y)
    # if "Missile" in action_list:
        # return True
    # else:
        # return False
  
  
def terrain_check_magic(table, x=0, y=0):
    pass
    # action_list = terrain_actions(x, y)
    # if "Magic" in action_list:
        # return True
    # else:
        # return False