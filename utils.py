def get_keywords(seed_keyword):
    seed = seed_keyword.strip().lower()

    keyword_rows = [
        {
            "keyword": f"{seed}",
            "volume": 4400,
            "competition": "Medium",
            "intent": "Commercial",
            "difficulty": 47
        },
        {
            "keyword": f"best {seed}",
            "volume": 2900,
            "competition": "High",
            "intent": "Commercial",
            "difficulty": 61
        },
        {
            "keyword": f"{seed} tools",
            "volume": 1900,
            "competition": "Medium",
            "intent": "Commercial",
            "difficulty": 52
        },
        {
            "keyword": f"{seed} strategy",
            "volume": 1300,
            "competition": "Low",
            "intent": "Informational",
            "difficulty": 35
        },
        {
            "keyword": f"{seed} checklist",
            "volume": 880,
            "competition": "Low",
            "intent": "Informational",
            "difficulty": 28
        },
        {
            "keyword": f"{seed} examples",
            "volume": 1200,
            "competition": "Low",
            "intent": "Informational",
            "difficulty": 33
        }
    ]

    return keyword_rows
