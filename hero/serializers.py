from rest_framework import serializers
from .models import Hero, Skill, ExtraSkill


class ExtraSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraSkill
        exclude = ["id", "skill"]


class SkillSerializer(serializers.ModelSerializer):
    extras = ExtraSkillSerializer(many=True)

    class Meta:
        model = Skill
        exclude = [
            "hero",
            "id",
        ]

    def extras_create_or_update(self, instance, extras):
        if not extras:
            return
        for extra in extras:
            _, created = ExtraSkill.objects.get_or_create(
                skill=instance,
                name=extra["name"],
                defaults={"skill": instance, **extra},
            )

    def update(self, instance, validated_data):
        extras = validated_data.pop("extras")
        self.Meta.model.objects.filter(pk=instance.pk).update(**validated_data)
        self.extras_create_or_update(instance, extras)
        return instance

    def create(self, validated_data):
        extras = validated_data.pop("extras")
        h = Hero.objects.all().last()
        obj, created = self.Meta.model.objects.get_or_create(
            hero=h,order=validated_data["order"], 
            defaults={"hero": h, **validated_data},
            #defaults=validated_data
        )
        self.extras_create_or_update(obj, extras)
        return obj


class HeroSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = Hero
        fields = "__all__"

    def create(self, validated_data):
        skills = validated_data.pop("skills")
        obj, created = self.Meta.model.objects.get_or_create(
            name=validated_data["name"], defaults=validated_data
        )
        if not skills:
            return obj

        for skill in skills:
            try:
                s = Skill.objects.get(order=skill["order"])
                # update skill
                s1 = SkillSerializer(s, data=skill)
                if s1.is_valid():
                    s1.save()
            except Skill.DoesNotExist:
                s = SkillSerializer(data=skill)
                if s.is_valid():
                    s.save()
        return obj