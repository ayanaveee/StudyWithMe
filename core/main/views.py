from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Achievement, StudySession, Note, Goal, StudyMaterialCategory, StudyMaterial, FavoriteMaterial
from django.utils.timezone import now
from .forms import  GoalForm
from .forms import StudySessionForm

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
def sessions_view(request):
    return render(request, 'main/sessions.html')

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
def achievements_view(request):
    user = request.user
    all_achievements = Achievement.objects.filter(user=user).order_by('-date_earned')
    unlocked_count = all_achievements.filter(date_earned__isnull=False).count()
    user_level = unlocked_count // 10 + 1
    progress_percent = (unlocked_count % 10) * 10

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
    }
    return render(request, 'main/achievements.html', context)

def check_and_award_achievement(user):
    goals_count = Goal.objects.filter(user=user).count()
    if goals_count >= 5:
        achievement, created = Achievement.objects.get_or_create(
            user=user,
            title="Пять целей",
            defaults={'description': 'Добавлено 5 целей', 'date_earned': timezone.now()}
        )
        if created:
            achievement.date_earned = timezone.now()
            achievement.save()

@login_required
def create_session(request):
    if request.method == 'POST':
        form = StudySessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            check_and_award_achievements(request.user)
            return redirect('sessions')
    else:
        form = StudySessionForm()
    return render(request, 'main/create_session.html', {'form': form})

def check_and_award_achievements(user):
    unlocked = Achievement.objects.filter(user=user).values_list('title', flat=True)
    if StudySession.objects.filter(user=user).count() >= 1 and "Первое занятие" not in unlocked:
        Achievement.objects.create(user=user, title="Первое занятие", description="Ты начал учиться!")
    dates = StudySession.objects.filter(user=user).values_list('date', flat=True).distinct()
    dates = sorted(set(dates))
    streak = 1
    for i in range(1, len(dates)):
        if (dates[i] - dates[i-1]).days == 1:
            streak += 1
        else:
            streak = 1
        if streak >= 7 and "7 дней подряд" not in unlocked:
            Achievement.objects.create(user=user, title="7 дней подряд", description="Ты учился 7 дней без перерыва!")
            break
    if Note.objects.filter(user=user).count() >= 5 and "5 заметок" not in unlocked:
        Achievement.objects.create(user=user, title="5 заметок", description="Ты создал 5 заметок!")
    goals = Goal.objects.filter(user=user, end_date__lt=now().date())
    if goals.exists() and "Цель достигнута" not in unlocked:
        Achievement.objects.create(user=user, title="Цель достигнута", description="Ты завершил одну из своих целей!")

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
    FavoriteMaterial.objects.filter(user=request.user, material=material).delete()
    return redirect('favorite_list')