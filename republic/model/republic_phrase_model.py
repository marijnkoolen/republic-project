resolution_categories = {
    "resolution_accepted": [
        "is goedgevonden ende verstaan",
        "IS naar voorgaande deliberatie goedgevonden ende verstaan",
        "de voorfchreve Missive copielijck overgenomen",
    ],
    "resolution_decision": [
        "gehouden voor gecommiteert",
        "waar by goedgevonden is",
        "voor de genomen moeyte bedanckt",
        # should probably move somewhere else
    ],
    "resolution_not_accepted": [
        "WAAR op geen resolutie is gevallen",
    ],
    "resolution_opening": [
        "hebben ter Vergaderinge ingebraght",
        "Is ter Vergaderinge gelesen",
        "IS gehoort het rapport van",
        "Ontvangen een Missive van",
        "Op de Requeste van",
        "Zynde ter Vergaderinge getoont",
    ],
    "resolution_considered": [
        "WAAR op gedelibereert en in achtinge genomen zynde",
        "WAAR op gedelibereert zijnde",
        "WAAR op gedelibereert",
    ],
    "resolution_resumed": [
        "BY refumptie gedelibereert zynde",
    ],
    "resolution_summarized": [
        "DE Resolutien, gisteren genomen",
        "zyn gelesen en gerefumeert",
    ],
    "non_meeting_date": [
        "Nihil actum est.",
    ],
    "resolution_first_entry": [
        "Zynde Nieuwejaarsdagh",
    ],
    "participant_list": [
        "PRAESIDE",
        "PRAESENTIBUS",
    ],
}

category_index = {phrase: category for category in resolution_categories for phrase in resolution_categories[category]}

resolution_phrases = [phrase for category in resolution_categories for phrase in resolution_categories[category]]

participant_list_phrases = [
    "PRAESIDE",
    "PRAESENTIBUS",
]

week_day_names_handwritten = [
    "Lunæ",
    "Martis",
    "Mercurii",
    "Jovis",
    "Veneris",
    "Sabbathi",
    "Dominica"
]

week_day_names_printed = [
    "Lunae",
    "Martis",
    "Mercurii",
    "Jovis",
    "Veneris",
    "Sabbathi",
    "Dominica"
]


