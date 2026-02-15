from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Prefetch, Subquery, OuterRef
from .models import Goal, SubGoal, Skill
from reviews.models import DailyReview, WeeklyReview, MonthlyReview, DailyReviewSkill
from django.db.models import Count, Q, F, ExpressionWrapper, IntegerField, Value, Sum, Case, When
from django.db.models.functions import Coalesce


@login_required
def goals(request):
    daily_time_subquery = (
        DailyReviewSkill.objects
        .filter(skill__subgoal__goal=OuterRef("pk"))
        .values("skill__subgoal__goal")
        .annotate(total=Sum("time_spent"))
        .values("total")
    )
    goals_list = (
        request.user.goals
        .annotate(
            all_subgoals_count=Count("subgoals", distinct=True),
            finish_subgoals_count=Count(
                "subgoals",
                filter=Q(subgoals__status="finished"),
                distinct=True
            ),
            skills_count=Count("subgoals__skills", distinct=True),
            time_spent=Coalesce(
                Subquery(daily_time_subquery),
                Value(0),
                output_field=IntegerField()
            ),
            progress = Case(
                When(all_subgoals_count=0, then=Value(0)),
                default=ExpressionWrapper(
                    F('finish_subgoals_count') * 100 / F('all_subgoals_count'),
                    output_field=IntegerField()
                )
            )
        ).order_by("created_at")
    )

    paginator = Paginator(goals_list, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}

    if request.htmx:
        return render(request, "cotton/partials/goals_page.html", context)
    return render(request, "tasks/goals.html", context)


@login_required
def goal_details(request, goal_id):
    current_user = request.user
    goal = get_object_or_404(
        Goal.objects.annotate(
            skills_count=Count("subgoals__skills", distinct=True),
            finished_skills_count=Count(
                "subgoals__skills",
                filter=Q(subgoals__skills__status="finished"),
                distinct=True
            ),
            subgoals_count=Count("subgoals", distinct=True),
            finished_subgoals_count=Count(
                "subgoals",
                filter=Q(subgoals__status="finished"),
                distinct=True
            ),
            time_spent=Coalesce(
                Sum('subgoals__skills__daily_reviews_skill__time_spent'),
                Value(0),
                output_field=IntegerField()
            ),
            progress= Case(
                When(subgoals_count=0, then=Value(0)),
                default=ExpressionWrapper(
                    F("finished_subgoals_count") * 100 / F("subgoals_count"),
                    output_field=IntegerField()
                )
            )
        ),
        id=goal_id, 
        user=current_user
    )

    subgoals = (
        goal.subgoals
        .annotate(
            time_spent=Coalesce(
                Sum('skills__daily_reviews_skill__time_spent'),
                Value(0),
                output_field=IntegerField()
            ),
            skills_count=Count("skills", distinct=True),
            finished_skills_count=Count(
                "skills",
                filter=Q(skills__status="finished"),
                distinct=True
            ),
            progress=Case(
                When(skills_count=0, then=Value(0)),
                default=ExpressionWrapper(
                    F("finished_skills_count") * 100 / F("skills_count"),
                    output_field=IntegerField()
                )
            )
        ).order_by("created_at")
    )
    paginator = Paginator(subgoals, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    for subgoal in page_obj:
        subgoal.preview_skills = subgoal.skills.all()[:3]
    context = {"page_obj": page_obj, "goal": goal}

    if request.htmx:
        return render(request, "cotton/partials/goal_details_page.html", context)
    return render(request, "tasks/goal_details.html", context)


@login_required
def subgoal_details(request, goal_id, subgoal_id):
    subgoal = get_object_or_404(
        SubGoal.objects.annotate(
            skills_count=Count("skills", distinct=True),
            finished_skills_count=Count(
                "skills",
                filter=Q(skills__status="finished"),
                distinct=True
            ),
            in_progress_skills_count=Count(
                "skills",
                filter=Q(skills__status="in_progress"),
                distinct=True
            ),
            pending_skills_count=Count(
                "skills",
                filter=Q(skills__status="pending"),
                distinct=True
            ),
            time_spent=Coalesce(
                Sum('skills__daily_reviews_skill__time_spent'),
                Value(0),
                output_field=IntegerField()
            ),
            progress = Case(
                When(skills_count=0, then=Value(0)),
                default=ExpressionWrapper(
                    F("finished_skills_count") * 100 / F("skills_count"),
                    output_field=IntegerField()
                )
            ),
            weekly_reviews_count=Count(
                "weekly_reviews_for_subgoal",
                distinct=True
            )
        ).prefetch_related(
            Prefetch(
                "skills",
                queryset=Skill.objects.annotate(
                    time_spent=Coalesce(
                        Sum("daily_reviews_skill__time_spent"),
                        Value(0),
                        output_field=IntegerField()
                    )
                )
            )
        ),
        id=subgoal_id,
        goal__id=goal_id,
        goal__user=request.user
    )

    skills = subgoal.skills.annotate(
        reviews_count=Count("daily_reviews_skill", distinct=True),
        time_spent=Coalesce(
            Sum("daily_reviews_skill__time_spent"),
            Value(0),
            output_field=IntegerField()
        )
    ).order_by("created_at")
    paginator = Paginator(skills, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    skills = page_obj
    context = {"subgoal": subgoal, "skills": skills}
    if request.htmx:
        return render(request, "cotton/partials/subgoal_details_page.html", context)
    return render(request, "tasks/subgoal_details.html", context)