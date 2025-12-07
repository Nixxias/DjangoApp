from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ArticleForm
from .models import Article, Profile
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group, User

def is_editor(user):
    return user.groups.filter(name='Editor').exists() or user.is_superuser
def role_required(allowed_roles):
    def decorator(view_func):
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            user_groups = [g.name.upper() for g in request.user.groups.all()]
            allowed_roles_upper = [r.upper() for r in allowed_roles]
            
            if request.user.is_superuser or any(role in user_groups for role in allowed_roles_upper):
                return view_func(request, *args, **kwargs)
                
            messages.error(request, "Brak uprawnień do tej sekcji.")
            return redirect('index') 
        return _wrapped
    return decorator
def is_admin(user):
    return user.groups.filter(name='Admin').exists() or user.is_superuser
def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'articles': articles})    
def index(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'articles': articles})
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            role = form.cleaned_data.get('role', 'Reader')
            user.profile.role = role.upper() 
            user.profile.save()

            group_name = role.capitalize() 
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
            
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Niepoprawne dane'})
    return render(request, 'login.html')
def logout_view(request):
    logout(request)
    return redirect('index')
@login_required
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user.is_authenticated:
        can_edit = is_editor(request.user) or is_admin(request.user)
        can_delete = is_admin(request.user)
    else:
        can_edit = False
        can_delete = False

    return render(request, 'article_detail.html', {
        'article': article,
        'can_edit': can_edit,
        'can_delete': can_delete
    })
@login_required
@role_required(['EDITOR', 'ADMIN'])
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, "Artykuł został dodany!")
            return redirect('index')
    else:
        form = ArticleForm()
    return render(request, 'create_article.html', {'form': form})
@login_required
@role_required(['EDITOR','ADMIN'])
def article_edit(request, pk): 
    """Tylko dla Editor i Admin."""
    article = get_object_or_404(Article, pk=pk)
    
    if not (is_editor(request.user) or is_admin(request.user)):
        messages.error(request, "Brak uprawnień do edycji.")
        return redirect('article_detail', pk=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Artykuł zaktualizowany.")
            return redirect('article_detail', pk=pk)
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'article_detail.html', {
        'form': form, 
        'article': article, 
        'edit_mode': True,  
        'can_delete': is_admin(request.user) 
    })
@login_required
@role_required(['ADMIN'])
def article_delete(request, pk):
    """Tylko dla Admin."""
    article = get_object_or_404(Article, pk=pk)
    
    if not is_admin(request.user):
        messages.error(request, "Tylko Administrator może usuwać artykuły.")
        return redirect('article_detail', pk=pk)

    if request.method == 'POST':
        article.delete()
        messages.success(request, "Artykuł usunięty.")
        return redirect('index')
    
    return render(request, 'delete_article.html', {'article': article})
