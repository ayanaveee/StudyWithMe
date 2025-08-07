from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Achievement, Note, Goal, StudyMaterialCategory, StudyMaterial, FavoriteMaterial
from django.utils.timezone import now
from .forms import  GoalForm
from django.views.decorators.http import require_POST
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


def study_materials_view(request):
    categories = StudyMaterialCategory.objects.prefetch_related('materials')
    return render(request, 'main/study_materials.html', {'categories': categories})


def study_material_detail(request, pk):
    material = get_object_or_404(StudyMaterial, pk=pk)
    return render(request, 'main/study_material_detail.html', {'material': material})


def index_view(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


@login_required
def goals_list(request):
    form = GoalForm()
    goals = Goal.objects.filter(user=request.user)

    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('goals')
        else:
            print(form.errors)
    else:
        form = GoalForm()

    return render(request, 'main/goals.html', {'form': form, 'goals': goals})


@login_required
def edit_goal(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)

    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('goals')
    else:
        form = GoalForm(instance=goal)

    return render(request, 'main/edit_goal.html', {'form': form, 'goal': goal})


@login_required
@require_POST
def mark_goal_completed(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    goal.is_completed = True
    goal.save()

    check_and_award_achievements(request.user)

    messages.success(request, "Цель отмечена как выполненная.")
    return redirect('goals')



@login_required
@require_POST
def delete_goal(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    goal.delete()
    messages.success(request, "Цель удалена.")
    return redirect('goals')



def achievements_view(request):
    user = request.user
    completed_goals_count = Goal.objects.filter(user=user, is_completed=True).count()
    user_level = completed_goals_count // 10 + 1
    progress_percent = (completed_goals_count % 10) * 10

    # Получаем достижения (если есть другие)
    all_achievements = Achievement.objects.filter(user=user).order_by('-date_earned')

    achievements_list = [{
        'title': ach.title,
        'description': ach.description,
        'date_earned': ach.date_earned,
        'unlocked': ach.date_earned is not None,
    } for ach in all_achievements]

    context = {
        'achievements': achievements_list,
        'user_level': user_level,
        'progress_percent': progress_percent,
        'completed_goals_count': completed_goals_count,
    }
    return render(request, 'main/achievements.html', context)


def check_and_award_achievements(user):
    # Проверяем, сколько целей выполнено
    completed_goals_count = Goal.objects.filter(user=user, is_completed=True).count()

    # Проверяем, есть ли уже достижение "Цель достигнута"
    achievement_code = 'goal_achievement'
    achievement = Achievement.objects.filter(user=user, code=achievement_code).first()

    if completed_goals_count > 0 and not achievement:
        Achievement.objects.create(
            user=user,
            code=achievement_code,
            title="Цель достигнута",
            description="Ты завершил одну из своих целей!",
            date_earned=now()
        )



def study_material_detail_view(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = FavoriteMaterial.objects.filter(user=request.user, material=material).exists()

    context = {
        'material': material,
        'is_favorited': is_favorited,
    }
    return render(request, 'main/study_material_detail.html', context)


@login_required
def favorite_materials_view(request):
    favorites = FavoriteMaterial.objects.filter(user=request.user).select_related('material')
    return render(request, 'main/favorite_list.html', {'favorites': favorites})


@login_required
def add_to_favorites(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)
    FavoriteMaterial.objects.get_or_create(user=request.user, material=material)
    return redirect('study_material_detail', material_id=material.id)


@login_required
def remove_favorite(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)
    favorite = FavoriteMaterial.objects.filter(user=request.user, material=material)
    if favorite.exists():
        favorite.delete()
        messages.success(request, f'Вы удалили из избранных материал: "{material.title}"')
    else:
        messages.warning(request, 'Материал не найден в избранных.')
    return redirect('favorite_materials')

@login_required
def favorite_material_detail_view(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)
    return render(request, 'main/favorite_material_detail.html', {'material': material})
