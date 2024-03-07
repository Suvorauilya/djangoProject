from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import AvatarForm
from .models import UserProfile

from e1.models import ModelReg


@csrf_exempt
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # или куда-то еще
    else:
        form = AvatarForm(instance=user_profile)

    return render(request, 'profile.html', {'form': form})


@csrf_exempt
def index(request):
    if request.method == 'POST': pass
    return render(request, '../../djangoProject/templates/index.html')


user_info = {"": False}


@csrf_exempt
def registration(request):
    if request.method == 'POST':
        data = ModelReg.objects.all()
        for i in data:
            if request.POST['email'] == i.email:
                return render(request, '../../djangoProject/templates/index.html',
                              {"err": f'Email: {i.email} занят другим пользователем'})
        reg = ModelReg()
        reg.email = request.POST['email']
        reg.password = request.POST['password']
        reg.login = request.POST['login']
        reg.save()
        return HttpResponse(f'Пользователь с Email: {reg.email} успешно зарегистрирован!')
    return render(request, '../../djangoProject/templates/registration.html')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = ModelReg.objects.all()
        print(data)
        print(f"Из пост запроса. Почта: {request.POST['email']} Pass: {request.POST['password']}")
        for i in data:
            print(f'Текущий объект из базы данных. Почта: {i.email} Pass: {i.password}')
            if request.POST['email'] == i.email and request.POST['password'] == i.password:
                user_login = request.POST['email']
                user_info[user_login] = True
                html = redirect('/profile', {'user': user_login})
                html.set_cookie('isAuth', user_login)
                return html

        return render(request, '../../djangoProject/templates/index.html', {'err': 'авторизация не пройдена'})
    return render(request, '../../djangoProject/templates/login.html')


@csrf_exempt
def profile(request):
    if request.method == 'POST':
        html = redirect('/')
        html.delete_cookie('isAuth')
        return html
    r = ''
    try:
        r = request.COOKIES['isAuth']
    except:
        return redirect('/')
    return render(request, '../../djangoProject/templates/profile.html', {'user': request.COOKIES['isAuth']})
