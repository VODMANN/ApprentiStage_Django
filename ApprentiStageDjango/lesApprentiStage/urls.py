from django.urls import path
from . import  views
from django.contrib.auth.views import LogoutView

app_name = 'lesApprentiStage'

urlpatterns=[
  path('',views.home,name='home'),
  path('signup/', views.signup, name='signup'),
  path('recherche', views.pageRecherche, name='recherche'),
  path('login/', views.UserLoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(next_page='lesApprentiStage:home'), name='logout'),
]
