from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'lesApprentiStage'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('recherche', views.pageRecherche, name='recherche'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='lesApprentiStage:home'), name='logout'),
    path('search/', views.search, name='search'),
    path('soutenance/', views.soutenance, name='soutenance'),
    path('supprimerSoutenance/<id>', views.supprimerSoutenance, name='supprimerSoutenance'),
    path('modifierSoutenance/<id>', views.modifierSoutenance, name='modifierSoutenance'),
    path('inscrireSoutenance/<id>', views.inscrireSoutenance, name='inscrireSoutenance'),
    path('desinscrireSoutenance/<id>', views.desinscrireSoutenance, name='desinscrireSoutenance'),
    path('api/calendar_events/', views.calendar_events, name='calendar_events'),
    path('export_calendar/', views.export_calendar, name='export_calendar'),
    path('calendar_ens/', views.calendar_ens, name='calendar_ens'),
    path('ajout_stage/', views.ajouter_contrat, name='ajout_stage'),
    path('ajouter_entreprise_sansC/', views.ajouter_entrepriseSeul, name='ajouter_entreprise'),
    path('ajouter_entreprise/', views.ajouter_entreprise, name='ajouter_entreprise'),
    path('ajouter_theme/', views.ajouter_theme, name='ajouter_theme'),
    path('ajouter_responsable/<int:contrat_id>/', views.ajouter_responsable, name='ajouter_responsable'),
    path('offre/<int:offre_id>/', views.offre_detail, name='offre_detail'),
    path('etudiant/recherche_offres/', views.recherche_offres, name='recherche_offres'),
    path('etudiant/edit/', views.edit_etudiant, name='edit_etudiant'),
    path('etudiant/profil/', views.profile, name='profil_etudiant'),
]