date_name_map = [
    {
        'text_type': 'printed',
        'resolution_type': 'ordinaris',
        'period_start': 1705,
        'period_end': 1796,
        'month_name': {
            'January': 1,
            'Januarij': 1,
            'February': 2,
            'Februarij': 2,
            'Maart': 3,
            'April': 4,
            'Mey': 5,
            'Junij': 6,
            'Juny': 6,
            'Julij': 7,
            'July': 7,
            'Augusti': 8,
            'September': 9,
            'October': 10,
            'November': 11,
            'December': 12
        },
        'week_day_name': {
            "Lunae": 0,
            "Martis": 1,
            "Mercurii": 2,
            "Jovis": 3,
            "Veneris": 4,
            "Sabbathi": 5,
            "Dominica": 6
        }
    },
    {
        'text_type': 'handwritten',
        'resolution_type': 'secreet',
        'period_start': 1600,
        'period_end': 1700,
        'month_name': {
            'January': 1,
            'Januarij': 1,
            'February': 2,
            'Februarij': 2,
            'Meerte': 3,
            'Martij': 3,
            'Marty': 3,
            'Meert': 3,
            'Aprilis': 4,
            'April': 4,
            'Maij': 5,
            'May': 5,
            'Mey': 5,
            'Meije': 5,
            'Meye': 5,
            'Maye': 5,
            'Junij': 6,
            'Juny': 6,
            'Julij': 7,
            'July': 7,
            'Augusti': 8,
            'Septembris': 9,
            'Septemb': 9,
            'September': 9,
            'Octobris': 10,
            'Octob': 10,
            'Novembris': 11,
            'Novemb': 11,
            'Decembris': 12,
            'Decemb': 12,
            'December': 12
        },
        'week_day_name': {
            "Lunae": 0,
            "Luna": 0,
            "Martis": 1,
            "Mercurij": 2,
            "Mercury": 2,
            "Jovis": 3,
            "Veneris": 4,
            "Sabbathi": 5,
            "Saterdach": 5,
            "Dominica": 6,
            "Sondach": 6
        }
    },
    {
        'text_type': 'handwritten',
        'resolution_type': 'ordinaris',
        'period_start': 1600,
        'period_end': 1700,
        'month_name': {
            'January': 1,
            'Januarij': 1,
            'February': 2,
            'Februarij': 2,
            'Meerte': 3,
            'Martij': 3,
            'Marty': 3,
            'Meert': 3,
            'Aprilis': 4,
            'April': 4,
            'Maij': 5,
            'May': 5,
            'Mey': 5,
            'Meije': 5,
            'Meye': 5,
            'Maye': 5,
            'Junij': 6,
            'Juny': 6,
            'Julij': 7,
            'July': 7,
            'Augusti': 8,
            'Septembris': 9,
            'Septemb': 9,
            'September': 9,
            'Octobris': 10,
            'Octob': 10,
            'Novembris': 11,
            'Novemb': 11,
            'Decembris': 12,
            'Decemb': 12,
            'December': 12
        },
        'week_day_name': {
            "Lunae": 0,
            "Luna": 0,
            "Martis": 1,
            "Mercurij": 2,
            "Mercury": 2,
            "Jovis": 3,
            "Jouis": 3,
            "Veneris": 4,
            "Sabbathi": 5,
            "Saterdach": 5,
            "Dominica": 6,
            "Sondach": 6
        },
        'month_day_name': {
            'eersten': 1,
            'jen': 1,
            'ijen': 2,
            'iijen': 3,
            'iiijen': 4,
            'ven': 5,
            'vjen': 6,
            'vien': 6,
            'vijen': 7,
            'viien': 7,
            'viijen': 8,
            'ixen': 9,
            '1xen': 9,
            'xen': 10,
            'xjen': 11,
            'xien': 11,
            'xijen': 12,
            'xiien': 12,
            'xiijen': 13,
            'xiiijen': 14,
            'xven': 15,
            'xvjen': 16,
            'xvien': 16,
            'xvijen': 17,
            'xviien': 17,
            'xviijen': 18,
            'xixen': 19,
            'xxen': 20,
            'xxjen': 21,
            'xxien': 21,
            'xxijen': 22,
            'xxiien': 22,
            'xxiijen': 23,
            'xxiiijen': 24,
            'xxven': 25,
            'xxvjen': 26,
            'xxvien': 26,
            'xxvijen': 27,
            'xxviien': 27,
            'xxviijen': 28,
            'xxixen': 29,
            'xxxen': 30,
            'xxxien': 30,
            'lesten': 0,
            'laesten': 0,
            'Laesten': 0,
            'naestlesten': -1,
            'nalesten': -1
        }
    }
]

month_names_early = [
    "Januarii",
    "Februarii",
    "Maart",
    "April",
    "Mey",
    "Junii",
    "Juli",
    "Augufti",
    "September",
    "October",
    "November",
    "December"
]

month_names_late = [
    "January",
    "February",
    "Maart",
    "April",
    "Mey",
    "Juny",
    "July",
    "Augufty",
    "September",
    "October",
    "November",
    "December"
]

week_day_name_map = {
    "Lunae": 1,
    "Martis": 2,
    "Mercurii": 3,
    "Jovis": 4,
    "Veneris": 5,
    "Sabbathi": 6,
    "Dominica": 7
}

