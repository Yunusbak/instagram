import requests
from django.shortcuts import render


def user_list(request):
    users = requests.get('http://127.0.0.1:8000/users/').json()['users']
    return render(request, 'user.html', {'users': users})



def user_detail(request, id):
    user = requests.get(f'http://127.0.0.1:8000/users/user/{id}/').json()['detail']
    return render(request, 'user_detail.html', {'user': user})