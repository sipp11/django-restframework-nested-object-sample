# Django + RestFramework + Nested data

We need to handle data like this which restframework doesn't handle automatically.

    airi = {
        "name": "Airi",
        "skills": [
            {
                "order": 1,
                "name": "A1",
                "damage": "280",
                "extras": [{ "trigger": "ultimate", "name": "A11", "damage": 1000 }]
            },
            {
                "order": 2,
                "name": "A2",
                "damage": "155",
                "extras": [{ "trigger": "A1", "name": "A21", "damage": 750 }]
            }
        ]
    }

    hayate = {
        "name": "Hayate",
        "skills": [
            {
                "order": 1,
                "name": "H1",
                "damage": "280",
                "extras": [{ "trigger": "ultimate", "name": "H100", "damage": 1720 }]
            },
            {
                "order": 2,
                "name": "H2",
                "damage": "155",
                "extras": [{ "trigger": "ultimate", "name": "H200", "damage": 740 }]
            }
        ]
    }


## Test in shell

    from hero.views import *
    from hero.models import *

    s = HeroSerializer(data=airi)
    s.is_valid()
    # s.errors
    s.save()

    s = HeroSerializer(data=hayate)
    s.is_valid()
    # s.errors
    s.save()
