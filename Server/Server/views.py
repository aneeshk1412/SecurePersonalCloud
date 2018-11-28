from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


def homepage(request):
    return render(request, 'homepage.html')
    # return HttpResponse('homepage')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # log the user in
            login(request, user)
            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log in the user
            user = form.get_user()
            if not request.user.is_authenticated:
                login(request, user)
                return redirect('user:userhome', username=request.user)
            if request.user != user:
                return render(request, 'invalid.html')
            if request.user == user:
                return redirect('homepage')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'logout.html')
    else:
        logout(request)
        return render(request, 'logout.html')
