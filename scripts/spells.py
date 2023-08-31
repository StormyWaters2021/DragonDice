def build_species():
    # Builds a list of the species in a player's army, for setting up spell cards
    mute()
    global my_species
    for die in table:
        if die.controller == me and die.Type == "Unit" and die.Species not in my_species and die.Species != "Dragonkin":
            my_species.append(die.Species)


def build_colors():
    # Builds a list of colors in a player's army, for setting up spell cards
    mute()
    global my_colors
    for die in table:
        if die.controller == me:
            if die.Type == "Unit" or die.Type == "Terrain":
                colors = die.Element.split(", ")
                color1 = colors[0]
                if color1 not in my_colors:
                    my_colors.append(color1)
                if len(colors) == 2:
                    color2 = colors[1]
                    if color2 not in my_colors:
                        my_colors.append(color2)


def build_spells():
    # Checks lists of colors and species and places appropriate spell cards in the player's hand
    mute()
    global my_colors
    global my_species
    my_spells = []
    for num in range(0, len(SPELL_BASICS)):
        my_spells.append(SPELL_BASICS[num])
    for c in my_colors:
        my_spells.extend(SPELL_COLORS[c])
    for s in my_species:
        my_spells.extend(SPELL_SPECIES[s])
    for spell in my_spells:
        me.hand.create(spell)


def is_spell(cards, x=0, y=0):
    # Used by the game to display or hide options related to spell cards.
    # If the player clicks on a spell card, the options to duplicate or remove
    # them are shown, but these options are hidden if the player clicks on any
    # other objects.
    for card in cards:
        if card.set == "Spell Cards":
            return True
        else: 
            return False
 
 
def duplicate_spell(card, x=0, y=0):
    # Creates an additional copy of a spell card on the table. 
    # These duplicate spell cards disappear if moved from the table (to prevent clutter)
    mute()
    id = card.model
    x = card.position[0]
    y = card.position[1]
    if me.isInverted:
        table.create(id, x-33, y)
    else:
        table.create(id, x+33, y)
   
   
def remove_spell(card, x=0, y=0):
    # Moves the spell card back to the player's hand (destroying duplicates)
    mute()
    card.moveTo(me.Hand)
    notify("{} ends the effects of {}.".format(me, card))
    