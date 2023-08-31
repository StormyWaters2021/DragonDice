def terrain_alts(die):
    # Builds a list of die faces for a terrain
    alts = [a for a in die.alternates]
    return alts


def terrain_check(cards, x=0, y=0):
    for card in cards:
        if card.Type == "Major Terrain":
            return True
        else: 
            return False


def check_terrain(die):
    # Prevents a player from accidentally rolling terrain
    if die.Type == "Major Terrain":
        confirm = askChoice("Are you sure you want to roll this Major Terrain?", ["Yes", "No"])
        if confirm == 1:
            return True
        else:
            return False
    else:
        return True
        

def terrain_up(die, x=0, y=0):
    # Turn a terrain up one face. Stops at 8 and notifies that you've captured an eighth face
    if die.Type != "Major Terrain":
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
    if die.Type != "Major Terrain":
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
    

def terrain_actions(x=0, y=0):
    terrain_list = []
    action_list = []
    action_icons = ["Melee", "Missile", "Magic"]
    
    # Find the unique ID for the terrain designated as the Frontier
    # frontier_terrain = int(getGlobalVariable("frontier_terrain")
    
    # Figure out which zone we are working in and grab the dice in that zone
    location = zone_check(x, y)
    if location == None:
        whisper("You didn't select a valid zone. Please try again.")
        return
    army = get_army(location)
    
    # Check for a Minor Terrain in that army, and append it to the list
    # for die in army:
    #    if die.Type == "Minor Terrain":
    #        terrain_list.append(die)
    
    # If we are at the Campaign Army, append the Frontier terrain
    # if location == "Campaign Army":
        # for die in table:
            # if die._id == frontier_terrain:
                # terrain_list.append(die)

    # If we are at our Home Army, figure out which terrain is Home and append it
    # if location == "Home Army":
    #    home = get_home()
    #    terrain_list.append(home)

    # Create a list of available actions from the terrains
    # for die in terrain_list:
    #   result = die.Icons.split(" ")
    #    if result[1] in action_icons:
    #        action_list.append(result[1])
    #return action_list
    
    
    # Record which terrain is the player's Home terrain 
def set_home(die):
    home = die._id
    if me.isInverted:
        var = "p2_home"
    else:
        var = "p1_home"
    setGlobalVariable(var, str(home))
    
    
    # Check which terrain was recorded as the player's Home terrain
def get_home():
    if me.isInverted:
        var = "p2_home"
    else:
        var = "p1_home"
    home = Card(int(getGlobalVariable(var)))
    return home