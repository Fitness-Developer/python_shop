from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Замените на вашу страницу логина
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})