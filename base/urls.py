from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('chat/<str:pk>/', views.chat, name="chat"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    # test updateroom
    # path('update-room-new/<str:pk>/', views.updateRoomNew, name="update-room-new"),
    # test updateroom end
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-follower/<str:pku>/<str:pkr>/',views.deleteFollower, name="delete-follower"),
    path('addhost/<str:pku>/<str:pkr>/',views.addHost, name="addhost"),
    path('unhost/<str:pku>/<str:pkr>/',views.unHost, name="unhost"),
    path('unfollow-room/<str:pku>/<str:pkr>/',
         views.unfollowRoom, name="unfollow-room"),
    path('add-follower/<str:pku>/<str:pkr>/',
         views.addFollower, name="add-follower"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('delete-chatmessage/<str:pk>/',
         views.deleteChatMessage, name="delete-chatmessage"),
    path('update-user/', views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    path('follow/', views.follow, name="follow"),
    path('chats/', views.chats, name="chats"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='base/password_reset.html'), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='base/password_reset_sent.html'),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='base/password_reset_form.html'),
         name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='base/password_reset_done.html'),
         name="password_reset_complete"),

]
