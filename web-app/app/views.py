import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect

from .forms import RegistrationForm, LoginForm

class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'auth/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            url = 'http://127.0.0.2:8005/auth/register'
            data = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password'],
            }
            response = requests.post(url, json=data)
            if response.json()['status'] == 201:
                return HttpResponse('User registered successfully')
            else:
                return HttpResponse('Something went wrong')

        else:
            return render(request, 'auth/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            url = 'http://127.0.0.2:8005/auth/login'
            data = {
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password'],
            }
            response = requests.post(url, json=data)
            if response.json()['status'] == 200:
                access_token = response.json()['token']['access_token']
                response = redirect("users")
                response.set_cookie('access_token', access_token,  httponly=True)
                return response
            else:
                return HttpResponse('Something went wrong')

        return render(request, 'auth/login.html', {'form': form})

def user_list(request):
    access_token = request.COOKIES.get('access_token')
    if not access_token:
        return redirect('login')

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('http://127.0.0.2:8005/auth/verify', headers=headers)
    if response.status_code == 200:
        return HttpResponse('siz muvaffaqiyatli tizimga kirdingiz')
    elif response.status_code == 401:
        response = HttpResponseRedirect('/login/')
        response.delete_cookie('access_token')
        return response
    else:
        return HttpResponse('Something went wrong')




def user_detail(request, id):
    user = requests.get(f'http://127.0.0.2:8005/users/user/{id}').json()['detail']
    return render(request, 'user_detail.html', {'user': user})


def all_posts(request):
    posts = requests.get('http://127.0.0.2:8005/posts/').json()['posts']
    return render(request, 'post.html', {'posts': posts})
