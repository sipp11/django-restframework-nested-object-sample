from rest_framework import serializers
from .models import Hero, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        exclude = [
            "hero",
            "id",
        ]


class HeroSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = Hero
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)
        skills = validated_data.pop("skills")
        print("popped: ", validated_data)
        h, created = Hero.objects.get_or_create(
            name=validated_data["name"], defaults=validated_data
        )
        if skills:
            for skill in skills:
                s, created = Skill.objects.get_or_create(
                    hero=h, name=skill["name"], defaults={"hero": h, **skill}
                )
        return h