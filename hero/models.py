from django.db.models import (
    Model,
    CharField,
    ManyToManyField,
    ForeignKey,
    CASCADE,
    IntegerField,
)


class Hero(Model):
    name = CharField("name", max_length=200)


class Skill(Model):
    hero = ForeignKey(Hero, on_delete=CASCADE, related_name="skills")
    order = IntegerField("order", default=-1)
    name = CharField("skill name", max_length=200)
    damage = CharField("Damage", max_length=200)


class ExtraSkill(Model):
    skill = ForeignKey(Skill, on_delete=CASCADE, related_name="extras")
    name = CharField("skill name", max_length=200)
    trigger = CharField("Trigger", max_length=10)
    damage = CharField("Damage", max_length=200)