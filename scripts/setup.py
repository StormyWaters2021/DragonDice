my_colors = []
my_species = []


def head_count(args):
    # Makes sure all players have loaded an army, then automatically builds the table.
    mute()
    
    # This prevents the function for running once for each player, as it is called each time a deck is loaded.
    if args.player == me:
        ready_players = int(getGlobalVariable("player_counter"))
        ready_players += 1
        
        # Make sure all players have loaded a deck and then build the table
        if ready_players == len(players):
            setGlobalVariable("player_counter", "0")
            for p in players:
                remoteCall(p, "load_terrain", [])
                remoteCall(p, "load_armies", [])
                remoteCall(p, "build_colors", [])
                remoteCall(p, "build_species", [])
                remoteCall(p, "build_spells", [])
                remoteCall(p, "point_calculator", [])
            set_player_global()
        else:
            setGlobalVariable("player_counter", str(ready_players))
        
        
        
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


def point_calculator():
    # Calculates the points value of the army the player loaded
    mute()
    points = 0
    summon = 0
    modify = 0
    army_count = 0
    
    # Total up each of the different die types
    for die in table:
        points += unit_calc(die)
        points += item_calc(die)
        modify += medium_correction(die)
        summon += summon_calc(die)
    # Adjust points total to account for pairs of medium-sized items
    points -= modify // 2
    notify("{} has loaded an army with {} total points, and {} points in their summoning pool.".format(me, points, summon))


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
    value = 0
    if die.Type == "Item" or die.Type == "Artifact" or die.Type == "Relic":
        value += ITEM_POINTS[die.Size]
    return value


def summon_calc(die):
    mute()
    value = 0
    if die.Species == "Dragonkin":
        value += UNIT_POINTS[die.Size]
    return value
    
    
def horde_roll():
    hi_score = int(getGlobalVariable("horde_roll"))
    roll_army("Horde Army")
    horde_roll = calculate_army("Horde Army", MANEUVER, "Maneuver")
    if horde_roll < hi_score:
        return
    else:
        hi_score = horde_roll
        setGlobalVariable("horde_winner", str(me._id))
        setGlobalVariable("horde_roll", str(hi_score))
       
       
def set_player_global():
    players_dict = {0: "p1_id", 1: "p2_id", 2: "p3_id", 3: "p4_id",}
    for number in range(0, len(players)):
        id = str(players[number]._id)
        setGlobalVariable(players_dict[number], id)