# Django + RestFramework + Nested data

We need to handle data like this which restframework doesn't handle automatically.

    airi = {
        "name": "Airi",
        "skills": [
            {
            "order": 1,
            "name": "A1",
            "damage": "232",
            "extras": [{ "trigger": "ultimate", "name": "A100", "damage": 1000 }]
            }
        ]
    }


## Test in shell

    from hero.views import *
    from hero.models import *

    s = HeroSerializer(data=airi)
    s.is_valid()
    s.errors
