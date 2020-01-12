"""
options.py by Byebrid
---------------------
For info on which options we can change for each scheme.

See https://worms2d.info/Game_scheme_file for more info.

Glossary
--------
- Type_Native: The type as stated in the manual. Recorded as str since not all pythonic types
"""

OPTIONS = {
    'Signature': {
        'Default': b'SCHM'
    },
    'Super Weapons': { #Actually represents version but equivalent to allowing super weapons
        'Values_Images': [
            (b'\x00', False, ('Custom', 'superwepno.bmp')),
            (b'\x01', True,  ('Custom', 'superwepyes.bmp'))
        ],
        'Position': {
            'row': 2,
            'column': 3
        }
    },
    'Hot-Seat Delay': {
        'Values_Images': [
            (None, 5, ('gameoptions', 'HotseatDelay', '000002.bmp')),
        ],
        'Position': {
            'row': 3,
            'column': 0
        },
        'Special Note': '0-255 seconds.',
        'Type_Native': 'ubyte',
    },
    'Retreat Time': {
        'Values_Images': [
            (None, 3, ('gameoptions', 'RetreatTime', '000002.bmp')),
        ],
        'Position': {
            'row': 2,
            'column': 0
        },
        'Special Note': '0-255 seconds.',
        'Type_Native': 'byte'
    },
    'Rope Retreat Time': {
        'Values_Images': [
            (None, 5, ('gameoptions', 'RopeRetreat', '000003.bmp')),
        ],
        'Position': {
            'row': 2,
            'column': 1
        },
        'Special Note': '0-255 seconds.',
        'Type_Native': 'byte',
        'Type_User': int
    },
    'Display Total Round Time': {
        'Values_Images': [
            (b'\x00', False, ('gameoptions', 'RoundTimeOFF.bmp')),
            (b'\x01', True,  ('gameoptions', 'RoundTimeON.bmp'))
        ],
        'Position': {
            'row': 3,
            'column': 1
        }
    },
    'Automatic Replays': {
        'Values_Images': [
            (b'\x00', False, ('gameoptions', 'replayOFF.bmp')),
            (b'\x01', True,  ('gameoptions', 'replayON.bmp'))
        ],
        'Position': {
            'row': 4,
            'column': 0
        }
    },
    'Fall Damage': {
        'Values_Images': [
            (None, 1, ('Custom', 'worm_falling.jpg')),
        ],
        'Position': {
            'row': 2,
            'column': 2
        },
        'Special Note': 'See https://worms2d.info/Fall_Damage',
        'Type_Native': 'byte',
    },
    'Anchored': {
        'Values_Images': [
            (b'\x00', False, ('gameoptions', 'artilleryOFF.bmp')),
            (b'\x01', True,  ('gameoptions', 'artilleryON.bmp'))
        ],
        'Position': {
            'row': 0,
            'column': 4
        }
    },
    'Bounty Mode': {
        'Default': b'\x17'
    },
    'Stockpiling Mode': {
        'Values_Images': [
            (b'\x00', 'Replenishing', ('gameoptions', 'Stockpiling', '000001.bmp')),
            (b'\x01', 'Accumulating', ('gameoptions', 'Stockpiling', '000002.bmp')),
            (b'\x02', 'Reducing',     ('gameoptions', 'Stockpiling', '000003.bmp'))
        ],
        'Position': {
            'row': 0,
            'column': 5
        }
    },
    'Worm Select': {
        'Values_Images': [
            (b'\x00', 'Ordered',   ('gameoptions', 'WormSelectOFF.bmp')),
            (b'\x01', 'Optional',  ('gameoptions', 'WormSelectON.bmp')),
            (b'\x02', 'Random',    ('gameoptions', 'WormSelectRANDOM.bmp'))
        ],
        'Position': {
            'row': 0,
            'column': 2
        }
    },
    'Sudden Death Event': {
        'Values_Images': [
            (b'\x00', 'Round Ends',      ('gameoptions', 'SuddenDeathModes', '00001.bmp')),
            (b'\x01', 'Nuclear Strike',  ('gameoptions', 'SuddenDeathModes', '00002.bmp')),
            (b'\x02', 'HP drops to 1',   ('gameoptions', 'SuddenDeathModes', '00003.bmp')),
            (b'\x02', 'Nothing happens?', ('gameoptions', 'SuddenDeathModes', '00004.bmp'))
        ],
        'Position': {
            'row': 3,
            'column': 5
        }
    },
    'Water Rise Rate': {
        'Values_Images': [
            (None, 1, ('gameoptions', 'WaterRiseSpeed', '000002.bmp')),
        ],
        'Position': {
            'row': 3,
            'column': 6
        },
        'Special Note': 'Very complicated. see https://worms2d.info/Sudden_Death',
        'Type_Native': 'sbyte',
    },
    'Weapon Crate Probability': {
        'Values_Images': [
            (None, 40, ('Custom', 'weapondrops.bmp')),
        ],
        'Position': {
            'row': 1,
            'column': 2
        },
        'Special Note': "Percentage chance depends on proportions of each crate type's probabilities. See https://worms2d.info/Crate_probability.",
        'Type_Native': 'sbyte',
    },
    'Donor Cards': {
        'Values_Images': [
            (b'\x00', False, ('gameoptions', 'DonorOFF.bmp')),
            (b'\x01', True,  ('gameoptions', 'DonorON.bmp'))
        ],
        'Position': {
            'row': 0,
            'column': 6
        }
    },
    'Health Crate Probability': {
        'Values_Images': [
            (None, 40, ('Custom', 'healthdrops.bmp')),
        ],
        'Position': {
            'row': 1,
            'column': 3
        },
        'Special Note': "Percentage chance depends on proportions of each crate type's probabilities. See https://worms2d.info/Crate_probability.",
        'Type_Native': 'sbyte',
    },
    'Health Crate Energy': {
        'Values_Images': [
            (None, 50, ('gameoptions', 'HealthCrate', '000002.bmp')),
        ],
        'Position': {
            'row': 1,
            'column': 5
        },
        'Special Note': 'From 0-255',
        'Type_Native': 'ubyte',
    },
    'Utility Crate Probability': {
        'Values_Images': [
            (None, 20, ('Custom', 'utilitydrops.bmp')),
        ],
        'Position': {
            'row': 1,
            'column': 4
        },
        'Special Note': "Percentage chance depends on proportions of each crate type's probabilities. See https://worms2d.info/Crate_probability.",
        'Type_Native': 'sbyte',
    },
    'Hazardous Object Types': {
        'Values_Images': [
            (None, 5, ('gameoptions', 'Objects', '000004.bmp')),
        ],
        'Position': {
            'row': 3,
            'column': 2
        },
        'Special Note': 'Very complicated. see https://worms2d.info/Hazardous_Objects#How_is_this_setting_saved_in_a_WSC_file.3F',
        'Type_Native': 'byte',
    },
    'Mine Delay': {
        'Values_Images': [
            (None, 3, ('gameoptions', 'MineFuse.tga', '000004.bmp')),
        ],
        'Position': {
            'row': 3,
            'column': 3
        },
        'Special Note': '4,128-255 will be random (between 0-3 seconds); 0-3,5-127 represent seconds.',
        'Type_Native': 'byte',
    },
    'Dud Mines': {
        'Values_Images': [
            (b'\x00', False, ('gameoptions', 'DudmineOFF.bmp')),
            (b'\x01', True,  ('gameoptions', 'DudmineON.bmp'))
        ],
        'Position': {
            'row': 3,
            'column': 4
        }
    },
    'Worm Placement': {
        'Values_Images': [
            (b'\x00', 'Automatic', ('gameoptions', 'TeleportinOFF.bmp')),
            (b'\x01', 'Manual',    ('gameoptions', 'TeleportinON.bmp'))
        ],
        'Position': {
            'row': 0,
            'column': 3
        }
    },
    'Initial Worm Energy': {
        'Values_Images': [
            (None, 100, ('gameoptions', 'WormEnergy', '000000.bmp')),
        ],
        'Position': {
            'row': 0,
            'column': 0
        },
        'Special Note': '0=DEATH. Everything from 1-255 should be fine.',
        'Type_Native': 'ubyte'
    },
    'Turn Time': {
        'Values_Images': [
            (None, 45, ('gameoptions', 'TurnTime', '000006.bmp'))
        ],
        'Position': {
            'row': 1,
            'column': 1
        },
        'Special Note': '0-127 represent seconds; 128-255 causes timer to count up',
        'Type_Native': 'sbyte', # 0x00 to 0x7F=represent seconds, 0x80 to 0xFF=timer counts up
        'Type_User': int # Perhaps test to see if in range of 0-127
    },
    'Round Time': {
        'Values_Images': [
            (None, 15, ('gameoptions', 'RoundTime', 'minutes.bmp'))
        ],
        'Position': {
            'row': 1,
            'column': 0
        },
        'Special Note': '0=Instant sudden death; 1-127=minutes; 128-255=seconds (but 128=1s and 255=128s annoyingly)',
        'Type_Native': 'sbyte', # 0x00=sudden death triggering on the first turn, 0x01 to 0x7F=represent minutes, 0x80 to 0xFF=represent seconds, in a way that 0xFF=1s and 0x80=128s.
        'Type_User': int
    },
    'Number of Rounds': {
        'Values_Images': [
            (None, 1, ('gameoptions', 'winsrequired', '000001.bmp')),
        ],
        'Position': {
            'row': 0,
            'column': 1
        },
        'Special Note': 'Number of wins required to end the game. Can be 1-255. 0 is the same as 1',
        'Type_Native': 'byte', # 0x00=1, Other=represent number of rounds
    },
    'Blood': {
        'Values_Images': [
            (b'\x00', False, ('OptionsSpecial', 'bloff.bmp')),
            (b'\x01', True,  ('OptionsSpecial', 'blon.bmp'))
        ],
        'Position': {
            'row': 0,
            'column': 0
        }
    },
    'Aqua Sheep': {
        'Values_Images': [
            (b'\x00', False, ('Custom', 'aquaoff.png')),
            (b'\x01', True,  ('Custom', 'aquaon.png'))
        ],
        'Position': {
            'row': 0,
            'column': 1
        }
    },
    'Sheep Heaven': {
        'Values_Images': [
            (b'\x00', False, ('OptionsSpecial', 'shoff.bmp')),
            (b'\x01', True,  ('OptionsSpecial', 'shon.bmp'))
        ],
        'Position': {
            'row': 0,
            'column': 2
        }
    },
    'God Worms': {
        'Values_Images': [
            (b'\x00', False, ('OptionsSpecial', 'gmoff.bmp')),
            (b'\x01', True,  ('OptionsSpecial', 'gmon.bmp'))
        ],
        'Position': {
            'row': 1,
            'column': 0
        }
    },
    'Indestructible Land': {
        'Values_Images': [
            (b'\x00', False, ('OptionsSpecial', 'indlandoff.bmp')),
            (b'\x01', True,  ('OptionsSpecial', 'indlandon.bmp'))
        ],
        'Position': {
            'row': 1,
            'column': 1
        }
    },
    'Upgraded Grenade': {
        'Values_Images': [
            (b'\x00', False, ('OptionsSpecial', 'gmoff.bmp')),
            (b'\x01', True,  ('OptionsSpecial', 'gmon.bmp'))
        ],
        'Position': {
            'row': 1,
            'column': 2
        }
    },
    'Upgraded Shotgun': {
        'Values_Images': [
            (b'\x00', False, ('OptionsSpecial', 'gmoff.bmp')),
            (b'\x01', True,  ('OptionsSpecial', 'gmon.bmp'))
        ],
        'Position': {
            'row': 2,
            'column': 0
        }
    },
    'Upgraded Clusters': {
        'Values_Images': [
            (b'\x00', False, ('OptionsSpecial', 'gmoff.bmp')),
            (b'\x01', True,  ('OptionsSpecial', 'gmon.bmp'))
        ],
        'Position': {
            'row': 2,
            'column': 1
        }
    },
    'Upgraded Longbow': {
        'Values_Images': [
            (b'\x00', False, ('OptionsSpecial', 'gmoff.bmp')),
            (b'\x01', True,  ('OptionsSpecial', 'gmon.bmp'))
        ],
        'Position': {
            'row': 2,
            'column': 2
        }
    },
    'Team Weapons': {
        'Values_Images': [
            (b'\x00', False, ('OptionsSpecial', 'gmoff.bmp')),
            (b'\x01', True,  ('OptionsSpecial', 'gmon.bmp'))
        ],
        'Position': {
            'row': 2,
            'column': 2
        },
        'Default': b'\x00'
    },
    'Super Weapons in Crates': {
        'Values_Images': [
            (b'\x00', False, ('OptionsSpecial', 'gmoff.bmp')),
            (b'\x01', True,  ('OptionsSpecial', 'gmon.bmp'))
        ],
        'Position': {
            'row': 2,
            'column': 2
        },
        'Default': b'\x00'
    },
}

# print(len(OPTIONS))