from django.shortcuts import render
from Crypto.Cipher import AES
from .models import Pass_info, Crypto
from .forms import PassForm, RegForm, AuthForm
from django.db import IntegrityError
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def index(request):
    return render(request, 'passes/index.html')

def add_info(request):
    if request.method == 'POST':
        form = PassForm(request.POST)
        if form.is_valid():
            sourceb = bytes(form.cleaned_data['source_text'], 'utf-8')
            cipher = AES.new(settings.AES_KEY, AES.MODE_EAX)
            s_nonce=cipher.nonce
            source, s_tag = cipher.encrypt_and_digest(sourceb)

            loginb = bytes(form.cleaned_data['login_text'], 'utf-8')
            cipher = AES.new(settings.AES_KEY, AES.MODE_EAX)
            l_nonce=cipher.nonce
            login, l_tag = cipher.encrypt_and_digest(loginb)

            passwordb = bytes(form.cleaned_data['password_text'], 'utf-8')
            cipher = AES.new(settings.AES_KEY, AES.MODE_EAX)
            p_nonce=cipher.nonce
            password, p_tag = cipher.encrypt_and_digest(passwordb)

            cr = Crypto(
                tag_s = s_tag,
                nonce_s = s_nonce,
                tag_l = l_tag,
                nonce_l = l_nonce,
                tag_p = p_tag,
                nonce_p = p_nonce,
                cr_date = timezone.now())
            cr.save()

            us = Pass_info(
                source_text = source,
                login_text = login,
                password_text = password,
                crypto=Crypto.objects.latest("cr_date"))
            us.save()
            return render(request, 'passes/success.html')
    else:
        form = PassForm()
    return render(request, 'passes/add_info.html', {'form':form})

def get_info(request):
    q=Pass_info.objects.get(id=1)
    c=Crypto.objects.get(id=q.crypto_id)

    cipher = AES.new(settings.AES_KEY, AES.MODE_EAX, nonce=c.nonce_s)
    source = cipher.decrypt(q.source_text)
    try:
        cipher.verify(c.tag_s)
        source_r=source
    except ValueError:
        sorce_r='error'

    cipher = AES.new(settings.AES_KEY, AES.MODE_EAX, nonce=c.nonce_l)
    login = cipher.decrypt(q.login_text)
    try:
        cipher.verify(c.tag_l)
        login_r=login
    except ValueError:
        login_r='error'

    cipher = AES.new(settings.AES_KEY, AES.MODE_EAX, nonce=c.nonce_p)
    password = cipher.decrypt(q.password_text)
    try:
        cipher.verify(c.tag_p)
        password_r=password
    except ValueError:
        password_r='error'

    return render(request, 'passes/get_info.html', {'source':source_r,
                                                    'password':password_r,
                                                    'login':login_r})
def reg(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            if password==password2:
                try:
                    user = User.objects.create_user(login, email, password)
                    user.save()
                except IntegrityError:
                    return render(request, 'passes/reg.html', {'form':form,
                                               'errormsg':"Указанный пользователь уже существует!"})
                return render(request, 'passes/success.html')
            else:
                return render(request, 'passes/reg.html', {'form':form,
                                               'errormsg':"Пароли не совпадают! Попробуйте еще раз"})
    else:
        form = RegForm()
    return render(request, 'passes/reg.html', {'form':form,
                                               'errormsg':""})

def success(request):
    return render(request, 'passes/success.html')

def auth(request):
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=login, password=password)
            if user is not None:
                if user.is_active:
                    return render(request, 'passes/success.html')
                else:
                    return render(request, 'passes/auth.html', {'form':form,
                                                'errormsg':"Введенные данные верны, но пользователь не активен на данный момент"})
            else:
                return render(request, 'passes/auth.html', {'form':form,
                                                'errormsg':"Введенные данные неверны"})
    else:
        form = AuthForm()
    return render(request, 'passes/auth.html', {'form':form,
                                                'errormsg':""})
# Create your views here.














