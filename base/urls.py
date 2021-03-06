from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('login/', views.loginPage , name='login'),
    path('logout/', views.logoutUser , name='logout'),
    path('register/',views.registerUser , name='register'),

    path('', views.home, name='home'),
    path('room/<int:pk>', views.room, name='room'),
    path('profile/<str:pk>',views.userProfile , name='user-profile' ),

    path('create-room' , views.createRoom , name='create-room'),
    path('update-room/<int:pk>' , views.updateRoom , name='update-room'),
    path('delete-room/<int:pk>' , views.deleteRoom , name='delete-room'),
    path('delete-message/<int:pk>' , views.deleteMessage , name='delete-message'),


    path('updateuser/' , views.updateUser , name='update-user'),

]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

