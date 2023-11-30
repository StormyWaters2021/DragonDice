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
    roll_calc = calculate_army(location, MELEE, "Melee")
    notify(roll_calc["final"])


def missile_roll(table, x, y):
    location = zone_check(x, y)
    if location == None:
        whisper("You didn't select a valid area. Please try again.")
        return
    roll_army(location)
    roll_calc = calculate_army(location, MISSILE, "Missile")
    notify(roll_calc["final"])
    

def magic_roll(table, x, y):
    location = zone_check(x, y)
    if location == None:
        whisper("You didn't select a valid area. Please try again.")
        return
    roll_army(location)
    roll_calc = calculate_army(location, MAGIC, "Magic")
    notify(roll_calc["final"])
    
    
def maneuver_roll(table, x, y):
    location = zone_check(x, y)
    if location == None:
        whisper("You didn't select a valid area. Please try again.")
        return
    roll_army(location)
    roll_calc = calculate_army(location, MANEUVER, "Maneuver")
    notify(roll_calc["final"])
    
    
def save_roll(table, x, y):
    location = zone_check(x, y)
    if location == None:
        whisper("You didn't select a valid area. Please try again.")
        return
    roll_army(location)
    roll_calc = calculate_army(location, SAVE, "Save")
    notify(roll_calc["final"])
    

# These functions pass an army and action type to calculate without rolling again
    
def melee_calc(table, x, y):
    location = zone_check(x, y)
    if location == None:
        whisper("You didn't select a valid area. Please try again.")
        return
    roll_calc = calculate_army(location, MELEE, "Melee")
    notify(roll_calc["final"])


def missile_calc(table, x, y):
    location = zone_check(x, y)
    if location == None:
        whisper("You didn't select a valid area. Please try again.")
        return
    roll_calc = calculate_army(location, MISSILE, "Missile")
    notify(roll_calc["final"])
    

def magic_calc(table, x, y):
    location = zone_check(x, y)
    if location == None:
        whisper("You didn't select a valid area. Please try again.")
        return
    roll_calc = calculate_army(location, MAGIC, "Magic")
    notify(roll_calc["final"])
    
    
def maneuver_calc(table, x, y):
    location = zone_check(x, y)
    if location == None:
        whisper("You didn't select a valid area. Please try again.")
        return
    roll_calc = calculate_army(location, MANEUVER, "Maneuver")
    notify(roll_calc["final"])
    
    
def save_calc(table, x, y):
    location = zone_check(x, y)
    if location == None:
        whisper("You didn't select a valid area. Please try again.")
        return
    roll_calc = calculate_army(location, SAVE, "Save")
    notify(roll_calc["final"])


# These functions figure out which actions are available to us automatically

def terrain_check_melee(table, x=0, y=0):
    location = zone_check(x, y)
    if location not in MARCHING_LOCATIONS:
        return False
    action_list = two_player_terrain_check(location)
    if "Melee" in action_list:
        return True
    else: return False

        
        
def terrain_check_missile(table, x=0, y=0):
    location = zone_check(x, y)
    if location not in MARCHING_LOCATIONS:
        return False
    action_list = two_player_terrain_check(location)
    if "Missile" in action_list:
        return True
    else: return False
  
  
def terrain_check_magic(table, x=0, y=0):
    location = zone_check(x, y)
    if location not in MARCHING_LOCATIONS:
        return False
    action_list = two_player_terrain_check(location)
    if "Magic" in action_list:
        return True
    else: return False
    
# These fumctions create dice on the table

def create_amazons(table, x, y):
    add_die_to_table("Species", "Amazons", x, y)
    
def create_coral(table, x, y):
    add_die_to_table("Species", "Coral Elves", x, y)
    
def create_dwarves(table, x, y):
    add_die_to_table("Species", "Dwarves", x, y)
    
def create_eldarim(table, x, y):
    add_die_to_table("Species", "Eldarim", x, y)
    
def create_feral(table, x, y):
    add_die_to_table("Species", "Feral", x, y)
    
def create_firewalkers(table, x, y):
    add_die_to_table("Species", "Fire Walkers", x, y)
    
def create_frostwings(table, x, y):
    add_die_to_table("Species", "Frostwings", x, y)
    
def create_goblins(table, x, y):
    add_die_to_table("Species", "Goblins", x, y)
    
def create_lava(table, x, y):
    add_die_to_table("Species", "Lava Elves", x, y)
    
def create_scalders(table, x, y):
    add_die_to_table("Species", "Scalders", x, y)
    
def create_swampstalkers(table, x, y):
    add_die_to_table("Species", "Swamp Stalkers", x, y)
    
def create_treefolk(table, x, y):
    add_die_to_table("Species", "Treefolk", x, y)
    
def create_undead(table, x, y):
    add_die_to_table("Species", "Undead", x, y)
    
def create_dracolem(table, x, y):
    add_die_to_table("Species", "Dracolem", x, y)
    
def create_terrain(table, x, y):
    add_die_to_table("Search", "Terrain", x, y)
    
def create_item(table, x, y):
    add_die_to_table("Search", "Items", x, y)
    
def create_dragonkin(table, x, y):
    add_die_to_table("Species", "Dragonkin", x, y)
    
def create_dragon(table, x, y):
    add_die_to_table("Search", "Dragon", x, y)