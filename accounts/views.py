from django.contrib.auth.decorators import login_required
from employees.models import Attendance, Employee

@login_required
def dashboard(request):
    employee, created = Employee.objects.get_or_create(user=request.user)
    attendance_records = Attendance.objects.filter(employee=employee).order_by('-date')
    total_days = attendance_records.count()
    present_days = attendance_records.filter(status='Present').count()
    absent_days = attendance_records.filter(status='Absent').count()
    performance = (present_days / total_days * 100) if total_days > 0 else 0
    return render(request, 'dashboard.html', {
        'attendance_records': attendance_records,
        'present_days': present_days,
        'absent_days': absent_days,
        'total_days': total_days,
        'performance': performance,
    })
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # Skip validation and save user directly
        try:
            user = form.save(commit=True)
            login(request, user)
            messages.success(request, "Account created successfully")
            return redirect('attendance_list')
        except Exception as e:
            messages.error(request, f"Error: {e}")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