month_map_early = {
    "Januarii": 1,
    "Februarii": 2,
    "Maart": 3,
    "April": 4,
    "Mey": 5,
    "Junii": 6,
    "Juli": 7,
    "Augufti": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

month_map_late = {
    "January": 1,
    "February": 2,
    "Maart": 3,
    "April": 4,
    "Mey": 5,
    "Juny": 6,
    "July": 7,
    "Augufty": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

keywords = resolution_phrases

spelling_variants = {
    "WAAR op gedelibereert zijnde": [
        "Waer op gedelibereert zynde"
    ],
    "DE Resolutien, gisteren genomen": [
        "DE Resolutien, eergisteren genomen",
    ],
    "Ontvangen een Missive van": [
        "ON een Missive van",
        "Ontfangen een Missive van",
        "Ontfangen twee Missiven van"
    ],
    "PRAESENTIBUS": [
        "PRASENTIBUS",
        "PRESENTIBUS",
        "P R A S E N T I B U S",
        "P R E S E N T I B U S"
    ],
    "PRAESIDE": [
        "PRASIDE",
        "PRESIDE",
        "P R A S I D E",
        "P R E S I D E"
    ],
    "is goedgevonden ende verstaan": [
        "IS goedgevonden ende verstaan",
        "Is goedgevonden en verstaan",
    ],
    "WAAR op geen resolutie is gevallen": [
        "Waer op geen resolutie is gevallen",
        "WAAR op geen resolutie voor alsnoch is gevallen",
        "Waer op geen resolutie voor alsnoch is gevallen",
    ]
}

session_phrase_model = [
    {
        'phrase': 'Extract uyt de Resolutien',
        'start_year': 1603, 'end_year': 1796,
        'label': 'extract',
        'variants': [
            'Extract uyt het Resolutie-',
            'Extract uyt het Register',
            'Extraheert uyt het Re-'
        ]
    },
    {
        'phrase': 'Het eerste jaar der Bataafsche Vryheid',
        'start_year': 1795, 'end_year': 1796,
        'label': 'tagline'
    },
    {
        'phrase': 'Nihil actum est',
        'start_year': 1603, 'end_year': 1796,
        'label': 'rest_day'
    },
    {
        'phrase': 'Zynde Vast- en Bede-dag',
        'start_year': 1703, 'end_year': 1796,
        'label': 'holiday',
        'variants': [
            'Zynde Danck-, Vast- en Bededagh'
        ]
    },
    {
        'phrase': 'GECOMPAREERT,',
        'start_year': 1703, 'end_year': 1796,
        'label': 'special_attendance'
    },
    {
        'phrase': 'Zyne Hoogheid den Heere Prince van ',
        'label': 'prince_attending',
        'start_year': 1703, 'end_year': 1796,
        'line_type': 'multi_line',
        'variants': [
            'Syne Hoogheyd den Heere Prince van ',
        ],
    },
    {
        'phrase': 'Præside,',
        'variants': ['Praeside'],
        'start_year': 1603, 'end_year': 1680,
        'label': 'presiding'
    },
    {
        'phrase': 'Præsentibus,',
        'variants': ['praesentibus'],
        'start_year': 1603, 'end_year': 1680,
        'label': 'attending'
    },
    {
        'phrase': 'PRAESIDE,',
        'variants': ['P R AE S I D E,'],
        'start_year': 1703, 'end_year': 1796,
        'label': 'presiding'
    },
    {
        'phrase': 'PRAESENTIBUS,',
        'variants': ['P R AE S E N T I B U S,'],
        'start_year': 1703, 'end_year': 1796,
        'label': 'attending'
    },
    {
        'phrase': 'Den Heere',
        'variants': ['De Heer'],
        'start_year': 1603, 'end_year': 1796,
        'label': 'president'
    },
    {
        'phrase': 'De Heeren',
        'start_year': 1603, 'end_year': 1796,
        'label': 'attendants'
    },
    {
        'phrase': 'Den Burger',
        'start_year': 1795, 'end_year': 1796,
        'label': 'president'
    },
    {
        'phrase': 'De Burgers',
        'start_year': 1795, 'end_year': 1796,
        'label': 'attendants'
    },
    {
        'phrase': 'DE Resolutien gisteren genomen',
        'variants': [
            'DE Resolutien eergisteren genomen',
            'DE Resolutien voorleede ',
            'DE Resolutien gisteren ge-',
        ],
        'start_year': 1705, 'end_year': 1796,
        'label': 'reviewed'
    },
    {
        'phrase': 'De resolutien gisteren genomen',
        'variants': [
            'De resolutien eergisteren genomen',
            'De resolutien voorleden ',
            'De resolutien gisteren ge-',
        ],
        'start_year': 1603, 'end_year': 1704,
        'label': 'reviewed'
    },
]

extra_phrases = [
    {
        'phrase': 'Zyne Hoogheid den Heere Prince van ',
        'label': 'prince_attending',
        'start_year': 1703, 'end_year': 1796,
        'line_type': 'multi_line',
        'variants': [
            'Syne Hoogheyd den Heere Prince van ',
        ],
        'max_offset': 4
    }
]

holiday_phrases = [
    {
        'phrase': 'Zynde Nieuwjaarsdag',
        'start_year': 1703, 'end_year': 1796,
        'label': 'holiday',
        'date_specifc': True
    },
    {
        'phrase': 'Zynde Vast- en Bede-dag',
        'start_year': 1703, 'end_year': 1796,
        'label': 'holiday',
        'date_specifc': False
    },
    {
        'phrase': 'Zynde eerste Paasdag',
        'start_year': 1703, 'end_year': 1796,
        'label': 'holiday',
        'date_specifc': False
    },
    {
        'phrase': 'Zynde tweede Paasdag',
        'start_year': 1703, 'end_year': 1796,
        'label': 'holiday',
        'date_specifc': False
    },
    {
        'phrase': 'Zynde Hemelvaartsdag',
        'start_year': 1703, 'end_year': 1796,
        'label': 'holiday',
        'date_specifc': False
    },
    {
        'phrase': 'Zynde tweede Pinksterdag',
        'start_year': 1703, 'end_year': 1796,
        'label': 'holiday',
        'date_specifc': False
    },
    {
        'phrase': 'Zynde eerste Kerstdag',
        'start_year': 1703, 'end_year': 1796,
        'label': 'holiday',
        'date_specifc': True
    },
    {
        'phrase': 'Zynde tweede Kerstdag',
        'start_year': 1703, 'end_year': 1796,
        'label': 'holiday',
        'date_specifc': True
    },
]

resolution_phrase_model = [
    {
        'phrase': 'hebben ter Vergaderinge ingebraght',
        'label': 'resolution_opening',
        'variants': [
            'heeft ter Vergaderinge ingebraght',
        ]
    },
    {
        'phrase': 'Zynde ter Vergaderinge getoont',
        'label': 'resolution_opening',
        'max_offset': 4
    },
    {
        'phrase': 'Is ter Vergaderinge gelesen',
        'label': 'resolution_opening',
        'max_offset': 4
    },
    {
        'phrase': 'Ontfangen een Missive van',
        'label': 'resolution_opening',
        'resolution_source': 'missive',
        'variants': [
            'ON een Missive van',
            'ONtfangen een Miffive van',
            'Nogh ontfangen een Missive van'
        ],
        'max_offset': 4
    },
    {
        'phrase': 'Is gehoort het rapport van',
        'label': 'resolution_opening',
        'resolution_source': 'rapport',
        'max_offset': 4
    },
    {
        'phrase': 'Op de Requeste van',
        'label': 'resolution_opening',
        'resolution_source': 'request',
        'max_offset': 4
    },
    {
        'phrase': 'Op de Memorie van',
        'label': 'resolution_opening',
        'resolution_source': 'memorie',
        'max_offset': 4
    },
    {
        'phrase': 'Op het gerapporteerde van de Heeren van',
        'label': 'resolution_opening',
        'resolution_source': 'rapport',
        'max_offset': 4
    },
    {
        'phrase': 'heeft aan haar Hoogh Mogende voorgedraagen en bekend gemaackt',
        'variants': [
            'hebben aan haar Hoogh Mogende voorgedraagen en bekend gemaackt'
        ],
        'label': 'resolution_opening',
        'max_offset': 100
    },
    {
        'phrase': 'is goedgevonden ende verstaan',
        'label': 'resolution_decision',
        'variants': [
            "IS naar voorgaande deliberatie goedgevonden ende verstaan",
        ]
    },
    {
        'phrase': 'de voorfchreve Missive copielijck overgenomen',
        'label': 'resolution_decision',
    },
    {
        'phrase': 'waar by goedgevonden is',
        'label': 'resolution_decision',
    },
    {
        'phrase': 'gehouden voor gecommiteert',
        'label': 'resolution_decision',
    },
    {
        'phrase': 'WAAR op gedelibereert en in achtinge genomen zynde',
        'label': 'resolution_decision',
    },
    {
        'phrase': 'WAAR op gedelibereert zijnde',
        'label': 'resolution_decision',
    },
    {
        'phrase': 'WAAR op gedelibereert',
        'label': 'resolution_decision',
    },
    {
        'phrase': 'voor de genomen moeyte bedanckt',  # should probably move somewhere else
        'label': 'resolution_decision',
    },
    {
        'phrase': 'WAAR op geen resolutie is gevallen',
        'variants': [
            "Waer op geen resolutie is gevallen",
            "WAAR op geen resolutie voor alsnoch is gevallen",
            "Waer op geen resolutie voor alsnoch is gevallen",
        ],
        'label': 'resolution_decision',
    },
    {
        'phrase': 'BY refumptie gedelibereert zynde',
        'label': 'resolution_opening',
        'max_offset': 4
    },
    {
        'phrase': 'DE Resolutien, gisteren genomen',
        'label': 'resolution_summarized',
        'max_offset': 4,
        'variants': [
            'DE Resolutien, eergisteren genomen',
            'DE Resolutien voorleede ',
        ]
    },
    {
        'phrase': 'zyn gelesen en gerefumeert',
        'label': 'resolution_summarized'
    },
]
