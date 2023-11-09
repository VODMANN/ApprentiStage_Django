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
  path('search/', views.search, name='search'),
  path('ajout_stage/', views.ajouter_contrat, name='ajout_stage'),
  path('ajouter_entreprise_sansC/', views.ajouter_entrepriseSeul, name='ajouter_entreprise'),
  path('ajouter_entreprise/', views.ajouter_entreprise, name='ajouter_entreprise'),
  path('ajouter_theme/', views.ajouter_theme, name='ajouter_theme'),
  path('ajouter_responsable/<int:contrat_id>/', views.ajouter_responsable, name='ajouter_responsable'),
  path('details_etudiant/<str:etudiant_id>/', views.details_etudiant, name='details_etudiant'),
  path('details_entreprise/<str:entreprise_id>/', views.details_entreprise, name='details_entreprise'),
  path('affichage_contrat/<int:contrat_id>/', views.affichage_contrat, name='affichage_contrat'),
]
