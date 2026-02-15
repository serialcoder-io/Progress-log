
from pytest_factoryboy import register
from users.tests.factories import UserFactory
from tasks.tests.factories import GoalFactory, SubGoalFactory, SkillFactory, ResourceFactory

register(UserFactory)
register(GoalFactory)
register(SubGoalFactory)
register(SkillFactory)
register(ResourceFactory)
