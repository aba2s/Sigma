from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token


def register(request):
	# request.POST: return a QueryDict of form field values
	if request.method == 'POST':
		# Let's create a form instance from POST data
		form = RegisterForm(request.POST)
		print(form.is_valid())
		if form.is_valid():
			# save form in the memory not in database  
			user = form.save(commit=False)  
			user.is_active = False 
			user.save()
			# form.save()
			# Sending mail to activate the account
			activateEmail(request, user, form.cleaned_data.get('email'))
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
		if user is not None and user.is_active == False:
			messages.error(request, 'User is not yet activated by admin')
			return render(request, 'accounts/login.html')
		elif user is not None and user.is_active == True:
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

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('accounts/activate_account_email.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')
	
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('homepage')
    return redirect('login')