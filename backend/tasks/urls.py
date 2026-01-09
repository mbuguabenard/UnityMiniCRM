from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyViewSet, ContactViewSet, DealViewSet, TaskViewSet,
    login_view, logout_view, dashboard_stats, profile_view, signup_view
)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'deals', DealViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('auth/login/', login_view, name='login'),
    path('auth/signup/', signup_view, name='signup'),
    path('auth/logout/', logout_view, name='logout'),
    path('dashboard/stats/', dashboard_stats, name='dashboard_stats'),
    path('profile/', profile_view, name='profile'),
    path('', include(router.urls)),
]
