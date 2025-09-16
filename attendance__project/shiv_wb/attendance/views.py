from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Attendance
from django.contrib.auth.models import User

def signup_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		if password1 != password2:
			return render(request, 'attendance/signup.html', {'error': 'Passwords do not match'})
		if User.objects.filter(username=username).exists():
			return render(request, 'attendance/signup.html', {'error': 'Username already exists'})
		user = User.objects.create_user(username=username, password=password1)
		login(request, user)
		return redirect('mark_attendance')
	return render(request, 'attendance/signup.html')

def login_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('mark_attendance')
		else:
			return render(request, 'attendance/login.html', {'error': 'Invalid credentials'})
	return render(request, 'attendance/login.html')

def logout_view(request):
	logout(request)
	return redirect('login')

@login_required
def mark_attendance(request):
	if request.method == 'POST':
		status = request.POST.get('status')
		Attendance.objects.create(user=request.user, status=status)
		return redirect('view_attendance')
	return render(request, 'attendance/mark_attendance.html')

@login_required
def view_attendance(request):
	records = Attendance.objects.filter(user=request.user).order_by('-date')
	return render(request, 'attendance/view_attendance.html', {'records': records})
