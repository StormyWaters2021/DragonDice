# OCTGN only allows random number generation via network calls, so we use a function
# to generate 1000 numbers at a time with a single network call to improve speed. 
# roll_bank is a dictionary of lists, with the keys being the number of "sides" a die has
# roll_count just determines the last number in the random list that was used, and 
# then generates a new list when it reaches the end.

# scatter_bank and scatter_count are similar, but for determining a random distance
# on the x and y axis to move dice when they are rolled if dice scattering is enabled.

roll_bank = {}
roll_count = 0
scatter_bank = []
scatter_count = 0

def update_bank(dice, x=0, y=0):
# Updates the roll bank account for new die sizes and to refresh lists when
# the player has used all the previously-generated numbers.
    global roll_bank
    global roll_count
    for d in dice:
    # Check how many sides the die has
        num_sides = len(d.alternates)
    # If that die size does not have a bank, create one
        if num_sides not in roll_bank.keys():
            new_list = rndArray(0, num_sides - 1, 1000)
            roll_bank[num_sides] = new_list
    
    # If we are approaching the end of the list, create a new list and reset the counter
        if len(dice) > 1000 - roll_count - 1:
            roll_count = 0
            new_list = rndArray(0, num_sides - 1, 1000)
            roll_bank[num_sides] = new_list


def roll_dice(dice, x=0, y=0):
    # Takes a list of dice and rolls each one
    mute()
    # Make sure the bank of rolled numbers is ready
    update_bank(dice)
    global roll_bank
    global roll_count
    for die in dice:
        if check_terrain(die):
        # Checks to see if the die is a terrain, and confirms that the player wants to roll it
        # to prevent players from accidentally rolling terrain if they didn't mean to.
            num_sides = len(die.alternates)
            new_face = roll_bank[num_sides][roll_count]
            die.alternate = die.alternates[new_face]
            roll_count +=1
            scatter(die)


def set_scatter_list():
    # Build a global list of 1000 numbers, used for scattering dice random distances
    global scatter_bank
    scatter_bank = rndArray(-50, 50, 1000)


def scatter(die):
    # Check to see if the players have dice scattering enabled (disabled by default)
    if int(getGlobalVariable("scatter_on")) == 0:
        return
    global scatter_count
    global scatter_bank
    # Check if the scatter counter is about to hit the end of the list and reset if necessary
    if scatter_count > 997:
        scatter_count = 0
    
    # Pull the next two numbers from the scatter list to offset the dice
    x_shift = scatter_bank[scatter_count]
    y_shift = scatter_bank[scatter_count+1]
    # Pull the current x and y coordinates for the die
    x, y = die.position
    die.moveToTable(x + x_shift, y + y_shift)
    scatter_count += 2


def reset_die(die, x=0, y=0):
    # Turns the die to its primary (ID) face
    die.alternate = ""
 
 
def scatter_off(*args):
    # Turns off dice scattering
    setGlobalVariable("scatter_on", "0")
    notify("{} turned off dice scattering.".format(me))
   
   
def scatter_on(*args):
    # Turns on die scattering
    setGlobalVariable("scatter_on", "1")
    notify("{} turned on dice scattering.".format(me))
    
    
def sort_army(dice):
    # Builds a list of all the dice in a selected pool, organized by size. 
    # Used by other functions to rearrange armies to keep a clean display
    sorted_army = []
    dragons = [d for d in dice if "Dragon" in d.Type]
    monsters = [d for d in dice if d.Size == "Monster"]
    champions = [d for d in dice if d.Size == "Champion" and d.Type == "Unit"]
    large_units = [d for d in dice if d.Size == "Large" and d.Type == "Unit"]  
    medium_units = [d for d in dice if d.Size == "Medium" and d.Type == "Unit"]
    small_units = [d for d in dice if d.Size == "Small" and d.Type == "Unit"]
    artifacts = [d for d in dice if d.Size == "Artifact"]
    large_items = [d for d in dice if d.Size == "Large" and d.Type == "Item"]
    medium_items = [d for d in dice if d.Size == "Medium" and d.Type == "Item"]
    small_items = [d for d in dice if d.Size == "Small" and d.Type == "Item"]
    relics = [d for d in dice if d.Size == "Relic"]
    minor_terrain = [d for d in dice if d.Type == "Minor Terrain"]
    medallions = [d for d in dice if d.Size == "Medallion"]
    sorted_army += dragons + monsters + champions + large_units + medium_units + small_units + artifacts + relics + medallions + large_items + medium_items + small_items + minor_terrain
    return sorted_army
    
 
def rearrange_army(location):
    # Rearranges an army, then sets all the dice to their ID
    army = get_army(location)
    army = sort_army(army)
    build_army(location)
    return army
    
