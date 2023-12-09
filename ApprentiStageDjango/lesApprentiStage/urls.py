from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'lesApprentiStage'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('recherche', views.pageRecherche, name='recherche'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='lesApprentiStage:home'), name='logout'),
    path('search/', views.search, name='search'),
    path('ajout_stage/', views.ajouter_contrat, name='ajout_stage'),
    path('ajouter_entreprise_sansC/', views.ajouter_entrepriseSeul, name='ajouter_entreprise'),
    path('ajouter_entreprise/', views.ajouter_entreprise, name='ajouter_entreprise'),
    path('ajouter_theme/', views.ajouter_theme, name='ajouter_theme'),
    path('ajouter_offre/', views.ajouter_offre, name='ajouter_offre'),
    path('ajouter_responsable/<int:contrat_id>/', views.ajouter_responsable, name='ajouter_responsable'),
    path('details_etudiant/<str:etudiant_id>/', views.details_etudiant, name='details_etudiant'),
    path('details_entreprise/<str:entreprise_id>/', views.details_entreprise, name='details_entreprise'),
    path('affichage_contrat/<int:contrat_id>/', views.affichage_contrat, name='affichage_contrat'),
    path('secretariat/upload_csv/', views.upload_csv, name='upload_csv'),
    path('secretariat/validation_offre/', views.validation_offre, name='validation_offre'),
    path('secretariat/delete_offre/<int:pk>', views.delete_offre, name='delete_offre'),
    path('secretariat/valid_offre/<int:pk>', views.valid_offre, name='valid_offre'),
    path('soutenance/', views.soutenance, name='soutenance'),
    path('supprimerSoutenance/<id>', views.supprimerSoutenance, name='supprimerSoutenance'),
    path('modifierSoutenance/<id>', views.modifierSoutenance, name='modifierSoutenance'),
    path('inscrireSoutenance/<id>', views.inscrireSoutenance, name='inscrireSoutenance'),
    path('desinscrireSoutenance/<id>', views.desinscrireSoutenance, name='desinscrireSoutenance'),
    path('api/calendar_events/', views.calendar_events, name='calendar_events'),
    path('export_calendar/', views.export_calendar, name='export_calendar'),
    path('calendar_ens/', views.calendar_ens, name='calendar_ens'),
    path('offre/<int:offre_id>/', views.offre_detail, name='offre_detail'),
    path('etudiant/recherche_offres/', views.recherche_offres, name='recherche_offres'),
    path('etudiant/edit/', views.edit_etudiant, name='edit_etudiant'),
    path('etudiant/profil/', views.profile, name='profil_etudiant'),
    path('suivi_etudiants/', views.suivi_etudiants, name='suivi_etudiants'),
    path('insert/', views.insertion, name='insert'),
    path('generer_convention/<int:contrat_id>/', views.generer_convention_view, name='generer_convention_view'),
    path('contrats_non_valides/', views.contrats_non_valides, name='contrats_non_valides'),
    path('valider_contrat/<int:contrat_id>/', views.valider_contrat, name='valider_contrat'),
    path('refuser_contrat/<int:contrat_id>/', views.refuser_contrat, name='refuser_contrat'),
    path('upload_convention/', views.upload_convention, name='upload_convention'),
    path('liste_contrats_signes/', views.liste_contrats_signes, name='liste_contrats_signes'),
    path('telecharger_convention_secretaire/<int:document_id>/', views.telecharger_convention_secretaire, name='telecharger_convention_secretaire'),
    path('upload_convention_secretaire/', views.upload_convention_secretaire, name='upload_convention_secretaire'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
