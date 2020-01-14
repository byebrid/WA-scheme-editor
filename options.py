"""
options.py by Byebrid
---------------------
For info on which options we can change for each scheme.

See https://worms2d.info/Game_scheme_file for more info.
"""
from collections import OrderedDict

OPTIONS = OrderedDict({
    'Signature': {
        'Type': None, # To signify user has no control over this
        'Default': b'SCHM'
    },
    'Super Weapons': { #Actually represents version but equivalent to allowing super weapons
        'Type': 'str',
        'Default': 'False',
        'Conversions': {
            'False': b'\x01',
            'True':  b'\x02'
        },
        'Images': {
            'False': ('Custom', 'superwepno.bmp'),
            'True':  ('Custom', 'superwepyes.bmp')
        },
        'Grid Args': {
            'row': 2,
            'column': 3
        }
    },
    'Hot-Seat Delay': {
        'Type': 'ubyte',
        'Default': 5,
        'Image': ('gameoptions', 'HotseatDelay', '000002.bmp'),
        'Grid Args': {
            'row': 3,
            'column': 0
        },
        'Popup Text': '0-255 seconds.'
    },
    'Retreat Time': {
        'Type': 'byte',
        'Default': 3,
        'Image': ('gameoptions', 'RetreatTime', '000002.bmp'),
        'Grid Args': {
            'row': 2,
            'column': 0
        },
        'Popup Text': '0-255 seconds.'
    },
    'Rope Retreat Time': {
        'Type': 'byte',
        'Default': 5,
        'Image': ('gameoptions', 'RopeRetreat', '000003.bmp'),
        'Grid Args': {
            'row': 2,
            'column': 1
        },
        'Popup Text': '0-255 seconds.'
    },
    'Display Total Round Time': {
        'Type': 'bool',
        'Default': True,
        'Images': {
            False: ('gameoptions', 'RoundTimeOFF.bmp'),
            True:  ('gameoptions', 'RoundTimeON.bmp')
        },
        'Grid Args': {
            'row': 3,
            'column': 1
        }
    },
    'Automatic Replays': {
        'Type': 'bool',
        'Default': True,
        'Images': {
            False: ('gameoptions', 'replayOFF.bmp'),
            True:  ('gameoptions', 'replayON.bmp')
        },
        'Grid Args': {
            'row': 4,
            'column': 0
        }
    },
    'Fall Damage': {
        'Type': 'byte',
        'Default': 1,
        'Image': ('Custom', 'worm_falling.jpg'),
        'Grid Args': {
            'row': 2,
            'column': 2
        },
        'Popup Text': 'See https://worms2d.info/Fall_Damage'
    },
    'Anchored': {
        'Type': 'bool',
        'Default': False,
        'Images': {
            False: ('gameoptions', 'artilleryOFF.bmp'),
            True:  ('gameoptions', 'artilleryON.bmp')
        },
        'Grid Args': {
            'row': 0,
            'column': 4
        }
    },
    'Bounty Mode': {
        'Type': None, # To signify user has no control over this
        'Default': b'\x17'
    },
    'Stockpiling Mode': {
        'Type': 'str',
        'Default': 'Replenishing',
        'Conversions': {
            'Replenishing': b'\x00',
            'Accumulating': b'\x01',
            'Reducing':     b'\x02'
        },
        'Images': {
            'Replenishing': ('gameoptions', 'Stockpiling', '000001.bmp'),
            'Accumulating': ('gameoptions', 'Stockpiling', '000002.bmp'),
            'Reducing':     ('gameoptions', 'Stockpiling', '000003.bmp')
        },
        'Grid Args': {
            'row': 0,
            'column': 5
        }
    },
    'Worm Select': {
        'Type': 'str',
        'Default': 'Ordered',
        'Conversions': {
            'Ordered':  b'\x00',
            'Optional': b'\x01',
            'Random':   b'\x02'
        },
        'Images': {
            'Ordered':  ('gameoptions', 'WormSelectOFF.bmp'),
            'Optional': ('gameoptions', 'WormSelectON.bmp'),
            'Random':   ('gameoptions', 'WormSelectRANDOM.bmp')
        },
        'Grid Args': {
            'row': 0,
            'column': 2
        }
    },
    'Sudden Death Event': {
        'Type': 'str',
        'Default': 'HP drops to 1',
        'Conversions': {
            'Round Ends':       b'\x00',
            'Nuclear Strike':   b'\x01',
            'HP drops to 1':    b'\x02',
            'Nothing happens?': b'\x03'
        },
        'Images': {
            'Round Ends':       ('gameoptions', 'SuddenDeathModes', '00001.bmp'),
            'Nuclear Strike':   ('gameoptions', 'SuddenDeathModes', '00002.bmp'),
            'HP drops to 1':    ('gameoptions', 'SuddenDeathModes', '00003.bmp'),
            'Nothing happens?': ('gameoptions', 'SuddenDeathModes', '00004.bmp')
        },
        'Grid Args': {
            'row': 3,
            'column': 5
        }
    },
    'Water Rise Rate': {
        'Type': 'sbyte',
        'Default': 1,
        'Image': ('gameoptions', 'WaterRiseSpeed', '000002.bmp'),
        'Grid Args': {
            'row': 1,
            'column': 6
        },
        'Popup Text': 'Very complicated. see https://worms2d.info/Sudden_Death'
    },
    'Weapon Crate Probability': {
        'Type': 'sbyte',
        'Default': 40,
        'Image': ('Custom', 'weapondrops.bmp'),
        'Grid Args': {
            'row': 1,
            'column': 2
        },
        'Popup Text': "Percentage chance depends on proportions of each crate type's probabilities. See https://worms2d.info/Crate_probability."
    },
    'Donor Cards': {
        'Type': 'bool',
        'Default': False,
        'Images': {
            False: ('gameoptions', 'DonorOFF.bmp'),
            True:  ('gameoptions', 'DonorON.bmp')
        },
        'Grid Args': {
            'row': 0,
            'column': 6
        }
    },
    'Health Crate Probability': {
        'Type': 'sbyte',
        'Default': 40,
        'Image': ('Custom', 'healthdrops.bmp'),
        'Grid Args': {
            'row': 1,
            'column': 3
        },
        'Popup Text': "Percentage chance depends on proportions of each crate type's probabilities. See https://worms2d.info/Crate_probability.",
    },
    'Health Crate Energy': {
        'Type': 'ubyte',
        'Default': 25,
        'Image': ('gameoptions', 'HealthCrate', '000002.bmp'),
        'Grid Args': {
            'row': 1,
            'column': 5
        },
        'Popup Text': 'From 0-255'
    },
    'Utility Crate Probability': {
        'Type': 'sbyte',
        'Default': 20,
        'Image': ('Custom', 'utilitydrops.bmp'),
        'Grid Args': {
            'row': 1,
            'column': 4
        },
        'Popup Text': "Percentage chance depends on proportions of each crate type's probabilities. See https://worms2d.info/Crate_probability.",
    },
    'Hazardous Object Types': {
        'Type': 'byte',
        'Default': 5,
        'Image': ('gameoptions', 'Objects', '000004.bmp'),
        'Grid Args': {
            'row': 3,
            'column': 2
        },
        'Popup Text': 'Very complicated. see https://worms2d.info/Hazardous_Objects#How_is_this_setting_saved_in_a_WSC_file.3F'
    },
    'Mine Delay': {
        'Type': 'byte',
        'Default': 3,
        'Image': ('gameoptions', 'MineFuse.tga', '000004.bmp'),
        'Grid Args': {
            'row': 3,
            'column': 3
        },
        'Popup Text': '4,128-255 will be random (between 0-3 seconds); 0-3,5-127 represent seconds.'
    },
    'Dud Mines': {
        'Type': 'bool',
        'Default': True,
        'Images': {
            False: ('gameoptions', 'DudmineOFF.bmp'),
            True:  ('gameoptions', 'DudmineON.bmp')
        },
        'Grid Args': {
            'row': 3,
            'column': 4
        }
    },
    'Worm Placement': {
        'Type': 'str',
        'Default': 'Automatic',
        'Conversions': {
            'Automatic': b'\x00',
            'Manual':    b'\x01'
        },
        'Images': {
            'Automatic': ('gameoptions', 'TeleportinOFF.bmp'),
            'Manual':    ('gameoptions', 'TeleportinON.bmp')
        },
        'Grid Args': {
            'row': 0,
            'column': 3
        }
    },
    'Initial Worm Energy': {
        'Type': 'ubyte',
        'Default': 100,
        'Image': ('gameoptions', 'WormEnergy', '000000.bmp'),
        'Grid Args': {
            'row': 0,
            'column': 0
        },
        'Popup Text': '0=DEATH. Everything from 1-255 should be fine.'
    },
    'Turn Time': {
        'Type': 'sbyte',
        'Default': 45,  # 0x00 to 0x7F=represent seconds, 0x80 to 0xFF=timer counts up
        'Image': ('gameoptions', 'TurnTime', '000006.bmp'),
        'Grid Args': {
            'row': 1,
            'column': 1
        },
        'Popup Text': '0-127 represent seconds; 128-255 causes timer to count up'
    },
    'Round Time': {
        'Type': 'sbyte',
        'Default': 15, # 0x00=sudden death triggering on the first turn, 0x01 to 0x7F=represent minutes, 0x80 to 0xFF=represent seconds, in a way that 0xFF=1s and 0x80=128s.
        'Image': ('gameoptions', 'RoundTime', 'minutes.bmp'),
        'Grid Args': {
            'row': 1,
            'column': 0
        },
        'Popup Text': '0=Instant sudden death; 1-127=minutes; 128-255=seconds (but 128=1s and 255=128s annoyingly)'
    },
    'Number of Rounds': {
        'Type': 'byte',
        'Default': 1, # 0x00=1, Other=represent number of rounds
        'Image': ('gameoptions', 'winsrequired', '000001.bmp'),
        'Grid Args': {
            'row': 0,
            'column': 1
        },
        'Popup Text': 'Number of wins required to end the game. Can be 1-255. 0 is the same as 1'
    },
    'Blood': {
        'Type': 'bool',
        'Default': False,
        'Images': {
            False: ('OptionsSpecial', 'bloff.bmp'),
            True:  ('OptionsSpecial', 'blon.bmp')
        },
        'Grid Args': {
            'row': 0,
            'column': 0
        }
    },
    'Aqua Sheep': {
        'Type': 'bool',
        'Default': False,
        'Images': {
            False: ('Custom', 'aquaoff.png'),
            True:  ('Custom', 'aquaon.png')
        },
        'Grid Args': {
            'row': 0,
            'column': 1
        }
    },
    'Sheep Heaven': {
        'Type': 'bool',
        'Default': False,
        'Images': {
            False: ('OptionsSpecial', 'shoff.bmp'),
            True:  ('OptionsSpecial', 'shon.bmp')
        },
        'Grid Args': {
            'row': 0,
            'column': 2
        }
    },
    'God Worms': {
        'Type': 'bool',
        'Default': False,
        'Images': {
            False: ('OptionsSpecial', 'gmoff.bmp'),
            True:  ('OptionsSpecial', 'gmon.bmp')
        },
        'Grid Args': {
            'row': 1,
            'column': 0
        }
    },
    'Indestructible Land': {
        'Type': 'bool',
        'Default': False,
        'Images': {
            False: ('OptionsSpecial', 'indlandoff.bmp'),
            True:  ('OptionsSpecial', 'indlandon.bmp')
        },
        'Grid Args': {
            'row': 1,
            'column': 1
        }
    },
    'Upgraded Grenade': {
        'Type': 'bool',
        'Default': False,
        'Images': {
            False: ('OptionsSpecial', 'gmoff.bmp'),
            True:  ('OptionsSpecial', 'gmon.bmp')
        },
        'Grid Args': {
            'row': 1,
            'column': 2
        }
    },
    'Upgraded Shotgun': {
        'Type': 'bool',
        'Default': False,
        'Images': {
            False: ('OptionsSpecial', 'gmoff.bmp'),
            True:  ('OptionsSpecial', 'gmon.bmp')
        },
        'Grid Args': {
            'row': 2,
            'column': 0
        }
    },
    'Upgraded Clusters': {
        'Type': 'bool',
        'Default': False,
        'Images': {
            False: ('OptionsSpecial', 'gmoff.bmp'),
            True:  ('OptionsSpecial', 'gmon.bmp')
        },
        'Grid Args': {
            'row': 2,
            'column': 1
        }
    },
    'Upgraded Longbow': {
        'Type': 'bool',
        'Default': False,
        'Images': {
            False: ('OptionsSpecial', 'gmoff.bmp'),
            True:  ('OptionsSpecial', 'gmon.bmp')
        },
        'Grid Args': {
            'row': 2,
            'column': 2
        }
    },
    'Team Weapons': {
        'Type': 'bool',
        'Default': False,
        'Images': {
            False: ('Custom', 'teamwepyes.bmp'),
            True:  ('Custom', 'teamwepno2.bmp')
        },
        'Grid Args': {
            'row': 3,
            'column': 0
        }
    },
    'Super Weapons in Crates': {
        'Type': 'bool',
        'Default': False,
        'Images': {
            False: ('OptionsSpecial', 'gmoff.bmp'),
            True:  ('OptionsSpecial', 'gmon.bmp')
        },
        'Grid Args': {
            'row': 3,
            'column': 1
        }
    }
})

items = list(OPTIONS.items()) 

MAIN_MENU_SLICE = items[1:9] + items[10:27]
SPECIAL_MENU_SLICE = items[27:]
HIDDEN_MENU_SLICE = [items[0], items[9]] # python tries to add them if we do items[0] + items[10]

MAIN_MENU_OPTIONS = OrderedDict({k:v for k,v in MAIN_MENU_SLICE})
SPECIAL_MENU_OPTIONS = OrderedDict({k:v for k,v in SPECIAL_MENU_SLICE})
HIDDEN_OPTIONS = OrderedDict({k:v for k,v in HIDDEN_MENU_SLICE})