def reset_army(location):
    army = rearrange_army(location)
    for die in army:
        reset_die(die)


def invert_check():
    # Determines which "side" of the table a player is on, and passes
    # the correct dictionary of table coordinates for armies, terrains, etc. 
    if me.isInverted:
        return P2_COORDS
    else:
        return P1_COORDS


def roll_army(location):
    # Selects all dice in a designated area of the table and passes
    # that list to the dice rolling function
    base_army = get_army(location)
    army = [d for d in base_army if d.set != "Terrain"]
    roll_dice(army)


def move_to_army(location, die):
    # Sends selected dice to a chosen location, then resets that location
    # to organize by size and turn all dice to IDs. 
    if die.Type == "Major Terrain": return
    coords = invert_check()
    x = coords[location][0]
    y = coords[location][1]
    die.moveToTable(x, y)
    rearrange_army(location)


def get_army(location):
    # Checks the passed location for all dice, and returns a list of dice objects in that zone
    
    army = []
    if me.isInverted:
        coords = P2_COORDS
        for c in table:
            if c.controller == me:
                if c.position[0] <= coords[location][0] + 75 and c.position[0] >= coords[location][2]:
                    if c.position[1] <= coords[location][1] + 75 and c.position[1] >= coords[location][3]:
                        if c.set != "Spell Cards":
                            army.append(c)
    else:
        coords = P1_COORDS
        for c in table:
            if c.controller == me:
                if c.position[0] >= coords[location][0] and c.position[0] <= coords[location][2]:
                    if c.position[1] >= coords[location][1] and c.position[1] <= coords[location][3]:
                        if c.set != "Spell Cards":
                            army.append(c)
    return army


def build_army(loc):
    # Takes all the dice in a "zone" and rearranges all the dice to organized rows.
    
    # Grab all the dice in the zone as a list
    full_army = get_army(loc)
    
    # Sort that list by size
    sorted = sort_army(full_army)
    
    # Determine which coordinate dictionary to use
    coords = invert_check()
    
    # Determine which direction (left or right) to place dice (since one player is inverted)
    if me.isInverted:
        offset = -1
    else:
        offset = 1

    # Get the first die's starting position from the coordinate dictionary
    x = coords[loc][0]
    y = coords[loc][1]
    die_shift = 0
    die_count = 0
    
    # Iterate through the sorted die list, placing each die offset slightly from the last,
    # starting a new row when the edge of the "zone" is reached
    for _ in range(0, len(sorted)):
        if len(sorted) > 0:
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
                    

def results_splitter(die):
    result = die.Icons.split(" ", 1)
    return result
  
  
def calculate_army(location, action, action_word):
# Complex result calculation. Will total up relevant normal icons,
# as well as icons that deal damage without allowing a save,
# as well as all other icons that may apply to the chosen action.

