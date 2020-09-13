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
        # extras that are gone
        existing_extras = [i.name for i in instance.extras.all()]
        incoming_extras = [i["name"] for i in extras]
        rmving = set(existing_extras) - set(incoming_extras)
        if rmving:
            ExtraSkill.objects.filter(skill=instance, name__in=list(rmving)).delete()

        # create/update
        for extra in extras:
            extra_obj, created = ExtraSkill.objects.get_or_create(
                skill=instance,
                name=extra["name"],
                defaults={"skill": instance, **extra},
            )
            if not created:  # update
                ExtraSkill.objects.filter(pk=extra_obj.pk).update(**extra)

    def update(self, instance, validated_data):
        extras = validated_data.pop("extras")
        self.Meta.model.objects.filter(pk=instance.pk).update(**validated_data)
        self.extras_create_or_update(instance, extras)
        return instance

    def create(self, validated_data):
        model = self.Meta.model
        extras = validated_data.pop("extras")
        if "hero" not in validated_data:
            raise serializers.ValidationError("Missing hero")
        obj, created = model.objects.get_or_create(
            hero=validated_data["hero"],
            order=validated_data["order"],
            defaults=validated_data,
        )
        if not created:  # update
            model.objects.filter(pk=obj.pk).update(**validated_data)
        self.extras_create_or_update(obj, extras)
        return obj


class HeroSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = Hero
        fields = "__all__"

    def skill_create_or_update(self, instance, skills):
        if not skills:
            return instance

        # skills that are gone
        existing_skills = [i.order for i in instance.skills.all()]
        incoming_skills = [i["order"] for i in skills]
        rmving = set(existing_skills) - set(incoming_skills)
        if rmving:
            Skill.objects.filter(hero=instance, order__in=list(rmving)).delete()

        # create/update
        for skill in skills:
            data = {"hero": instance.pk, **skill}
            try:
                s = Skill.objects.get(hero=instance, order=skill["order"])
                # update skill
                s1 = SkillSerializer(s, data=data)
                if s1.is_valid():
                    s1.save()
            except Skill.DoesNotExist:
                s = SkillSerializer(data=data)
                if s.is_valid():
                    s.save()

    def update(self, instance, validated_data):
        skills = validated_data.pop("skills")
        self.Meta.model.objects.filter(pk=instance.pk).update(**validated_data)
        self.skill_create_or_update(instance, skills)
        return instance

    def create(self, validated_data):
        model = self.Meta.model
        skills = validated_data.pop("skills")
        obj, created = model.objects.get_or_create(
            name=validated_data["name"], defaults=validated_data
        )
        if not created:  # update
            model.objects.filter(pk=obj.pk).update(**validated_data)
        self.skill_create_or_update(obj, skills)
        return obj
