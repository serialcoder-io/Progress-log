import pytest
from django.db import IntegrityError

from tasks.tests.factories import GoalFactory
from users.models import User
from tasks.models import Goal, SubGoal, Skill, Resource


@pytest.mark.django_db
def test_create_new_goal(goal_factory):
    goal = goal_factory()
    assert Goal.objects.count() == 1
    assert goal.status == "pending"