# counters to keep track of situational species bonuses
    global dwarves; dwarves = 0
    global feral; feral = 0
    global firewalkers; firewalkers = 0
    global scalders; scalders = 0
    
    start_army = get_army(location)
    army = [d for d in start_army if d.set != "Terrain"]
    normal = 0
    nosave = 0
    ids = 0
    sai = 0
    species = 0
    autosave = 0
    all_results = []
    other_sai = []
    other_counts = []
    spell_list = []
    report = ""
    nosave_report = ""
    autosavereport = ""

    # First check for icons that roll and reroll. Keep rolling them 
    # and totaling results until you get a non-reroll icon.
    # This step does *not* calculate any non-SAI results
    for die in army:
        sai += roll_and_reroll(die, action, 0)

    # Then build a list of all the roll results left
    for die in army:
        result = results_splitter(die)
        all_results.append(result)

    for item in all_results:

        # Total all normal, non-ID, non-SAI results
        if item[1] in action["normal"]:
            normal += int(item[0])
        
        # Total all icons from SAIs that count as normal results
        if item[1] in action["count"] or item[1] in ANY_ROLL["count"]:
            sai += int(item[0])
            
        # Add IDs, but also record them separately for effects that care about non-ID results. 
        elif item[1] == "ID":
            ids += int(item[0])

        # Total all icons that generate a result that doesn't allow for a save
        # such as Smite or Stone
        elif item[1] in action["nosave"]:
            nosave += int(item[0])

        # Build a list of icons that were not already used but are relevant to this type of roll
        elif item[1] in action["extra"] or item[1] in ANY_ROLL["extra"]:
            
            # If it's not already in the list, add it, and add the numerical value to a second list.
            if item[1] not in other_sai:
                other_sai.append(item[1])
                other_counts.append(int(item[0]))
                
            # If it's already in the list, find its position, then use that position
            # and increment the appropriate value in the matched list (so multiple 
            # instances of one SAI are added together instead of being listed twice
            else:
                index = other_sai.index(item[1])
                other_counts[index] += int(item[0])
        
        # Check to see if this is a non-maneuver roll, and if so, iterate through
        # the non-maneuver SAIs to find any results that were rolled
        elif action_word != "Maneuver" and item[1] in NON_MANEUVER["extra"]:
            if item[1] not in other_sai:
                other_sai.append(item[1])
                other_counts.append(int(item[0]))
            else:
                index = other_sai.index(item[1])
                other_counts[index] += int(item[0])
    
    for die in army:
        if die.Type == "Unit" or die.Type == "Monster" or die.Type == "Champion":
            species += species_check(die, location, action_word)
    
    if action_word == "Save":
        autosave = autosave_check(army)
        normal += autosave
        autosavereport = str(autosave) + " autosaves, "
    
    # Don't bother reporting zero "no-save" results
    if nosave > 0:
        nosave_report = str(nosave) + " damage that can't be saved.\n"

    # Create a report of all the results that weren't already totaled
    if len(other_sai) > 0:
        report = "The following SAIs were not included in the calculation:\n"
    for num in range(0, len(other_sai)):
        report += str(other_counts[num]) + " " + other_sai[num] + "\n"
    
    if dwarves > 0:
        report += "Add an additional " + str(dwarves) + " results if this is a counter-attack, from the Dwarves species ability. "
    if feral > 0:
        report += "Add an additional " + str(feral) + " results if this is a counter-attack, from the Feral species ability. "
    if firewalkers > 0:
        report += "Add an additional " + str(firewalkers) + " results if this is not a counter-attack, from the Fire Walkers species ability. "
    if scalders > 0:
        report += "Add an additional " + str(scalders) + " results if this is a save roll vs missiles, from the Scalders species ability. "
    
    # Build list of magic results by color
    if action_word == "Magic":
        magic_results = "\nMagic results break down to a maximum of:\n"
        calculate_magic(army)
        global ivory
        global black
        global blue
        global green
        global red
        global yellow
        global bronze
        global silver
        global gold
        if ivory != 0:
            magic_results = magic_results + str(ivory) + " ivory magic\n"
        if black != 0:
            magic_results = magic_results + str(black) + " black magic\n"
        if blue != 0:
            magic_results = magic_results + str(blue) + " blue magic\n"
        if green != 0:
            magic_results = magic_results + str(green) + " green magic\n"
        if red != 0:
            magic_results = magic_results + str(red) + " red magic\n"
        if yellow != 0:
            magic_results = magic_results + str(yellow) + " yellow magic\n"
        if bronze != 0:
            magic_results = magic_results + str(bronze) + " bronze magic\n"
        if silver != 0:
            magic_results = magic_results + str(silver) + " silver magic\n"
        if gold != 0:
            magic_results = magic_results + str(gold) + " gold magic\n"
        report += magic_results
    
    # Build a dict of each of these results for later use
    final = me.name + " performed a " + action_word + " roll with their " + location + ": \n" + str(normal + ids + sai + species) + " normal results (including " + str(ids) + " ID results, " + str(sai) + " normal results from SAIs, " + autosavereport + "and " + str(species) + " results from species abilities).\n" + nosave_report + report + "This calculation does NOT account for any eighth-face doubling. "
    results_dict = {"normal": normal, "ids": ids, "sai": sai, "species": species, "final": final}
    
    # Finally, report these totals to the chat window. 
    # notify("{} performed a {} roll with their {}: \n{} normal results (including {} ID results, {} normal results from SAIs, and {} results from species abilities).\n{}{}".format(me, action_word, location, normal + ids + sai + species, ids, sai, species, nosave_report, report))
    
    return results_dict


def calculate_magic(army):
    global ivory; ivory = 0
    global black; black = 0
    global blue; blue = 0
    global green; green = 0
    global red; red = 0
    global yellow; yellow = 0
    global bronze; bronze = 0
    global silver; silver = 0
    global gold; gold = 0
    for die in army:
        result = die.Icons.split(" ")
        if result[1] == "Magic" or result[1] in MAGIC["count"] or result[1] in ANY_ROLL["count"]:
            if "ivory" in die.Element.lower():
                ivory += int(result[0])
            if "black" in die.Element.lower():
                black += int(result[0])
            if "blue" in die.Element.lower():
                blue += int(result[0])
            if "green" in die.Element.lower():
                green += int(result[0])
            if "red" in die.Element.lower():
                red += int(result[0])
            if "yellow" in die.Element.lower():
                yellow += int(result[0])
            if "bronze" in die.Element.lower():
                bronze += int(result[0])
            if "silver" in die.Element.lower():
                silver += int(result[0])
            if "gold" in die.Element.lower():
                gold += int(result[0])
            
    return
                

