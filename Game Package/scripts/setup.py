my_colors = []
my_species = []
my_turn_position = 0
HOME_DICT = {0: "p1_home", 1: "p2_home", 2: "p3_home", 3: "p4_home",}
FRONTIER_DICT = {0: "p1_frontier", 1: "p2_frontier", 2: "p3_frontier", 3: "p4_frontier",}


def head_count(args):
    # Makes sure all players have loaded an army, then automatically builds the table.
    mute()
    
    # This prevents the function for running once for each player, as it is called each time a deck is loaded.
    if args.player == me:
        if me._id == 1:
        # Checks to see if the player is the host
            build_turn_order()
            for p in players:
                remoteCall(p, "get_my_turn_position", [])
        ready_players = int(getGlobalVariable("player_counter"))
        ready_players += 1
        
        # Make sure all players have loaded a deck and then build the table
        if ready_players == len(players):
            setGlobalVariable("player_counter", "0")
            for p in players:
                remoteCall(p, "store_terrain", [])
                remoteCall(p, "load_terrain", [])
                remoteCall(p, "load_armies", [])
                remoteCall(p, "build_colors", [])
                remoteCall(p, "build_species", [])
                remoteCall(p, "build_spells", [])
                remoteCall(p, "point_calculator", [])
                remoteCall(p, "hash_report", [])
        else:
            setGlobalVariable("player_counter", str(ready_players))


#############################
#        Turn Setup         #
#############################


def build_turn_order():
    # Builds a list of all player IDs and stores it as a global variable, to lock in turn order
    playerIDList = []
    check = getGlobalVariable("turn_order")
    if check != "0":
        return
    for player in players:
        if not player.isInverted: playerIDList.append(str(player._id))
    for player in players:
        if player.isInverted: playerIDList.append(str(player._id))
    setGlobalVariable("turn_order", ",".join(playerIDList))


def get_my_turn_position():
    # Finds what position a player is in the turn sequence,
    # used by other functions to determine which terrain is their home, etc
    global my_turn_position
    turn_order = getGlobalVariable("turn_order")
    playerIDList = turn_order.split(",")
    playerIDList = [int(i) for i in playerIDList]
    my_position = playerIDList.index(me._id)
    my_turn_position = my_position


#############################
#       Terrain Setup       #
#############################
        
        
def load_terrain():
    # Searches the player's decks for major terrain and moves them to the table. 
    mute()
    terrain = invert_check()
    for die in me.piles["Home Army"]:
        if die.Type == "Major Terrain":
            die.moveToTable(terrain["Home Terrain"][0], terrain["Home Terrain"][1])
            if me.isInverted:
                setGlobalVariable("p2_home", str(die._id))
            else:
                setGlobalVariable("p1_home", str(die._id))
    for die in me.piles["Campaign Army"]:
        if die.Type == "Major Terrain":
            die.moveToTable(terrain["Frontier Terrain"][0], terrain["Frontier Terrain"][1])


def store_terrain():
    global my_turn_position
    home_id = 0
    frontier_id = 0
    for die in me.piles["Home Army"]:
        if die.Type == "Major Terrain":
            home_id = die._id
    for die in me.piles["Campaign Army"]:
        if die.Type == "Major Terrain":
            frontier_id = die._id
    if home_id != 0:
        setGlobalVariable(HOME_DICT[my_turn_position], str(home_id))
    else:
        notifyBar("#FF0000", "{} did not load their home terrain properly. Please manually set your home terrain.".format(me))
    if frontier_id != 0:
        setGlobalVariable(FRONTIER_DICT[my_turn_position], str(frontier_id))
    else:
        notifyBar("#FF0000", "{} did not load their frontier terrain properly. Please manually set your frontier terrain.".format(me))

def set_home(die, x=0, y=0):
    global my_turn_position
    if die.Type == "Major Terrain":
        home_id = die._id
        setGlobalVariable(HOME_DICT[my_turn_position], str(home_id))
        terrain = invert_check()
        die.moveToTable(terrain["Home Terrain"][0], terrain["Home Terrain"][1])
        notify("{} has set {} as their home terrain.".format(me, die))
    else:
        whisper("That die can't be your home terrain. Please try again.")
        
        
def set_frontier(die, x=0, y=0):
    global my_turn_position
    if die.Type == "Major Terrain":
        frontier_id = die._id
        setGlobalVariable(FRONTIER_DICT[my_turn_position], str(frontier_id))
        terrain = invert_check()
        die.moveToTable(terrain["Frontier Terrain"][0], terrain["Frontier Terrain"][1])
        notify("{} has set {} as their frontier terrain.".format(me, die))
    else:
        whisper("That die can't be your frontier terrain. Please try again.")

