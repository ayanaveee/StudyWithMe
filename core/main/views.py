from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Achievement, StudySession, Note, Goal, StudyMaterialCategory, StudyMaterial
from django.utils.timezone import now
from .forms import StudySessionForm

def study_materials(request):
    categories = StudyMaterialCategory.objects.all().prefetch_related('study_material_set')
    return render(request, 'main/study_materials.html', {'categories': categories})

def study_material_detail(request, pk):
    material = get_object_or_404(StudyMaterial, pk=pk)
    return render(request, 'main/study_material_detail.html', {'material': material})

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def sessions(request):
    return render(request, 'main/sessions.html')

def goals(request):
    return render(request, 'main/goals.html')

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