def roll_and_reroll(die, action, number):
    # Checks for icons (like Rend) that add results, and then reroll and apply new results as well
    keep_rolling = True
    while keep_rolling:
        dice = []
        dice.append(die)
        result = results_splitter(die)
        if result[1] in action["reroll"]:
            notify("{} rolled {}! Re-rolling...".format(die, die.Icons))
            number += int(result[0])
            roll_dice(dice)
        else:
            keep_rolling = False
    return number


def autosave_check(army):
    autosave = 0
    itemvalue = 0
    dracolemvalue = 0
    for die in army:
        if die.Species == "Dragonkin" and "Belly" not in die.Icons:
            autosave += int(die.Autosaves)
    # for die in army:
        # if die.Type == "Item":
            # itemvalue += ITEM_POINTS[die.Size]
    # for die in army:
        # if die.Species == "Dracolem":
            # dracolemvalue += UNIT_POINTS[die.Size]
    # if itemvalue > dracolemvalue: autosave += dracolemvalue
    # elif dracolemvalue > itemvalue: autosave += itemvalue
    return autosave



def zone_check(x, y):
    # Determines which zone a player has clicked in, to automatically select the right area to roll/reset
    # Returns the name of the army, eg: "Home Army", "Campaign Army", etc.
    coords = invert_check()
    if me.isInverted:
        for location in coords:
            if x < coords[location][0] and x > coords[location][2] and y < coords[location][1] and y > coords[location][3]:
                return location
    else:
        for location in coords:
            if x > coords[location][0] and x < coords[location][2] and y > coords[location][1] and y < coords[location][3]:
                return location



def build_frontier_list():
    # Gather a list of all the IDs stored in the global variables
    # and return the list. These are stored as strings, so they
    # need to be converted to integers first
    frontier_1 = getGlobalVariable("p1_frontier")
    frontier_2 = getGlobalVariable("p2_frontier")
    frontier_3 = getGlobalVariable("p3_frontier")
    frontier_4 = getGlobalVariable("p4_frontier")
    frontier_list = [int(frontier_1), int(frontier_2), int(frontier_3), int(frontier_4)]
    return frontier_list


def get_terrain_ids(location):
    terrain_list = []
    army = get_army(location)
    
    # Grab all minor terrains that are in the army and add their IDs to a list
    for die in army:
        if die.Type == "Minor Terrain":
            terrain_list.append(die._id)
    
    # Check which location is used, and append the relevant terrain ID to the list
    if location == "Home Army":
        if me.isInverted:
            terrain_list.append(int(getGlobalVariable("p2_home")))
        else:
            terrain_list.append(int(getGlobalVariable("p1_home")))
    elif location == "Campaign Army":
        frontier_list = build_frontier_list()
        for i in frontier_list:
            terrain_list.append(i)
    elif location == "Horde Army":
        if me.isInverted:
            terrain_list.append(int(getGlobalVariable("p1_home")))
        else:
            terrain_list.append(int(getGlobalVariable("p2_home")))
    return terrain_list


def two_player_terrain_check(location):
    # Check terrains at location to determine which actions are available
    action_list = []
    terrain_list = get_terrain_ids(location)
    army = get_army(location)
    
    # If the army is in reserves, bypass this part and just append "Magic" to the actions list    
    if location == "Reserves":
        action_list.append("Magic")
    elif location not in MARCHING_LOCATIONS:
        return
    
    # Using the list of IDs, check the table for all dice with those IDs
    # and append either the action icon shown, or append all three actions
    # if the terrain is on the eighth face
    for die in table:
        if die._id in terrain_list:
            if die.alternate != "":
                for action in ACTION_TYPES:
                    if action in die.Icons:
                        action_list.append(action)
            else:
                action_list = ["Melee", "Missile", "Magic"]
    return action_list
    
def add_die_to_table(filter, type, x=0, y=0):
    choice = {filter:type}
    card, qty = askCard(choice, title="Choose a die to create")
    table.create(card, x, y, quantity = qty, persist = True)


def delete_card(card, x=0, y=0):
    if card.set == "Spell Cards":
        remove_spell(card)
    elif card.type in ['Item', 'Artifact', 'Medallion', 'Relic', 'Minor Terrain']:
        move_to_army('BUA', card)
    elif card.set in ['Dragons', 'Dragonkin']:
        move_to_army('Summoning Pool', card)
    elif card.type == 'Unit':
        move_to_army('DUA', card)
    else: return