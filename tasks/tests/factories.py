from datetime import timedelta
import json

import factory
from faker import Faker
from django.contrib.auth import get_user_model
from tasks.models import Goal, SubGoal, Skill, Resource, StatusChoices
from users.tests.factories import UserFactory
# factory.LazyAttribute(lambda a: fake.date_time_between(start_date='-15d', end_date='now'))


def fake_quill_text(text: str):
    return json.dumps({
        "delta": {
            "ops": [
                {"insert": text + "\n"}
            ]
        },
        "html": f"<p>{text}</p>"
    })

User = get_user_model()
fake = Faker('en_GB')

class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal
        skip_postgeneration_save = True

    user = factory.SubFactory(UserFactory)
    name = factory.LazyAttribute(lambda a: f"{a.user.display_name}'s Goal {fake.unique.word()}")
    description = factory.LazyAttribute(
        lambda a: fake_quill_text(fake.text(max_nb_chars=500))
    )
    started_at = None
    completed_at = None
    deadline_at = None
    status = factory.LazyFunction(lambda: StatusChoices.PENDING)

    @factory.post_generation
    def set_deadline(obj, create, extracted, **kwargs):
        if not create:
            return
        obj.deadline_at = obj.created_at + timedelta(days=45)
        obj.save(update_fields=["deadline_at"])


class SubGoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubGoal
        skip_postgeneration_save = True

    goal = factory.SubFactory(GoalFactory)
    name = factory.LazyAttribute(lambda a: f"{a.goal.name} '-' {fake.unique.word()}")
    description = factory.LazyAttribute(
        lambda a: fake_quill_text(fake.text(max_nb_chars=500))
    )
    started_at = None
    completed_at = None
    deadline_at = None
    status = factory.LazyFunction(lambda: StatusChoices.PENDING)

    @factory.post_generation
    def set_deadline(obj, create, extracted, **kwargs):
        if not create:
            return
        obj.deadline_at = obj.created_at + timedelta(days=5)
        obj.save(update_fields=["deadline_at"])


class SkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Skill
        skip_postgeneration_save = True

    subgoal = factory.SubFactory(SubGoalFactory)
    name = factory.LazyAttribute(lambda a: f"{a.subgoal.name} '-' {fake.unique.word()}")
    description = factory.LazyAttribute(
        lambda a: fake_quill_text(fake.text(max_nb_chars=500))
    )
    started_at = None
    completed_at = None
    status = factory.LazyFunction(lambda: StatusChoices.PENDING)
    deadline_at = None


    @factory.post_generation
    def set_deadline(obj, create, extracted, **kwargs):
        if not create:
            return
        obj.deadline_at = obj.created_at + timedelta(days=1)
        obj.save(update_fields=["deadline_at"])


class ResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Resource

    skill = factory.SubFactory(SkillFactory)
    name = factory.LazyAttribute(lambda a: f"{a.skill.name} '-' {fake.unique.word()}")
    url = factory.LazyAttribute(lambda a: fake.url())