#############################
#        Army Setup         #
#############################


def load_armies():
    # Searches each player's deck and moves all the units to their appropriate zones
    # See the function 'build_army' for more detailed notes
    mute()
    coords = invert_check()
    
    # Offset determines if dice are placed left-to-right or right-to-left.
    # Shift places the dice slightly differently for the inverted player since
    # The coordinates are calculated based on the non-inverted player's view.
    if me.isInverted:
        offset = -1
        shift = 75
    else:
        offset = 1
        shift = 0
    army_count = 0
    
    # Iterate through the four initial zones (Home, Campaign, Horde, and Summoning Pool)
    while army_count < 4:
        loc = ARMIES[army_count]
        full_army = [d for d in me.piles[loc]]
        sorted = sort_army(full_army)
        x = coords[loc][0]
        y = coords[loc][1]
        die_shift = 0
        die_count = 0
        for _ in range(0, len(sorted)):
            if len(me.piles[loc]) > 0:
                die = sorted[die_count]
                if me.isInverted:
                    die.moveToTable(x + 70 - die.width + (die_shift * offset), y + 60 - die.height)
                else:
                    die.moveToTable(x + (die_shift * offset), y)
                die_shift += die.width + 5
                die_count += 1
                if me.isInverted: 
                    if die.position[0] < coords[loc][2] + 60:
                        die_shift = 10
                        y += 70 * offset
                elif not me.isInverted:
                    if die.position[0] > coords[loc][2] - 50:                
                        die_shift = 0
                        y += 70 * offset
        army_count += 1


#############################
#     Points Calculator     #
#############################

def point_calculator():
    # Calculates the points value of the army the player loaded
    mute()
    points = 0
    summon = 0
    modify = 0
    dracolem = 0
    army_count = 0
    
    # Total up each of the different die types
    for die in table:
        if die.controller == me:
            points += unit_calc(die)
            points += item_calc(die)
            modify += medium_correction(die)
            summon += summon_calc(die)
            dracolem += dracolem_calc(die)
    # Adjust points total to account for pairs of medium-sized items
    points -= modify // 2
    summon_items = dracolem_verify(dracolem)
    notify("{} has loaded an army with {} total points, and {} points in their summoning pool. ".format(me, points, summon))
    if dracolem > 0:
        notify("They have a total of {} points of worth of Dracolem, and {} points worth of items in their Summoning Pool.".format(dracolem, summon_items))


def medium_correction(die):
    # Determines the number of medium-sized items in the player's army
    mute()
    counter = 0
    if die.Size == "Medium" and die.Type == "Item":
        counter += 1
    return counter
    

def unit_calc(die):
    mute()
    value = 0
    if die.Type == "Unit" and die.Species != "Dragonkin":
        value += UNIT_POINTS[die.Size]
    return value


def item_calc(die):
    mute()
    summon = get_army("Summoning Pool")
    value = 0
    if die in summon:
        return 0
    elif die.Type == "Item" or die.Type == "Artifact" or die.Type == "Relic":
        value += ITEM_POINTS[die.Size]
    return value


def summon_calc(die):
    mute()
    value = 0
    if die.Species == "Dragonkin":
        value += UNIT_POINTS[die.Size]
    return value
    
    
def dracolem_calc(die):
    mute()
    value = 0
    if die.Species == "Dracolem":
        value += UNIT_POINTS[die.Size]
    return value

    
def dracolem_verify(dracolem):
    value = 0
    too_big = 0
    too_many = 0
    dracolem_mod = dracolem // 3
    summon_dice_list = get_army("Summoning Pool")
    for die in summon_dice_list:
        if die.Type == "Item":
            value += ITEM_POINTS[die.Size]
        elif die.type == "Artifact" or die.Type == "Relic":
            too_big += 1
    if value > dracolem_mod:
        too_many += 1
    if too_big > 0:
        notify("{} has an invalid setup of items in their Summoning Pool. They have Artifacts and/or Relics in their Summoning Pool.".format(me))
    if too_many > 0:
        notify("{} has an invalid setup of items in their Summoning Pool. They have {} save-worth of items, but they are only allowed {}.".format(me, value, dracolem_mod))
    return value
    
    
#############################
#      Hash Reporting       #
#############################

def hash_report():
    opplist = [p for p in players if p != me]
    # whisper("Players = {}. Opplist = {}.".format(players, opplist))
    for p in opplist:
        guidstring = str(sorted([d.model for d in table if d.controller == p]))
        guidhash = hash(guidstring)
        whisper("{}'s hash is {}.".format(p, guidhash))