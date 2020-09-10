from django.db.models import Model, CharField, ManyToManyField, ForeignKey, CASCADE, IntegerField

# Create your models here.
class Hero(Model):
    name = CharField("name", max_length=200)


class Skill(Model):
    hero = ForeignKey(Hero, on_delete=CASCADE, related_name='skills')
    order = IntegerField("order", default=-1)
    name = CharField("skill name", max_length=200)
    damage = CharField("Damage", max_length=200)