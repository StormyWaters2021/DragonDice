ACTION_TYPES = ("Melee", "Magic", "Missile")
MARCHING_LOCATIONS = ("Home Army", "Campaign Army", "Horde Army", "Reserves")
TERRAIN_ELEMENTS = ("Blue (Air)", "Black (Death)", "Red (Fire)", "Green (Water)", "Yellow (Earth)")

# These dictionaries set the coordinates for a player's armies and terrains

P1_COORDS = {
    "Home Terrain": (-540, -35, -540, -35),
    "Frontier Terrain": (-125, -35, -125, -35),
    "Home Army": (-735, 80, -315, 265),
    "Campaign Army": (-245, 80, 210, 265),
    "Horde Army": (270, 80, 695, 265),
    "Summoning Pool": (-245, 345, 205, 525),
    "Reserves": (270, 340, 695, 525),
    "DUA": (-735, 335, -315, 400),
    "BUA": (-735, 455, -315, 525)
}

P2_COORDS = {
    "Home Terrain": (470, -40, 470, -40),
    "Frontier Terrain": (55, -40, 55, -40),
    "Home Army": (655, -140, 255, -315),
    "Campaign Army": (165, -140, -260, -315),
    "Horde Army": (-355, -140, -745, -315),
    "Summoning Pool": (165, -410, -260, -575),
    "Reserves": (-355, -410, -745, -575),
    "DUA": (655, -405, 265, -450),
    "BUA": (655, -525, 265, -575)
}

# These dictionaries are used to calculate roll results, based on the action taken
# Count = Counts as normal results, included in normal calculation
# Extra = Functions during the roll, but has some non-standard effect, not counted in normal calculation
# Reroll = Generates normal results, then rolls again, keeps a running total and adds to normal calculation
# No Save = Generates results where no save is allowed, not counted in normal calculation
# Normal = Generates normal results

MELEE = {
"count": ["Counter", "Sneak Attack", "Sortie", "Trample" ], 
"extra": ["Breath", "Cantrip", "Charge", "Charm", "Choke", "Cloak", "Coil", "Confuse", "Convert", "Decapitate", "Double Strike", "Entangle", "Firebreath", "Firecloud", "Flame", "Frost Breath", "Galeforce", "Gore", "Howl", "Hug", "Hypnotic Glare", "Illusion", "Kick", "Magic Suppression", "Net", "Plague", "Poison", "Roar", "Scare", "Screech", "Slay", "Sleep", "Smother", "Spell Disruption", "Stomp", "Stun", "Surprise", "Swallow", "Trumpet", "Wave", "Web", "Wither", ],
"reroll": ["Flurry", "Rend", "Tail"],
"nosave": ["Smite", "Sneak Attack", "Stone", ],
"normal": ["Melee"],
}

MISSILE = {
"count": ["Volley", ], 
"extra": ["Bullseye", "Cantrip", "Confuse", "Crush", "Elevate", "Firecloud", "Flaming Arrow", "Frost Breath", "Galeforce", "Howl", "Illusion", "Impale", "Magic Suppression", "Net", "Seize", "Spell Disruption", "Web", ], 
"reroll": [],
"nosave": ["Stone", ],
"normal": ["Missile"],
}

MAGIC = {
"count": ["Cantrip", "Cloak", "Magic Suppression", "Spell Disruption", ], 
"extra": ["Attune", "Fabricate", "Galeforce", "Illusion", "Sneak Attack", "Summon Dragon", ], 
"reroll": [],
"nosave": [],
"normal": ["Magic"],
}

MANEUVER = {
"count": ["Elevate", "Firewalking", "Fly", "Hoof", "Rend", "Teleport", "Trample"], 
"extra": ["Wave", "Wayfare", ], 
"reroll": [],
"nosave": [],
"normal": ["Maneuver"],
}

SAVE = {
"count": ["Cloak", "Counter", "Fabricate", "Fly", "Hoof", "Kick", "Rise from the Ashes", "Sortie", ], 
"extra": ["Bash", "Cantrip", "Counter", "Elevate", "Flurry", "Trumpet", "Vanish", "Volley", ], 
"reroll": [],
"nosave": [],
"normal": ["Save"],
}

ANY_ROLL = {
"count": ["Create Fireminions", ], 
"extra": ["Dispel Magic", ], 
"reroll": [],
"nosave": [],
"normal": [],
}

NON_MANEUVER = {
"count": [], 
"extra": ["Element Fire", "Element Water", "Element Earth", "Element Death", "Element Air", "Ferry", "Firewalking", "Gate", "Regenerate", "Teleport", "Wild Growth", ], 
"reroll": [],
"nosave": [],
"normal": [],
}

ARMIES = ("Home Army", "Campaign Army", "Horde Army", "Summoning Pool")


# Used to calculate the points values of armies during setup
UNIT_POINTS = {"Small": 1, "Medium": 2, "Large": 3, "Champion": 4, "Monster": 4}

ITEM_POINTS = {"Small": 1, "Medium": 2, "Large": 2, "Artifact": 3, "Relic": 4, "Medallion": 4}


