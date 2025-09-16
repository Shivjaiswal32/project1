from django.urls import path
from .views import DashboardView, AttendanceListView, AttendanceCreateView, AttendanceUpdateView, AttendanceDeleteView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('attendance/', AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/add/', AttendanceCreateView.as_view(), name='attendance_create'),
    path('attendance/<int:pk>/edit/', AttendanceUpdateView.as_view(), name='attendance_update'),
    path('attendance/<int:pk>/delete/', AttendanceDeleteView.as_view(), name='attendance_delete'),
]
