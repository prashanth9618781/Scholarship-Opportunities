<<<<<<< HEAD
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
# main url routes developments 
from application.views import CustomTokenObtainPairView,ScholarshipCreateView,ScholarshipUpdateView,UserModelViewSet

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'register',UserModelViewSet)
from application import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/',CustomTokenObtainPairView.as_view(),name='get_token'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='refresh_token'),
    #main path developments 
    path('api/', include(router.urls)),
    
    path('api/scholarships/<int:pk>/', ScholarshipUpdateView.as_view(), name='scholarship-update'),
    path('api/scholarships/create/',ScholarshipCreateView.as_view(), name='create-scholarship'),

    path('api/scholarships/apply/<int:scholarship_id>/', views.apply_scholarship, name='apply_scholarship'),
    path('api/scholarships/all-applications/',views. all_applications, name='all_applications'),
    path('api/scholarships/update-status/<int:pk>/', views.update_application_status, name='update_application_status'),

    path('api/scholarships/',views.ScholarshipListView.as_view(), name='scholarship-list'),
    path('api/scholarships/create/',ScholarshipCreateView.as_view(), name='create-scholarship'),
    path('api/scholarships/my-applications/',views.my_applications, name='my_applications'),

=======
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
# main url routes developments 
from application.views import CustomTokenObtainPairView,ScholarshipCreateView,ScholarshipUpdateView,UserModelViewSet

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'register',UserModelViewSet)
from application import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/',CustomTokenObtainPairView.as_view(),name='get_token'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='refresh_token'),
    #main path developments 
    path('api/', include(router.urls)),
    
    path('api/scholarships/<int:pk>/', ScholarshipUpdateView.as_view(), name='scholarship-update'),
    path('api/scholarships/create/',ScholarshipCreateView.as_view(), name='create-scholarship'),

    path('api/scholarships/apply/<int:scholarship_id>/', views.apply_scholarship, name='apply_scholarship'),
    path('api/scholarships/all-applications/',views. all_applications, name='all_applications'),
    path('api/scholarships/update-status/<int:pk>/', views.update_application_status, name='update_application_status'),

    path('api/scholarships/',views.ScholarshipListView.as_view(), name='scholarship-list'),
    path('api/scholarships/create/',ScholarshipCreateView.as_view(), name='create-scholarship'),
    path('api/scholarships/my-applications/',views.my_applications, name='my_applications'),

>>>>>>> ce448217a3e986c12530c8704b3356fc81cc687d
]