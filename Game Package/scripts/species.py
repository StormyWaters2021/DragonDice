def get_terrain_elements(terrain_list):
    element_list = []
    for die in table: 
        if die._id in terrain_list:
            for element in TERRAIN_ELEMENTS:
                if element in die.Element and element not in element_list:
                    element_list.append(element)
    return element_list


def maneuver_as_save(die):
    result = die.Icons.split(" ")
    if result[1] == "Maneuver" or result[1] in MANEUVER["count"]:
        return int(result[0])
    else: return 0


def melee_as_maneuver(die):
    result = die.Icons.split(" ")
    if result[1] == "Melee" or result[1] in MELEE["count"]:
        return int(result[0])
    else: return 0
        
        
def save_as_melee(die):
    result = die.Icons.split(" ")
    if result[1] == "Save" or result[1] in SAVE["count"]:
        return int(result[0])
    else: return 0


def maneuver_as_melee(die):
    result = die.Icons.split(" ")
    if result[1] == "Maneuver" or result[1] in MANEUVER["count"]:
        return int(result[0])
    else: return 0
    
    
def species_check(die, location, action_word):
    species = 0
    global dwarves
    global feral
    global firewalkers
    global scalders
    
    terrain_ids = get_terrain_ids(location)
    element_list = get_terrain_elements(terrain_ids)
    
    if die.Species == "Coral Elves" and "Green (Water)" in element_list and action_word == "Save":
        species += maneuver_as_save(die)
    elif die.Species == "Dwarves":
        if "Yellow (Earth)" in element_list and action_word == "Maneuver":
            species += melee_as_maneuver(die)
        elif "Red (Fire)" in element_list and action_word == "Melee":
            bonus = save_as_melee(die)
            dwarves += bonus
    elif die.Species == "Feral" and "Blue (Air)" in element_list and "Yellow (Earth)" in element_list and action_word == "Melee":
        bonus = maneuver_as_melee(die)
        feral += bonus
    elif die.Species == "Fire Walkers" and "Red (Fire)" in element_list and action_word == "Melee":
        bonus += save_as_melee(die)
        firewalkers += bonus
    elif die.Species == "Goblins" and "Yellow (Earth)" in element_list and action_word == "Maneuver":
        species += melee_as_maneuver(die)
    elif die.Species == "Lava Elves" and "Red (Fire)" in element_list and action_word == "Save":
        species += maneuver_as_save(die)
    elif die.Species == "Scalders" and "Green (Water)" in element_list and action_word == "Save":
        bonus = maneuver_as_save(die)
        scalders += bonus
    elif die.Species == "Swamp Stalkers" and "Green (Water)" in element_list and action_word == "Save":
        species += maneuver_as_save(die)
    else: return 0
    return species