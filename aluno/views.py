from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from .models import form_aluno

def login(request):
    if request.method != "POST":
        return render(request, 'aluno/login.html')

    usuario = request.POST.get('usuario')
    senha1 = request.POST.get('senha1')

    user = auth.authenticate(request, username=usuario, password=senha1)
    if not user:
        messages.add_message(messages.ERROR,'Usuario ou Senha invalido') 
        return render(request, 'aluno/login.html')
    else:
        auth.login(request,user)
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('dashboard')


def cadastrar(request):
    if request.method != "POST":
        return render(request, 'aluno/cadastrar.html')

    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    senha1 = request.POST.get('senha1')
    senha2 = request.POST.get('senha2')
    if not email or not usuario or not nome or not sobrenome or not senha1 or not senha2:
        messages.add_message(request, messages.WARNING,
                             'Todos os campos são obrigatórios')
        return render(request, 'aluno/cadastrar.html')

    try:
        validate_email(email)
    except:
        messages.add_message(request, messages.WARNING, 'Email invalido')
        return render(request, 'aluno/cadastrar.html')

    if len(senha1) < 6:
        messages.add_message(request, messages.WARNING,
                             'Senha deve ter no minimo 6 caracteres')
        return render(request, 'aluno/cadastrar.html')

    if senha1 != senha2:
        messages.add_message(request, messages.WARNING,
                             'Senhas são diferentes')
        return render(request, 'aluno/cadastrar.html')

    if User.objects.filter(username=usuario).exists():
        messages.add_message(request, messages.WARNING, 'Usuario ja existe')
        return render(request, 'aluno/cadastrar.html')

    if User.objects.filter(email=email).exists():
        messages.add_message(request, messages.WARNING, 'Email ja existe')
        return render(request, 'aluno/cadastrar.html')
    
    user = User.objects.create_user(
        username=usuario,
        email=email,
        first_name=nome,
        last_name=sobrenome,
        password=senha1
    )
    messages.add_message(request, messages.WARNING, 'Cadastrado com Sucesso')
    user.save()
    return redirect('login')

@login_required(redirect_field_name='login')

def dashboard(request):
    if request.method != 'POST':
        return render(request, 'aluno/dashboard.html')

    form = form_aluno(request.POST, request.FILES)
    if not form.is_valid():
        form = form_aluno(request.POST)
        return render(request,'aluno/dashboard.html')
    else:
        form.save()
        return render(request, 'aluno/dashboard.html')

def post(request):
    form = form_aluno()
    return render(request,'aluno/post_aluno.html', {'form':form})
