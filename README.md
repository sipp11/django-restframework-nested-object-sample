# Django + RestFramework + Nested data

We need to handle data like this which restframework doesn't handle automatically.

    {"name": "Airi","skills": [{"order": 1, "name": "A1", "damage": "232"}]}

## Test in shell

    from hero.views import *
    from hero.models import *

    s = HeroSerializer(data={"name": "Airi","skills": [{"order": 1, "name": "A1", "damage": "232"}]})
    s.is_valid()
    s.errors
