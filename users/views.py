from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import User
from django.contrib import messages

# Create your views here.
@csrf_protect
def register(request):
    if request.method == 'POST':
        #passimsim reikšmesis iš formos
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['password2']
        if password1 == password2:
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, email=email, password=password1)
                return redirect('login')
            else:
                messages.error(request, 'Toks UserName jau egzistuoja, pasistenk būti orginalesniu :D')
                return redirect('register')
        else: 
            messages.error(request, 'Slaptažodžiai turėtų sutapti šiaip jau seni :)')
            return redirect('register')
        
    return render(request, 'registration/register.html')