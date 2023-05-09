from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout


def register(request):
	if request.method == 'POST':
		# Let's create a form instance from POST data
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password1 = form.cleaned_data.get("password1")
			password2 = form.cleaned_data.get("password2")
			if password1 and password2 and password1 != password2:
				raise form.ValidationError(
					form.error_messages['password_mismatch'],
					code='password_mismatch',
				)
	
			messages.success(request, 'Account was created for', username)
			return redirect('login')
		else:
			messages.error(request, 'echec')
			return render(request, 'registration/register.html')
	else:
		form = RegisterForm()
		context = {
			'form': form
		}
		return render(request, 'registration/register.html', context )

def login_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
			# return redirect('user_insertion_orders', pk=request.user.id)
		else:
			messages.error(request, 'Your login is wrong')
			return render(request, 'registration/login.html')
	context={}
	return render(request, 'registration/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')