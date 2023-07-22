from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q


def register(request):
	# request.POST: return a QueryDict of form field values
	if request.method == 'POST':
		# Let's create a form instance from POST data
		form = RegisterForm(request.POST)
		print(form.is_valid())
		if form.is_valid():
			form.save()	
			username = form.cleaned_data.get('username')
			msg = "An account was created for {}".format(username)
			messages.success(request, msg)
			return redirect('login')
		else:
			data = request.POST.dict() # form fields value
			user = User.objects.filter(
				Q(username=data['username']) | Q(email=data['email']))
			# If the user already exists
			if user.exists():
				# Check if username or email adress has already been taken
				try:
					username = user[0].username
					email = user[0].email
				except Exception as e:
					# Check if email has already been taken
					messages.error(request, e)
					return redirect('register')	
				else:
					if username:
						msg = "Username <{}> already exists.".format(
							username
						)
						messages.error(request, msg)
						return redirect('register')
					if email:
						msg = "Email <{}> already exists.".format(
							username
						)
						messages.error(request, msg)
			# If passwords didn't match
			elif data['password1'] != data['password2']:
				msg = "Passwords do NOT match."
				messages.error(request, msg)
				return redirect('register')
			# if any others trouble		
			else:
				print(request.POST)
				msg2 = "Password cant'be a commonly used password."
				msg3 = "Password can't be entirely numeric"
				msg4 = "Password can't be too similar to your other personal."
				# To have each message in separate li balise:
				messages.error(request, msg2)
				messages.error(request, msg3)
				messages.error(request, msg4)
				return redirect('register')
	else:
		form = RegisterForm()
		context = {
			'form': form
		}
		return render(request, 'accounts/register.html', context )

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
			return render(request, 'accounts/login.html')
	context={}
	return render(request, 'accounts/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')