# These dictionaries are used to build the spell cards in a player's hand, 
# based on the colors and species in that player's armies
# These are GUIDs for the various spell cards

# Basic spells of each color and alloy

SPELL_COLORS = {
    "Blue (Air)": ["7103f936-648d-49bc-b7af-ed7603cc9d1d", "7105f0e4-04a7-4651-a078-76112076f640",
                   "7814a178-e20d-445c-b991-0030abf638c2"],
    "Black (Death)": ["6fea1edd-cabd-4067-8e4e-5b7e281d5b80", "716eda65-2347-48ab-b159-8fd9f97079f6",
                      "7332e82e-b84b-4982-bb9e-b2be5899ebf4"],
    "Red (Fire)": ["6e7c26fb-a333-4aff-9010-b6cca2fc601b", "6efa7f95-88a9-4b6f-824a-904dc71b8403",
                   "6f297ec7-bcf0-4069-88ba-67d71596fdcf"],
    "Green (Water)": ["70132c49-2d04-43b1-a624-78127ac6756e", "767a855c-f4ad-4341-ac3d-b0b9c274c59b",
                      "780ee710-0330-4359-8b56-dc8b9324ad40"],
    "Yellow (Earth)": ["727a5cb8-0bf9-4290-9fe8-3a27e12d2ceb", "73935453-427b-4d45-adcf-81c111d5ceeb",
                       "7644008a-246e-443c-b1bf-310f3110c3fd"],
    "Ivory": [],
    "Gold": ["ae08c614-1727-494d-8816-0a41fe9d2733"],
    "Silver": ["ac701497-d0b8-49fe-adcd-b2ef8cc2869d"],
    "Bronze": ["ac33c82e-a837-4536-aa17-6721c597e38d"],
    "Alloy": ["aa13d920-5e64-425f-979a-957f38b4fa0b", "aa85ad40-40c2-40a5-89fd-512837528e8e", "aaaf3e5c-93aa-4ce4-bf8b-45e8d21d595f",
                "abf3f87f-d7b9-4417-85bb-b85940c6325f", "ac06e3d6-2d47-4f4b-8815-57c1e9239350"],
}

# Species-specific spell lists

SPELL_SPECIES = {
    "Amazons": ["78d96ad4-e8b6-4a79-a35c-4cec60a6ae40", "79472428-83f9-4a52-8468-92d0ddf587bc"],
    "Coral Elves": ["79e0339f-8a38-4a9e-9e4e-ab531440c793", "7bde1176-91d8-4df9-a31a-c6f53d3cd239"],
    "Dwarves": ["7c855b72-fdf6-4607-ac5c-44dc1f46b44e", "7cd9b2fd-9db0-4cf8-ab78-94680e90316c"],
    "Eldarim": ["7cfb0aa5-b373-4b4d-bf8a-cca3c314be30", "7de49c8e-5e97-4d9e-a004-768fbc2644f2"],
    "Feral": ["7e3da2a3-de0c-4b8f-9b54-24b6b135f0d9", "7df0087a-24cd-46b7-b6bb-8347ca96daa3"],
    "Fire Walkers": ["7f032006-b28b-44ca-a293-f6e3054edd88", "7ea9e42b-d7dd-4923-a707-1aef71e7a8bd"],
    "Frostwings": ["811bff1b-2f33-4b82-b1e7-1def8aa934c5", "80a56f35-a877-4eb0-aa52-7046298dc20d"],
    "Goblins": ["81671736-6d39-4ac6-bb8f-f25cf5dbba2d", "822d81b3-8081-4339-9d3f-d10bfcdde365"],
    "Lava Elves": ["8269cb14-79ba-49f3-a14e-527ae3008c2a", "8264b14e-9d59-479d-b06a-ff9601f16cca"],
    "Scalders": ["85321e0f-48e5-4e19-8cff-64c7e7e39113", "84bd1c11-6f81-4c9d-86e5-a12e801eb939"],
    "Swamp Stalkers": ["862e6079-dfe1-46b5-b46a-ad86cf219aa9", "8560075f-eb30-4eac-8411-ac409cf18349"],
    "Treefolk": ["863f1e12-5082-4e00-899f-76a5e7efddb9", "867c09c2-dd0d-47a8-9769-cae6dc5ceb64"],
    "Undead": ["8815faee-02a0-4ed8-82ec-9cf98283ce9a", "8846249e-b19a-4dc9-9af2-3eed6ced44b0",
               "89992b23-a05d-4f56-a010-80b4c240c5d1", "8b062da1-eacc-43cf-b3be-39bb8084875e"],
    "Dracolem": [],
}

# Elemental spells
SPELL_BASICS = ["72b770b9-f756-4d21-b8c0-1b9bfbd14943", "7440cf69-ab96-45b1-81e9-bcd43d58af0e",
                "74665192-ec8d-4282-a9d0-e98aa224b7ae", "747afeec-7431-4f17-9253-6493ba9e77b5"]
