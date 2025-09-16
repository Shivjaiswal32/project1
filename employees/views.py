from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Attendance, Employee
from .forms import AttendanceForm

# ----------------------
# DASHBOARD VIEW
# ----------------------
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_superuser:
            records = Attendance.objects.all().order_by('-date')
        else:
            employee, created = Employee.objects.get_or_create(user=self.request.user)
            records = Attendance.objects.filter(employee=employee).order_by('-date')

        # Attendance Summary
        total_days = records.count()
        present_days = records.filter(status='Present').count()
        absent_days = records.filter(status='Absent').count()
        performance = (present_days / total_days * 100) if total_days > 0 else 0

        context.update({
            'attendance_records': records,
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': absent_days,
            'performance': performance,
        })
        return context


# ----------------------
# LIST VIEW
# ----------------------
class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'employees/attendance_list.html'
    context_object_name = 'records'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Attendance.objects.all().order_by('-date')
        else:
            employee, created = Employee.objects.get_or_create(user=self.request.user)
            return Attendance.objects.filter(employee=employee).order_by('-date')


# ----------------------
# CREATE VIEW
# ----------------------
class AttendanceCreateView(LoginRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'employees/attendance_form.html'
    success_url = reverse_lazy('dashboard')   # ✅ redirect to dashboard, not list

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if self.request.user.is_superuser:
            employee = form.cleaned_data.get('employee')
        else:
            employee, created = Employee.objects.get_or_create(user=self.request.user)
        form.instance.employee = employee
        return super().form_valid(form)


# ----------------------
# UPDATE VIEW
# ----------------------
class AttendanceUpdateView(LoginRequiredMixin, UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'employees/attendance_form.html'
    success_url = reverse_lazy('dashboard')   # ✅ redirect to dashboard

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Attendance.objects.all()
        else:
            employee, created = Employee.objects.get_or_create(user=self.request.user)
            return Attendance.objects.filter(employee=employee)


# ----------------------
# DELETE VIEW
# ----------------------
class AttendanceDeleteView(LoginRequiredMixin, DeleteView):
    model = Attendance
    template_name = 'employees/attendance_confirm_delete.html'
    success_url = reverse_lazy('dashboard')   # ✅ redirect to dashboard

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Attendance.objects.all()
        else:
            employee, created = Employee.objects.get_or_create(user=self.request.user)
            return Attendance.objects.filter(employee=employee)
