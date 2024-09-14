import requests
from django.contrib import messages
from django.shortcuts import render, redirect


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        response = requests.post('http://127.0.0.2:8000/auth/register', json={
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'username': username,
            'password': password
        })
        if response.status_code == 200:
            messages.success(request, f'Account created for {first_name} {last_name}!')
            return redirect('login')

        else:
            messages.error(request, f'Something went wrong. Please try again!')


    return render(request, 'auth/register.html')



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        response = requests.post('http://127.0.0.2:8000/auth/login', json={
            'username': username,
            'password': password
        })
        if response.status_code == 200:
            data = response.json()
            access_token = data['token']['access_token']
            refresh_token = data['token']['refresh_token']
            request.session['access_token'] = access_token
            request.session['refresh_token'] = refresh_token
            messages.success(request, f'You are now logged in!')
            return redirect('user-list')

        else:
            messages.error(request, f'Something went wrong. Please try again!')
            return redirect('login')

    return render(request, 'auth/login.html')


def base(request):
    return render(request, 'base.html')


def user_list(request):
    users = requests.get('http://127.0.0.2:8005/users/').json()['users']
    return render(request, 'user.html', {'users': users})



def user_detail(request, id):
    user = requests.get(f'http://127.0.0.2:8005/users/user/{id}').json()['detail']
    return render(request, 'user_detail.html', {'user': user})


def all_posts(request):
    posts = requests.get('http://127.0.0.2:8005/posts/').json()['posts']
    return render(request, 'post.html', {'posts': posts})
