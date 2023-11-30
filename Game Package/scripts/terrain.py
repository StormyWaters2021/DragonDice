def terrain_alts(die):
    # Builds a list of die faces for a terrain
    alts = [a for a in die.alternates]
    return alts


def terrain_check(cards, x=0, y=0):
    for card in cards:
        if card.Type == "Major Terrain" or card.Type == "Minor Terrain":
            return True
        else: 
            return False


def check_terrain(die):
    # Prevents a player from accidentally rolling terrain
    if die.Type == "Major Terrain" or die.Type == "Minor Terrain":
        confirm = askChoice("Are you sure you want to roll this terrain?", ["Yes", "No"])
        if confirm == 1:
            return True
        else:
            return False
    else:
        return True
        

def terrain_up(die, x=0, y=0):
    # Turn a terrain up one face. Stops at 8 and notifies that you've captured an eighth face
    check = [die]
    if not terrain_check(check):
        return
    alts = terrain_alts(die)
    current_face = die.alternate
    current_index = alts.index(current_face)
    if current_index == 0:
        notify("{} is already on its eighth face.".format(die.Name))
    elif current_index == 7:
        die.alternate = die.alternates[0]
        notify("{} captures an eighth face!".format(me))
    else:
        current_index += 1
        die.alternate = die.alternates[current_index]
        notify("{} advances {} to {}.".format(me, die.Name, die.Icons))


def terrain_down(die, x=0, y=0):
    # Turn a terrain down one face. Stops at 1 and notifies that you're already at the first face
    check = [die]
    if not terrain_check(check):
        return
    alts = terrain_alts(die)
    current_face = die.alternate
    current_index = alts.index(current_face)
    if current_index == 1:
        notify("{} is already on its first face.".format(die.Name))
    else:
        current_index -= 1
        die.alternate = die.alternates[current_index]
        notify("{} lowers {} to {}.".format(me, die.Name, die.Icons))


def terrain_randomizer(die, x=0, y=0):
    # Automatically sets initial terrain condition. Rolls the die, then rerolls 7s and turns 6s down to 5.
    alts = terrain_alts(die)
    if die.Type != "Major Terrain":
        return
    else:
        while alts.index(die.alternate) == 7:
            roll_dice(die)
    if alts.index(die.altnerate) == 6:
        die.alternate = die.alternates[5]
    notify("{} has randomized {} to {}.".format(me, die.Name, die.Icons))
    
