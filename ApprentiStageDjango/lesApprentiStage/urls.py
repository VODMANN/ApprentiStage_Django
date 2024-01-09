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
    path('update_mdp/', views.change_password, name='change_password'),
    path('validation_mdp/', views.change_password_success, name='change_password_success'),
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
    path('edit_enseignant/', views.edit_enseignant, name='edit_enseignant'),
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
    path('searcher/', views.liste_recherche, name='liste_recherche'),
    path('secretariat/contrats/', views.liste_contrats, name='liste_contrats'),
    path('secretariat/creer/contrats/', views.creer_contrat, name='creer_contrat'),
    path('secretariat/modifier/contrats/<int:pk>/', views.modifier_contrat, name='modifier_contrat'),
    path('secretariat/supprimer/contrats/<int:pk>/', views.supprimer_contrat, name='supprimer_contrat'),
    path('secretariat/creer/entreprise/', views.creer_entreprise, name='creer_entreprise'),
    path('secretariat/modifier/entreprise/<int:pk>/', views.modifier_entreprise, name='modifier_entreprise'),
    path('secretariat/supprimer/entreprise/<int:pk>/', views.delete_entreprise, name='supprimer_entreprise'),
    path('secretariat/creer/etudiant/', views.creer_etudiant, name='creer_etudiant'),
    path('secretariat/etudiant/modifier/<str:num_etu>/', views.modifier_etudiant, name='modifier_etudiant'),
    path('secretariat/etudiant/supprimer/<str:num_etu>/', views.delete_etudiant, name='supprimer_etudiant'),
    path('secretariat/enseignant/modifier/<str:num_harpege>/', views.modifier_enseignant, name='modifier_enseignant'),
    path('secretariat/enseignant/supprimer/<str:num_harpege>/', views.delete_enseignant, name='supprimer_enseignant'),
    path('secretariat/creer/promo/', views.PromoCreateView.as_view(), name='creer_promo'),
    path('secretariat/modifier/promo/<int:pk>/', views.PromoUpdateView.as_view(), name='modifier_promo'),
    path('secretariat/supprimer/promo/<int:pk>/', views.PromoDeleteView.as_view(), name='supprimer_promo'),
    path('secretariat/creer/departement/', views.DepartementCreateView.as_view(), name='creer_departement'),
    path('secretariat/modifier/departement/<int:pk>/', views.DepartementUpdateView.as_view(), name='modifier_departement'),
    path('secretariat/supprimer/departement/<int:pk>/', views.DepartementDeleteView.as_view(), name='supprimer_departement'),
    path('secretariat/creer/offre/', views.creer_offre, name='creer_offre'),
    path('secretariat/modifier/offre/<int:pk>/', views.OffreUpdateView.as_view(), name='modifier_offre'),
    path('secretariat/supprimer/offre/<int:pk>/', views.OffreDeleteView.as_view(), name='supprimer_offre'),
        # URL Soutenance Léo
    path('inscrire_soutenance/<int:soutenance_id>/', views.inscrire_soutenance, name='inscrire_soutenance'),
    path('desinscrire_soutenance/<int:soutenance_id>/', views.desinscrire_soutenance, name='desinscrire_soutenance'),
    path('nombre_soutenances/<str:num_harpege>/', views.NombreSoutenanceView.as_view(), name='nombre_soutenances'),        # URL pour les vues CRUD de Salle
    path('secretariat/creer/salle/', views.SalleCreateView.as_view(), name='creer_salle'),
    path('secretariat/modifier/salle/<int:pk>/', views.SalleUpdateView.as_view(), name='modifier_salle'),
    path('secretariat/supprimer/salle/<int:pk>/', views.SalleDeleteView.as_view(), name='supprimer_salle'),

    # URL pour les vues CRUD de Soutenance
    path('secretariat/creer/soutenance/', views.SoutenanceCreateView.as_view(), name='creer_soutenance'),
    path('secretariat/modifier/soutenance/<int:pk>/', views.SoutenanceUpdateView.as_view(), name='modifier_soutenance'),
    path('secretariat/supprimer/soutenance/<int:pk>/', views.SoutenanceDeleteView.as_view(), name='supprimer_soutenance'),

    # # URL pour les vues CRUD de Document
    path('secretariat/creer/document/', views.DocumentCreateView.as_view(), name='creer_document'),
    path('secretariat/modifier/document/<int:pk>/', views.DocumentUpdateView.as_view(), name='modifier_document'),
    path('secretariat/supprimer/document/<int:pk>/', views.DocumentDeleteView.as_view(), name='supprimer_document'),

    # URL pour les vues CRUD d'Evaluation
    path('secretariat/creer/evaluation/', views.EvaluationCreateView.as_view(), name='creer_evaluation'),
    path('secretariat/modifier/evaluation/<int:pk>/', views.EvaluationUpdateView.as_view(), name='modifier_evaluation'),
    path('secretariat/supprimer/evaluation/<int:pk>/', views.EvaluationDeleteView.as_view(), name='supprimer_evaluation'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
