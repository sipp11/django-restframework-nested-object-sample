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
            "id",
        ]
        extra_kwargs = {"hero": {"write_only": True, "required": False}}

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
        if "hero" not in validated_data:
            raise serializers.ValidationError("Missing hero")
        obj, created = self.Meta.model.objects.get_or_create(
            hero=validated_data["hero"],
            order=validated_data["order"],
            defaults=validated_data,
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
            data = {"hero": obj.pk, **skill}
            try:
                s = Skill.objects.get(hero=obj, order=skill["order"])
                # update skill
                s1 = SkillSerializer(s, data=data)
                if s1.is_valid():
                    s1.save()
            except Skill.DoesNotExist:
                s = SkillSerializer(data=data)
                if s.is_valid():
                    s.save()
        return obj