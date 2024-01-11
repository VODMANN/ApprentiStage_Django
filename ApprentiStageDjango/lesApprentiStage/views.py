from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.views.generic import *
from .utils import *

from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import redirect_to_login

from .models import *
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta, timezone  
from icalendar import Calendar, Event
import csv
from django.contrib.auth.hashers import make_password
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django_filters import FilterSet, CharFilter
from .filters import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

def insertion(request):
    return insert(request)


def user_type_and_role_required(allowed_user_types,role=[]):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return redirect_to_login(request.get_full_path())

            user_type = user.get_user_type()
            if user_type not in allowed_user_types:
                return HttpResponseForbidden('Vous n\'avez pas les droits nécessaires pour accéder à cette page.')

            if user_type == 'enseignant':
                enseignant_profile = user.profilenseignant
                if enseignant_profile.roleEnseignant not in role:
                    return HttpResponseForbidden('Vous n\'avez pas les droits nécessaires pour accéder à cette page.')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator



class UserLoginView(LoginView):
    template_name = 'registration/login.html'


from .models import NombreSoutenances

def home(request):
    offre_list = Offre.objects.all()   
    user = request.user

    if request.user.is_authenticated:
        user_type = request.user.type_utilisateur
        print(user_type)

        if user_type == 'etudiant':
            offre_list = Offre.objects.filter(estPublie=1)
            return render(request, 'etudiant/accueil_etu.html', {'offre_list': offre_list})

        if user_type == 'secretaire':
            offre_list = Offre.objects.all().order_by('-pk')
            return render(request, 'secretariat/accueil_sec.html', {'offre_list': offre_list})

        if user_type == 'enseignant':
            is_responsible = user.profilenseignant.roleEnseignant in ['chef_departement', 'enseignant_promo']

            # Ajoutez le code pour obtenir le nombre de soutenances par promo pour cet enseignant.
            soutenances_par_promo = NombreSoutenances.objects.filter(enseignant=user.profilenseignant)

            return render(request, 'enseignant/accueil_ens.html', {
                'user': user,
                'is_responsible': is_responsible,
                'soutenances_par_promo': soutenances_par_promo
            })

    return render(request, 'pages/accueil.html')


def validation_offre(request):
    offre_list = Offre.objects.all().order_by('-pk')
    return render(request, 'secretariat/validation_offre.html', {'offre_list': offre_list})


@user_type_and_role_required(['enseignant','secretaire'], [ProfilEnseignant.CHEF_DEPARTEMENT])
def signup(request):
    promos = Promo.objects.all()  
    if request.method == 'POST':
        user_form = UtilisateurForm(request.POST)
        etudiant_form = EtudiantForm(request.POST)
        enseignant_form = EnseignantForm(request.POST)
        secretaire_form = SecretaireForm(request.POST)


        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user_type = user_form.cleaned_data['type_utilisateur']  
            if user_type == 'etudiant' and etudiant_form.is_valid():
                user.save()
                etudiant = etudiant_form.save(commit=False)
                etudiant.utilisateur = user
                etudiant.save()
                subject = "Bienvenue sur Notre Site"
                template = f'mail/register_valid.html'
                context = {
                    'date': datetime.today().date(),
                    'username': user.username,
                    'email': etudiant.mailEtu
                }
                receivers = [etudiant.mailEtu]
                send_email_with_html_body(
                subjet=subject,
                receivers=receivers,
                template=template,
                context=context
            )
                return redirect('lesApprentiStage:home')
            elif user_type == 'enseignant' and enseignant_form.is_valid():
                user.save()
                enseignant = enseignant_form.save(commit=False)
                enseignant.utilisateur = user
                enseignant.save()

                if enseignant.roleEnseignant == ProfilEnseignant.CHEF_DEPARTEMENT:
                    selected_departement = enseignant_form.cleaned_data.get('departements')
                    if selected_departement:
                        selected_departement.chef = enseignant
                        selected_departement.save()

                selected_promos = enseignant_form.cleaned_data.get('promos')
                for promo in selected_promos:
                    EnseignantPromo.objects.create(enseignant=enseignant, promo=promo)
                subject = "Bienvenue sur Notre Site"
                template = f'mail/register_valid.html'
                context = {
                    'date': datetime.today().date(),
                    'username': user.username,
                    'email': enseignant.mailEnseignant
                }
                receivers = [enseignant.mailEnseignant]
                send_email_with_html_body(
                subjet=subject,
                receivers=receivers,
                template=template,
                context=context
            )
                return redirect('lesApprentiStage:home')
            
            elif user_type == 'secretaire' and secretaire_form.is_valid():
                user.save()
                secretaire = secretaire_form.save(commit=False)
                secretaire.utilisateur = user
                secretaire.save()
                return redirect('lesApprentiStage:home')
    else:
        user_form = UtilisateurForm(request.POST)
        etudiant_form = EtudiantForm()
        enseignant_form = EnseignantForm()
        secretaire_form = SecretaireForm()

    if not user_form.is_valid():
        print('Erreurs dans le formulaire UtilisateurForm:', user_form.errors)


    return render(request, 'registration/signup.html', {
        'user_form': user_form,
        'etudiant_form': etudiant_form,
        'enseignant_form': enseignant_form,
        'secretaire_form': secretaire_form,
        'promos': promos,
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important pour garder l'utilisateur connecté
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})

def change_password_success(request):
    return render(request, 'registration/change_password_success.html')


@login_required
@user_type_and_role_required(['secretaire'])
def pageRecherche(request):
    return render(request, 'pages/recherche.html')


@login_required
@user_type_and_role_required(['secretaire'])
def search(request):
    query = request.GET.get('query', '')
    search_type = request.GET.get('type', '')
    promo_filter = request.GET.get('promo', '')

    search_mapping = {
        'ETUDIANT': (ProfilEtudiant, ['civiliteEtu', 'nomEtu', 'prenomEtu', 'numEtu', 'adresseEtu', 'cpEtu', 'villeEtu', 'telEtu', 'promo__annee', 'idDepartement__nomDep']),
        'ENTREPRISE': (Entreprise, ['nomEnt', 'numSiret', 'adresseEnt', 'cpEnt', 'villeEnt', 'responsable__nomResp', 'responsable__prenomResp', 'responsable__emailResp']),
        'CONTRAT': (Contrat, ['type', 'description', 'etat', 'dateDeb', 'dateFin', 'etudiant__civiliteEtu', 'etudiant__nomEtu', 'etudiant__prenomEtu', 'etudiant__numEtu', 'entreprise__nomEnt', 'entreprise__adresseEnt', 'entreprise__cpEnt', 'entreprise__villeEnt']),
    }

    results = []
    if search_type in search_mapping:
        model, fields = search_mapping[search_type]
        query_objects = Q()
        for field in fields:
            if field == 'promo__annee' and promo_filter:
                query_objects |= Q(**{f'{field}__icontains': promo_filter})
            else:
                query_objects |= Q(**{f'{field}__icontains': query})

        results = model.objects.filter(query_objects).values(*fields)

    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        data = list(results)
        return JsonResponse(data, safe=False)

    promotions = Promo.objects.all()
    return render(request, 'pages/recherche.html', {"results": results, "search_type": search_type, "promotions": promotions})

@login_required
@user_type_and_role_required(['secretaire'])
def contrats_non_valides(request):
    contrats_non_valides = Contrat.objects.filter(estValide__isnull=True)

    return render(request, 'secretariat/contrats_non_valides.html', {'contrats_non_valides': contrats_non_valides})

@login_required
@user_type_and_role_required(['secretaire'])
def valider_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, pk=contrat_id)
    contrat.estValide = True
    contrat.etat = 0
    contrat.save()
    return redirect('lesApprentiStage:contrats_non_valides')

@login_required
@user_type_and_role_required(['secretaire'])
def refuser_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, pk=contrat_id)
    contrat.estValide = False
    contrat.save()
    return redirect('lesApprentiStage:contrats_non_valides')

@login_required
def upload_convention(request):
    if request.method == 'POST':
        contrat_id = request.POST.get('contrat_id')
        fichier_upload = request.FILES.get('fichier')

        if fichier_upload:
            contrat = get_object_or_404(Contrat, pk=contrat_id)
            etudiant_email = contrat.etudiant.mailEtu
            document, created = Document.objects.update_or_create(
                contrat=contrat,
                defaults={'fichier': fichier_upload, 'titre': fichier_upload.name}
            )
            contrat.etat = 1
            contrat.save()

            sujet = "Nouvelle Convention Téléversée"
            message = "Une nouvelle convention a été téléversée et nécessite votre attention."
            destinataire = ['rochdi53sami@gmail.com']

            send_mail(sujet, message, 'samidevtest53@gmail.com', destinataire)
            return HttpResponse("Fichier uploadé avec succès !")
        else:
            return HttpResponse("Aucun fichier fourni.", status=400)

    return HttpResponse("Requête invalide.", status=400)


def liste_recherche(request):
    filters = {
        'contrat_filter': ContratFilter(request.GET, queryset=Contrat.objects.all()),
        'etudiant_filter': ProfilEtudiantFilter(request.GET, queryset=ProfilEtudiant.objects.all()),
        'entreprise_filter': EntrepriseFilter(request.GET, queryset=Entreprise.objects.all()),
        'enseignant_filter': ProfilEnseignantFilter(request.GET, queryset=ProfilEnseignant.objects.all()),
        'promo_filter': PromoFilter(request.GET, queryset=Promo.objects.all()),
        'departements_filter': DepartementFilter(request.GET, queryset=Departement.objects.all()),
        'offre_filter': OffreFilter(request.GET, queryset=Offre.objects.all()),
        'salle_filter': SalleFilter(request.GET, queryset=Salle.objects.all()),
        'soutenance_filter': SoutenanceFilter(request.GET, queryset=Soutenance.objects.all()),
        'document_filter': DocumentFilter(request.GET, queryset=Document.objects.all()),
        'evaluation_filter': EvaluationFilter(request.GET, queryset=Evaluation.objects.all()),
    }

    selected_filter = request.GET.get('selected_filter')

    # Ajout des filtres au contexte
    context = {
        'filters': filters,
        'selected_filter': selected_filter,
    }

    return render(request, 'secretariat/crud_master.html', context)



def liste_contrats(request):
    contrats = Contrat.objects.all()
    contrat_filter = ContratFilter(request.GET, queryset=contrats)
    context = {
        'contrat_filter': contrat_filter,
    }
    return render(request, 'secretariat/contrats/liste_contrats.html', context)

# Création d'un nouveau contrat
def creer_contrat(request):
    if request.method == 'POST':
        form = ContratForm(request.POST)
        if form.is_valid():
            form.save()
            url_sans_fragment = reverse('lesApprentiStage:liste_recherche')
            nouvelle_url = f"{url_sans_fragment}#contrat"  
            return redirect(nouvelle_url)
    else:
        form = ContratForm()
    return render(request, 'secretariat/contrats/creer_contrat.html', {'form': form})

# Modification d'un contrat existant
def modifier_contrat(request, pk):
    contrat = get_object_or_404(Contrat, pk=pk)

    if request.method == 'POST':
        form = ContratForm(request.POST, instance=contrat)
        if form.is_valid():
            form.save()
            url_sans_fragment = reverse('lesApprentiStage:liste_recherche')
            nouvelle_url = f"{url_sans_fragment}#contrat"  
            return redirect(nouvelle_url)
    else:
        form = ContratForm(instance=contrat)

    return render(request, 'secretariat/contrats/modifier_contrat.html', {'form': form, 'contrat': contrat})


# Suppression d'un contrat
def supprimer_contrat(request, pk):
    contrat = get_object_or_404(Contrat, pk=pk)
    if request.method == 'POST':
        contrat.delete()
        url_sans_fragment = reverse('lesApprentiStage:liste_recherche')
        nouvelle_url = f"{url_sans_fragment}#contrat"  
        return redirect(nouvelle_url)
    return render(request, 'secretariat/contrats/supprimer_contrat.html', {'contrat': contrat})

# ///////////////////////crud etudiant ////////////////////////////

def creer_etudiant(request):
    if request.method == 'POST':
        form = EtudiantForm(request.POST)
        if form.is_valid():
            form.save()
            url_sans_fragment = reverse('lesApprentiStage:liste_recherche')
            nouvelle_url = f"{url_sans_fragment}#etudiant"  
            return redirect(nouvelle_url)
        else:
            form = EtudiantForm()
    return render(request, 'secretariat/etudiant/creer_etudiant.html', {'form': form})

def modifier_etudiant(request, num_etu):
    etudiant = get_object_or_404(ProfilEtudiant, numEtu=num_etu)
    if request.method == 'POST':
        form = EtudiantForm(request.POST, instance=etudiant)
        if form.is_valid():
            form.save()
            url_sans_fragment = reverse('lesApprentiStage:liste_recherche')
            nouvelle_url = f"{url_sans_fragment}#entreprise"  
            return redirect(nouvelle_url)
    else:
        form = EtudiantForm(instance=etudiant)
    return render(request, 'secretariat/etudiant/modifier_etudiant.html', {'form': form, 'etudiant': etudiant})

def delete_etudiant(request, num_etu):
    etudiant = get_object_or_404(ProfilEtudiant, numEtu=num_etu)
    if request.method == 'POST':
        etudiant.delete()
        url_sans_fragment = reverse('lesApprentiStage:liste_recherche')
        nouvelle_url = f"{url_sans_fragment}#entreprise"  
        return redirect(nouvelle_url)
    return render(request, 'secretariat/etudiant/delete_etudiant.html', {'etudiant': etudiant})



# ///////////////////////crud entreprise ////////////////////////////
def creer_entreprise(request):
    if request.method == 'POST':
        form = EntrepriseForm(request.POST)
        if form.is_valid():
            form.save()
            url_sans_fragment = reverse('lesApprentiStage:liste_recherche')
            nouvelle_url = f"{url_sans_fragment}#entreprise"  
            return redirect(nouvelle_url)
    else:
        form = EntrepriseForm()
    return render(request, 'secretariat/entreprise/creer_entreprise.html', {'form': form})

def modifier_entreprise(request,pk):
    entreprise = get_object_or_404(Entreprise, pk=pk)
    if request.method == 'POST':
        form = EntrepriseForm(request.POST, instance=entreprise)
        if form.is_valid():
            form.save()
            url_sans_fragment = reverse('lesApprentiStage:liste_recherche')
            nouvelle_url = f"{url_sans_fragment}#entreprise"  
            return redirect(nouvelle_url)
    else:
        form = EntrepriseForm(instance=entreprise)
    return render(request, 'secretariat/entreprise/modifier_entreprise.html', {'form': form, 'entreprise': entreprise})

def delete_entreprise(request,pk):
    entreprise = get_object_or_404(Entreprise, pk=pk)
    if request.method == 'POST':
        entreprise.delete()
        url_sans_fragment = reverse('lesApprentiStage:liste_recherche')
        nouvelle_url = f"{url_sans_fragment}#entreprise"  
        return redirect(nouvelle_url)
    return render(request, 'secretariat/entreprise/delete_entreprise.html', {'entreprise': entreprise})


# ///////////////////////crud enseignant ////////////////////////////

def creer_enseignant(request):
    if request.method == 'POST':
        form = EnseignantForm(request.POST)
        if form.is_valid():
            form.save()
            url_sans_fragment = reverse('lesApprentiStage:liste_recherche')
            nouvelle_url = f"{url_sans_fragment}#offre"  
            return redirect(nouvelle_url)
    else:
        form = EnseignantForm()
    return render(request, 'secretariat/enseignant/creer_enseignant.html', {'form': form})

def modifier_enseignant(request, num_harpege):
    enseignant = get_object_or_404(ProfilEnseignant, numHarpege=num_harpege)
    if request.method == 'POST':
        form = Enseignant_secForm(request.POST, instance=enseignant)
        if form.is_valid():
            enseignant = form.save()
            # Gérer la mise à jour des promos
            EnseignantPromo.objects.filter(enseignant=enseignant).delete()
            for promo in form.cleaned_data['promos']:
                EnseignantPromo.objects.create(enseignant=enseignant, promo=promo)
            url_sans_fragment = reverse('lesApprentiStage:liste_recherche')
            nouvelle_url = f"{url_sans_fragment}#offre"  
            return redirect(nouvelle_url)
    else:
        form = Enseignant_secForm(instance=enseignant)
    return render(request, 'secretariat/enseignant/modifier_enseignant.html', {'form': form, 'enseignant': enseignant})


def delete_enseignant(request, num_harpege):
    enseignant = get_object_or_404(ProfilEnseignant, numHarpege=num_harpege)
    if request.method == 'POST':
        enseignant.delete()
        url_sans_fragment = reverse('lesApprentiStage:liste_recherche')
        nouvelle_url = f"{url_sans_fragment}#enseignant"  
        return redirect(nouvelle_url)
    return render(request, 'secretariat/enseignant/delete_enseignant.html', {'enseignant': enseignant})




# ///////////////////////crud Promo ////////////////////////////

class PromoCreateView(CreateView):
    model = Promo
    template_name = 'secretariat/promo/creer_promo.html'  
    fields = ['nomPromo', 'anneeScolaire', 'departement', 'parcours', 'volumeHoraire']

    def get_success_url(self):
        # Récupérer l'URL de base à partir du nom de l'URL
        base_url = reverse_lazy('lesApprentiStage:liste_recherche')
        # Ajouter le fragment à l'URL
        url_with_fragment = f"{base_url}#promo"
        return url_with_fragment


class PromoDeleteView(DeleteView):
    model = Promo
    template_name = 'secretariat/promo/delete_promo.html'  

    def get_success_url(self):
        # Récupérer l'URL de base à partir du nom de l'URL
        base_url = reverse_lazy('lesApprentiStage:liste_recherche')

        # Ajouter le fragment à l'URL
        url_with_fragment = f"{base_url}#promo"
        return url_with_fragment
    
class PromoUpdateView(UpdateView):
    model = Promo
    template_name = 'secretariat/promo/modifier_promo.html'  
    fields = ['nomPromo', 'anneeScolaire', 'departement', 'parcours', 'volumeHoraire'] 

    def get_success_url(self):
        # Récupérer l'URL de base à partir du nom de l'URL
        base_url = reverse_lazy('lesApprentiStage:liste_recherche')

        # Ajouter le fragment à l'URL
        url_with_fragment = f"{base_url}#promo"
        return url_with_fragment

# ///////////////////////crud departement ////////////////////////////

class DepartementCreateView(CreateView):
    model = Departement
    template_name = 'secretariat/departement/creer_departement.html'  
    fields = ['nomDep', 'adresseDep', 'chef']  

    def get_success_url(self):
        # Récupérer l'URL de base à partir du nom de l'URL
        base_url = reverse_lazy('lesApprentiStage:liste_recherche')

        # Ajouter le fragment à l'URL
        url_with_fragment = f"{base_url}#departements"  
        return url_with_fragment
    
class DepartementUpdateView(UpdateView):
    model = Departement
    template_name = 'secretariat/departement/modifier_departement.html'  
    fields = ['nomDep', 'adresseDep', 'chef']  

    def get_success_url(self):
        # Récupérer l'URL de base à partir du nom de l'URL
        base_url = reverse_lazy('lesApprentiStage:liste_recherche')

        # Ajouter le fragment à l'URL
        url_with_fragment = f"{base_url}#departements"  
        return url_with_fragment
    
class DepartementDeleteView(DeleteView):
    model = Departement
    template_name = 'secretariat/departement/delete_departement.html'  

    def get_success_url(self):
        # Récupérer l'URL de base à partir du nom de l'URL
        base_url = reverse_lazy('lesApprentiStage:liste_recherche')

        # Ajouter le fragment à l'URL
        url_with_fragment = f"{base_url}#departements"  
        return url_with_fragment
    
# ///////////////////////crud offre ////////////////////////////


def creer_offre(request):
    if request.method == 'POST':
        form = OffreForm(request.POST)
        if form.is_valid():
            cleaned_form = form.cleaned_data
            tmp_form = {
                'titre': cleaned_form.get('titre'),
                'mailRh': cleaned_form.get('mailRh'),
                'duree': cleaned_form.get('duree'),
                'description': cleaned_form.get('description'),
                'competences': cleaned_form.get('competences'),
                'entreprise': cleaned_form.get('entreprise'),
                'theme': cleaned_form.get('theme'),
                'datePublication': date.today(),
            }
            form = OffreFormFini(tmp_form) 
            
            Offre = form.save()
            Offre.estPublie = True
            Offre.save()
            url_sans_fragment = reverse('lesApprentiStage:liste_recherche')
            nouvelle_url = f"{url_sans_fragment}#offre"  
            return redirect(nouvelle_url)
    else:
        form = OffreForm()

    return render(request, 'secretariat/offre/creer_offre.html', {'form': form})



class OffreUpdateView(UpdateView):
    model = Offre
    template_name = 'secretariat/offre/modifier_offre.html'  
    fields = ['titre', 'description', 'mailRh', 'competences', 'duree', 'datePublication', 'entreprise', 'theme', 'estPublie'] 
    
    def get_success_url(self):
            # Récupérer l'URL de base à partir du nom de l'URL
            base_url = reverse_lazy('lesApprentiStage:liste_recherche')

            # Ajouter le fragment à l'URL
            url_with_fragment = f"{base_url}#offre"  # Remplacez "offre" par votre fragment souhaité
            return url_with_fragment
        
class OffreDeleteView(DeleteView):
    model = Offre
    template_name = 'secretariat/offre/delete_offre.html' 
     
    def get_success_url(self):
            # Récupérer l'URL de base à partir du nom de l'URL
            base_url = reverse_lazy('lesApprentiStage:liste_recherche')

            # Ajouter le fragment à l'URL
            url_with_fragment = f"{base_url}#offre"  # Remplacez "offre" par votre fragment souhaité
            return url_with_fragment    




# ///////////////////////crud salle ////////////////////////////

class SalleCreateView(CreateView):
    model = Salle
    template_name = 'secretariat/salle/creer_salle.html'
    fields = ['numero']

    def get_success_url(self):
        # Récupérer l'URL de base à partir du nom de l'URL
        base_url = reverse_lazy('lesApprentiStage:liste_recherche')

        # Ajouter le fragment à l'URL
        url_with_fragment = f"{base_url}#salle"
        return url_with_fragment

class SalleUpdateView(UpdateView):
    model = Salle
    template_name = 'secretariat/salle/modifier_salle.html'
    fields = ['numero']

    def get_success_url(self):
        # Récupérer l'URL de base à partir du nom de l'URL
        base_url = reverse_lazy('lesApprentiStage:liste_recherche')

        # Ajouter le fragment à l'URL
        url_with_fragment = f"{base_url}#salle"
        return url_with_fragment

class SalleDeleteView(DeleteView):
    model = Salle
    template_name = 'secretariat/salle/delete_salle.html'

    def get_success_url(self):
    # Récupérer l'URL de base à partir du nom de l'URL
        base_url = reverse_lazy('lesApprentiStage:liste_recherche')

        # Ajouter le fragment à l'URL
        url_with_fragment = f"{base_url}#salle"
        return url_with_fragment


# ///////////////////////crud soutenance ////////////////////////////

class BaseSoutenanceForm(forms.ModelForm):
    class Meta:
        model = Soutenance
        fields = ['dateSoutenance', 'heureSoutenance', 'salle', 'idContrat', 'candide', 'estDistanciel']

    def __init__(self, *args, **kwargs):
        super(BaseSoutenanceForm, self).__init__(*args, **kwargs)
        # Définir le champ candide comme optionnel
        self.fields['candide'].required = False
        self.fields['salle'].required = False

class SoutenanceCreateForm(BaseSoutenanceForm):
    class Meta(BaseSoutenanceForm.Meta):
        widgets = {
            'dateSoutenance': forms.DateInput(attrs={'type': 'date'}),
            'heureSoutenance': forms.TimeInput(attrs={'type': 'time'}),
        }

class SoutenanceCreateView(CreateView):
    form_class = SoutenanceCreateForm
    template_name = 'secretariat/soutenance/creer_soutenance.html'

    def get_success_url(self):
        base_url = reverse_lazy('lesApprentiStage:liste_recherche')
        url_with_fragment = f"{base_url}#soutenance"
        return url_with_fragment

class TimePickerWidget(forms.TimeInput):
    input_type = 'time'

    def format_value(self, value):
        if isinstance(value, str):
            return value
        return value.strftime('%H:%M') if value else ''

class SoutenanceUpdateForm(BaseSoutenanceForm):
    class Meta(BaseSoutenanceForm.Meta):
        widgets = {
            'dateSoutenance': forms.DateInput(attrs={'type': 'date'}),
            'heureSoutenance': TimePickerWidget(attrs={'type': 'time'}),
        }

class SoutenanceUpdateView(UpdateView):
    model = Soutenance
    form_class = SoutenanceUpdateForm
    template_name = 'secretariat/soutenance/modifier_soutenance.html'

    def get_success_url(self):
        base_url = reverse_lazy('lesApprentiStage:liste_recherche')
        url_with_fragment = f"{base_url}#soutenance"
        return url_with_fragment

class SoutenanceDeleteView(DeleteView):
    model = Soutenance
    template_name = 'secretariat/soutenance/delete_soutenance.html'

    def get_success_url(self):
            # Récupérer l'URL de base à partir du nom de l'URL
        base_url = reverse_lazy('lesApprentiStage:liste_recherche')

        # Ajouter le fragment à l'URL
        url_with_fragment = f"{base_url}#soutenance"
        return url_with_fragment


# ///////////////////////crud documents ////////////////////////////

class DocumentCreateView(CreateView):
    model = Document
    template_name = 'secretariat/document/creer_document.html'
    fields = ['titre', 'fichier', 'contrat']
    success_url = reverse_lazy('lesApprentiStage:liste_recherche')

    def get_success_url(self):
            # Récupérer l'URL de base à partir du nom de l'URL
        base_url = reverse_lazy('lesApprentiStage:liste_recherche')

        # Ajouter le fragment à l'URL
        url_with_fragment = f"{base_url}#document"
        return url_with_fragment

class DocumentUpdateView(UpdateView):
    model = Document
    template_name = 'secretariat/document/modifier_document.html'
    fields = ['titre', 'fichier', 'contrat']
    success_url = reverse_lazy('lesApprentiStage:liste_recherche')

    def get_success_url(self):
            # Récupérer l'URL de base à partir du nom de l'URL
        base_url = reverse_lazy('lesApprentiStage:liste_recherche')

        # Ajouter le fragment à l'URL
        url_with_fragment = f"{base_url}#document"
        return url_with_fragment

class DocumentDeleteView(DeleteView):
    model = Document
    template_name = 'secretariat/document/delete_document.html'

    def get_success_url(self):
            # Récupérer l'URL de base à partir du nom de l'URL
        base_url = reverse_lazy('lesApprentiStage:liste_recherche')

        # Ajouter le fragment à l'URL
        url_with_fragment = f"{base_url}#document"
        return url_with_fragment

# ///////////////////////crud evaluation ////////////////////////////
class EvaluationCreateView(CreateView):
    model = Evaluation
    template_name = 'secretariat/evaluation/creer_evaluation.html'

    def get_form_class(self):
        if self.request.user.type_utilisateur == 'enseignant':
            class EnseignantEvaluationForm(forms.ModelForm):
                class Meta:
                    model = Evaluation
                    fields = ['contrat', 'note', 'commentaire']
            return EnseignantEvaluationForm
        else:
            class DefaultEvaluationForm(forms.ModelForm):
                class Meta:
                    model = Evaluation
                    fields = ['contrat', 'enseignant', 'note', 'commentaire']
            return DefaultEvaluationForm

    def get_form(self, form_class=None):
        form = super(EvaluationCreateView, self).get_form(form_class)

        if self.request.user.type_utilisateur == 'enseignant':
            enseignant = self.request.user.profilenseignant
            
            # Filtrer les choix de contrat pour les contrats liés à l'enseignant connecté
            if 'contrat' in form.fields:
                form.fields['contrat'].queryset = Contrat.objects.filter(enseignant=enseignant)

        return form

    def form_valid(self, form):
        if self.request.user.type_utilisateur == 'enseignant':
            # Attribuer automatiquement l'enseignant connecté à l'évaluation
            form.instance.enseignant = self.request.user.profilenseignant
        return super(EvaluationCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lesApprentiStage:liste_recherche') + "#evaluation"

class EvaluationUpdateView(UpdateView):
    model = Evaluation
    template_name = 'secretariat/evaluation/modifier_evaluation.html'

    def get_form_class(self):
        # Choisir la classe de formulaire en fonction du type d'utilisateur
        if self.request.user.type_utilisateur == 'enseignant':
            # Classe de formulaire pour les enseignants (sans le champ 'enseignant')
            class EnseignantEvaluationForm(forms.ModelForm):
                class Meta:
                    model = Evaluation
                    fields = ['contrat', 'note', 'commentaire']
            return EnseignantEvaluationForm
        else:
            # Classe de formulaire par défaut (avec le champ 'enseignant')
            class DefaultEvaluationForm(forms.ModelForm):
                class Meta:
                    model = Evaluation
                    fields = ['contrat', 'enseignant', 'note', 'commentaire']
            return DefaultEvaluationForm

    def get_form(self, form_class=None):
        form = super(EvaluationUpdateView, self).get_form(form_class)

        if self.request.user.type_utilisateur == 'enseignant':
            enseignant = self.request.user.profilenseignant
            
            # Filtrer les choix de contrat pour les contrats liés à l'enseignant connecté
            if 'contrat' in form.fields:
                form.fields['contrat'].queryset = Contrat.objects.filter(enseignant=enseignant)

            # Rendre le champ 'enseignant' caché et définir sa valeur
            if 'enseignant' in form.fields:
                form.fields['enseignant'].initial = enseignant.numHarpege
                form.fields['enseignant'].widget = forms.HiddenInput()

        return form

    def get_success_url(self):
        # Redirection après la mise à jour de l'évaluation
        return reverse_lazy('lesApprentiStage:liste_recherche') + "#evaluation"
    
class EvaluationDeleteView(DeleteView):
    model = Evaluation
    template_name = 'secretariat/evaluation/delete_evaluation.html'
    
    def get_success_url(self):
            # Récupérer l'URL de base à partir du nom de l'URL
            base_url = reverse_lazy('lesApprentiStage:liste_recherche')

            # Ajouter le fragment à l'URL
            url_with_fragment = f"{base_url}#evaluation"  # Remplacez "evaluation" par votre fragment souhaité
            return url_with_fragment


@login_required
@user_type_and_role_required(['secretaire'])
def liste_contrats_signes(request):
    contrats_signes = Contrat.objects.filter(etat='1')
    for contrat in contrats_signes:
        contrat.document = Document.objects.filter(contrat=contrat).first()
    return render(request, 'secretariat/liste_contrats_signes.html', {'contrats_signes': contrats_signes})

@login_required
@user_type_and_role_required(['secretaire'])
def telecharger_convention_secretaire(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    response = HttpResponse(document.fichier.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename="{document.titre}"'
    return response

@login_required
@user_type_and_role_required(['secretaire'])
def upload_convention_secretaire(request):
    if request.method == 'POST':
        contrat_id = request.POST.get('contrat_id')
        fichier_upload = request.FILES.get('fichier')
        
        if fichier_upload:
            contrat = get_object_or_404(Contrat, pk=contrat_id)
            etudiant_email = contrat.etudiant.mailEtu
            document, created = Document.objects.update_or_create(
                contrat=contrat,
                defaults={'fichier': fichier_upload, 'titre': fichier_upload.name}
            )
            contrat.etat = "2"
            contrat.save()

            sujet = "Nouvelle Convention Téléversée"
            message = "Une nouvelle convention a été téléversée et nécessite votre attention."
            destinataire = [etudiant_email]

            send_mail(sujet, message, 'samidevtest53@gmail.com', destinataire)

            return JsonResponse({'success': True, 'message': 'Fichier uploadé avec succès !'})
        else:
            return JsonResponse({'success': False, 'message': 'Aucun fichier fourni !'})
            
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'}, status=405)

# /////////////////////// Soutenances Léo ////////////////////////////

def inscrire_soutenance(request, soutenance_id):
    soutenance = get_object_or_404(Soutenance, id=soutenance_id)
    user = request.user
    
    if user.get_user_type() == "enseignant" and soutenance.candide != user.profilenseignant:
        soutenance.candide = user.profilenseignant
        soutenance.save()

    return redirect(reverse('lesApprentiStage:liste_recherche') + '?selected_filter=soutenance')

def desinscrire_soutenance(request, soutenance_id):
    soutenance = get_object_or_404(Soutenance, id=soutenance_id)
    user = request.user

    if user.get_user_type() == "enseignant" and soutenance.candide == user.profilenseignant:
        soutenance.candide = None
        soutenance.save()

    return redirect(reverse('lesApprentiStage:liste_recherche') + '?selected_filter=soutenance')


class NombreSoutenanceView(View):
    template_name = 'secretariat/soutenance/nombre_soutenances.html'

    def get(self, request, num_harpege=None):
        enseignant = get_object_or_404(ProfilEnseignant, pk=num_harpege) if num_harpege else None
        form = NombreSoutenanceForm(initial={'enseignant': enseignant})
        return render(request, self.template_name, {'form': form, 'enseignant': enseignant})

    def post(self, request, num_harpege=None):
        form = NombreSoutenanceForm(request.POST)

        if form.is_valid():
            promo = form.cleaned_data['promo']
            nombre_soutenances_stage = form.cleaned_data['nombreSoutenancesStage']
            nombre_soutenances_apprentissage = form.cleaned_data['nombreSoutenancesApprentissage']

            # Vérifier si une instance existe déjà pour le prof et la promo
            try:
                enseignant = ProfilEnseignant.objects.get(pk=num_harpege)
                instance = NombreSoutenances.objects.get(enseignant=enseignant, promo=promo)
                instance.nombreSoutenancesStage = nombre_soutenances_stage
                instance.nombreSoutenancesApprentissage = nombre_soutenances_apprentissage
                instance.save()
            except NombreSoutenances.DoesNotExist:
                # Si aucune instance n'existe pas, créez-en une nouvelle
                instance = form.save(commit=False)
                instance.promo = promo
                instance.enseignant = enseignant
                instance.save()

            messages.success(request, 'Nombre de soutenances attribué avec succès.')
            return redirect('lesApprentiStage:home')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
            return render(request, self.template_name, {'form': form})



@login_required
def soutenance(request):
    user_type_to_view_func = {
        'secretaire': soutenance_sec,
        'etudiant': soutenance_etu,
        'enseignant': soutenance_ens,
    }
    
    user_type = request.user.type_utilisateur
    view_func = user_type_to_view_func.get(user_type)
    
    if view_func:
        return view_func(request, user_type)
    else:
        return HttpResponseForbidden("Type d'utilisateur non autorisé pour cette action.")


@login_required
def soutenance_sec(request, user_type):
    if request.method == 'POST':
        formSoutenance = SoutenanceForm(request.POST)
        if formSoutenance.is_valid():
            salle = formSoutenance.cleaned_data['salle']
            heureSoutenance = formSoutenance.cleaned_data['heureSoutenance']
            dateSoutenance = formSoutenance.cleaned_data['dateSoutenance']
            verification = Soutenance.objects.filter(
                salle=salle, 
                heureSoutenance=heureSoutenance,
                dateSoutenance=dateSoutenance
            )
            if not verification.exists():
                formSoutenance.save()
                messages.success(request, "La soutenance a été ajoutée avec succès.")
                return redirect('lesApprentiStage:soutenance')
            else:
                messages.error(request, "Une soutenance est déjà programmée dans cette salle à cette heure et date.")
        else:
            messages.error(request, "Il y a eu un problème avec le formulaire.")
    else:
        formSoutenance = SoutenanceForm()
    listSoutenance = Soutenance.objects.all()
    return render(request, 'pages/soutenance.html', {
        "form": formSoutenance,
        'listSoutenance': listSoutenance, 
        'user': user_type
    })

@login_required
def soutenance_etu(request, user_type):
    unUtilisateur = get_object_or_404(Utilisateur, username=request.user.username)
    unEtudiant = get_object_or_404(ProfilEtudiant, utilisateur=unUtilisateur)
    lesContrats = Contrat.objects.filter(etudiant=unEtudiant)  # Récupérer tous les contrats pour l'étudiant
    etuSoutenances = Soutenance.objects.filter(idContrat__in=lesContrats)  # Utiliser '__in' pour filtrer par les contrats récupérés
    return render(request, 'pages/soutenance.html', {
        'etuSoutenances': etuSoutenances,  # Passer les soutenances en contexte
        'user': user_type
    })


@login_required
def soutenance_ens(request, user_type):
    unUtilisateur = get_object_or_404(Utilisateur, username=request.user.username)
    unEnseignant = get_object_or_404(ProfilEnseignant, utilisateur=unUtilisateur)
    unContrat = Contrat.objects.filter(enseignant=unEnseignant)
    enSoutenance = Soutenance.objects.filter(idContrat__in=unContrat) | Soutenance.objects.filter(candide=unEnseignant)
    listCandideSoutenance = Soutenance.objects.filter(candide=None).exclude(idContrat__in=unContrat)
    return render(request, 'pages/soutenance.html', {
        'enSoutenance': enSoutenance,
        'user': user_type, 
        'listCandideSoutenance': listCandideSoutenance, 
        'enseignant': unEnseignant
    })



@login_required
@user_type_and_role_required(['etudiant'])
def ajouter_contrat(request):
    if request.method == 'POST':
        form = ContratEtudiantForm(request.POST)
        if form.is_valid():
            contrat = form.save(commit=False)
            try:
                profil_etudiant = request.user.profiletudiant
            except Utilisateur.profiletudiant.RelatedObjectDoesNotExist:
                messages.error(request, "Vous devez avoir un profil étudiant pour ajouter un contrat.")
                return redirect('lesApprentiStage:home')

            contrat.etudiant = profil_etudiant
            contrat.save()
            messages.success(request, "Contrat ajouté avec succès.")
            return redirect('lesApprentiStage:ajouter_responsable', contrat_id=contrat.id)
        
    else:
        form = ContratEtudiantForm()
    
    return render(request, 'etudiant/ajouter_contrat.html', {'form': form, 'EntrepriseForm': EntrepriseForm(), 'ThemeForm': ThemeForm()})


@login_required
def ajouter_entrepriseSeul(request):
    if request.method == 'POST':
        form = EntrepriseForm(request.POST)
        if form.is_valid():
            entreprise = form.save()
            messages.success(request, "Entreprise ajoutée avec succès.")
            return redirect('lesApprentiStage:home') 
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
    else:
        form = EntrepriseForm()

    return render(request, 'pages/ajouter_entreprise.html', {'EntrepriseForm': form})


@login_required
def ajouter_entreprise(request):
    if request.method == 'POST':
        form = EntrepriseForm(request.POST)
        if form.is_valid():
            entreprise = form.save()
            messages.success(request, "Entreprise ajoutée avec succès.")
            return JsonResponse({"success": True, "entreprise": {"nomEnt": entreprise.nomEnt, "pk": entreprise.pk}})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = EntrepriseForm()

    return render(request, 'pages/ajouter_entreprise.html', {'EntrepriseForm': form})



@login_required
def supprimerSoutenance(request,id):
    unesoutenance = Soutenance.objects.filter(id = id)[0]
    unesoutenance.delete()
    return redirect('lesApprentiStage:soutenance')

@login_required
def modifierSoutenance(request, id):
    unesoutenance = get_object_or_404(Soutenance, id=id)
    listSoutenance = Soutenance.objects.all()
    if request.method == 'POST':
        formSoutenance = SoutenanceForm(request.POST, instance=unesoutenance)
        if formSoutenance.is_valid():
            salle = formSoutenance.cleaned_data['salle']
            heureSoutenance = formSoutenance.cleaned_data['heureSoutenance']
            dateSoutenance = formSoutenance.cleaned_data['dateSoutenance']
            verification = Soutenance.objects.filter(
                salle=salle, 
                heureSoutenance=heureSoutenance, 
                dateSoutenance=dateSoutenance
            ).exclude(id=id)
            if not verification.exists():
                formSoutenance.save()
                messages.success(request, "La soutenance a été modifiée avec succès.")
                return redirect('lesApprentiStage:soutenance')
            else:
                messages.error(request, "Impossible de modifier la soutenance car la salle est déjà réservée à cet horaire.")
        else:
            messages.error(request, "Il y a eu un problème avec le formulaire.")
    else:
        formSoutenance = SoutenanceForm(instance=unesoutenance)
    return render(request, 'pages/soutenance.html', {
        "form": formSoutenance, 
        'modifSoutenance': unesoutenance, 
        'listSoutenance': listSoutenance,
        'user': request.user.type_utilisateur
    })

@login_required
def inscrireSoutenance(request,id):
    unUtilisateur = Utilisateur.objects.filter(username = request.user.username)[0]
    unEnseignant = ProfilEnseignant.objects.filter(utilisateur = unUtilisateur)[0]
    unesoutenance = Soutenance.objects.filter(id = id)[0]
    unesoutenance.candide = unEnseignant
    unesoutenance.save()
    return redirect('lesApprentiStage:soutenance')


@login_required
def desinscrireSoutenance(request,id):
    unesoutenance = Soutenance.objects.filter(id = id)[0]
    unesoutenance.candide = None
    unesoutenance.save()
    return redirect('lesApprentiStage:soutenance')


@login_required
def calendar_events(request):
    events = []

    # Assurez-vous que seul un enseignant peut accéder à cette vue
    if request.user.type_utilisateur != 'enseignant':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Obtenez le profil enseignant connecté
    profil_enseignant = get_object_or_404(ProfilEnseignant, utilisateur=request.user)

    # Filtrez les soutenances où l'utilisateur est le candide
    soutenances = Soutenance.objects.filter(candide=profil_enseignant)

    for soutenance in soutenances:
        event = {
            'title': f'Soutenance: {soutenance.idContrat.etudiant.nomEtu} {soutenance.idContrat.etudiant.prenomEtu}',
            'start': f'{soutenance.dateSoutenance.isoformat()}T{soutenance.heureSoutenance.isoformat()}',
            'end': (datetime.combine(soutenance.dateSoutenance, soutenance.heureSoutenance) + timedelta(hours=1)).isoformat(),
            'url': '',
            'allDay': False
        }
        
        events.append(event)

    return JsonResponse(events, safe=False)


def export_calendar(request):
    # Créer un calendrier
    cal = Calendar()

    # Récupérer les événements depuis la base de données
    events = Soutenance.objects.filter(candide=request.user.profilenseignant)

    for soutenance in events:
        event = Event()
        event.add('summary', 'Soutenance ' + soutenance.idContrat.etudiant.nomEtu)
        event.add('dtstart', datetime.combine(soutenance.dateSoutenance, soutenance.heureSoutenance))
        event.add('dtend', datetime.combine(soutenance.dateSoutenance, soutenance.heureSoutenance) + timedelta(hours=1))
        event.add('dtstamp', datetime.now())
        # Ajouter d'autres propriétés si nécessaire...
        
        cal.add_component(event)

    response = HttpResponse(cal.to_ical(), content_type="text/calendar")
    response['Content-Disposition'] = 'attachment; filename="soutenances.ics"'
    return response

def calendar_ens(request):
    return render(request, 'pages/calendrier_ens.html')

def ajouter_theme(request):
    if request.method == 'POST':
        form = ThemeForm(request.POST)
        if form.is_valid():
            theme = form.save()
            messages.success(request, "Thème ajouté avec succès.")
            return JsonResponse({"success": True, "theme": {"nomTheme": theme.nomTheme, "pk": theme.pk}})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = ThemeForm()

    return render(request, 'pages/ajouter_theme.html', {'ThemeForm': form})

def ajouter_offre(request):
    if request.method == 'POST':
        form = OffreForm(request.POST)
        if form.is_valid():
            cleaned_form=form.cleaned_data
            tmp_form={
                'titre': cleaned_form.get('titre'),
                'mailRh': cleaned_form.get('mailRh'),
                'duree': cleaned_form.get('duree'),
                'description': cleaned_form.get('description'),
                'competences': cleaned_form.get('competences'),
                'entreprise': cleaned_form.get('entreprise'),
                'theme': cleaned_form.get('theme'),
                'datePublication': date.today()
            }
            form=OffreFormFini(tmp_form) 
            Offre = form.save()
            return redirect("/")
        else:
            return render(request, 'pages/ajouter_offre.html', {'OffreForm': form, 'EntrepriseForm': EntrepriseForm(), 'ThemeForm': ThemeForm()})
    else:
        form = OffreForm()

    return render(request, 'pages/ajouter_offre.html', {'OffreForm': form, 'EntrepriseForm': EntrepriseForm(), 'ThemeForm': ThemeForm()})



@login_required
def edit_enseignant(request):
    if request.user.type_utilisateur != 'enseignant':
        return redirect('page_d_erreur')

    profil_enseignant, created = ProfilEnseignant.objects.get_or_create(utilisateur=request.user)
    change_password_form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        form = ProfilEnseignantForm(request.POST, instance=profil_enseignant)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('/')
    else:
        form = ProfilEnseignantForm(instance=profil_enseignant)

    return render(request, 'enseignant/edit_enseignant.html', {'form': form, 'change_password_form': change_password_form})

@login_required
def delete_offre(request, pk):
    instance = get_object_or_404(Offre, pk=pk)
    instance.delete()
    return HttpResponse("true")

@login_required
def valid_offre(request, pk):
    instance = get_object_or_404(Offre, pk=pk)
    instance.estPublie = 1
    instance.save()
    return HttpResponse("true")


def ajouter_responsable(request, contrat_id):
    contrat = get_object_or_404(Contrat, pk=contrat_id)
    entreprise = contrat.entreprise

    if request.method == 'POST':
        responsable_form = ResponsableForm(request.POST, entreprise=entreprise)
        tuteur_form = TuteurForm(request.POST)
        if responsable_form.is_valid() and tuteur_form.is_valid():
            responsable = responsable_form.save(commit=False)
            tuteur = tuteur_form.save(commit=False)
            if responsable_form.cleaned_data['responsable_existant']:
                responsable = responsable_form.cleaned_data['responsable_existant']
            else:
                responsable.entreprise = entreprise
                responsable.save()
            tuteur.entreprise = entreprise
            tuteur.save()
            contrat.responsable = responsable
            contrat.tuteur = tuteur
            contrat.save()
            messages.success(request, "Responsable et tuteur ajoutés avec succès.")
            return redirect('lesApprentiStage:home')
    else:
        responsable_form = ResponsableForm(entreprise=entreprise)
        tuteur_form = TuteurForm()

    context = {
        'responsable_form': responsable_form,
        'tuteur_form': tuteur_form
    }
    return render(request, 'pages/ajouter_responsable.html', context)

@login_required
@user_type_and_role_required(['secretaire'])
def details_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(ProfilEtudiant, numEtu=etudiant_id)
    contrats_stage = Contrat.objects.filter(etudiant=etudiant, type='stage')
    contrats_apprentissage = Contrat.objects.filter(etudiant=etudiant, type='apprentissage')

    context = {
        'etudiant': etudiant,
        'contrats_stage': contrats_stage,
        'contrats_apprentissage': contrats_apprentissage,
    }
    return render(request, 'admin/detailsEtu.html', context)

@login_required
@user_type_and_role_required(['secretaire'])
def details_entreprise(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, numSiret=entreprise_id)

    context = {
        'entreprise': entreprise,
    }
    return render(request, 'admin/detailsEnt.html', context)

def affichage_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)

    # Assurez-vous que la relation avec l'entreprise existe
    if contrat.entreprise:
        # Utilisez la relation inverse à partir du modèle Responsable
        responsable_entreprise = contrat.entreprise.responsable_set.first()
    else:
        responsable_entreprise = None

    context = {
        'contrat': contrat,
        'entreprise': contrat.entreprise,
        'tuteur': contrat.tuteur,
        'responsable_entreprise': responsable_entreprise,
    }

    return render(request, 'admin/affichageContrat.html', context)



def offre_detail(request, offre_id):
    offre = Offre.objects.get(pk=offre_id)
    return render(request, 'etudiant/offre_detail.html', {'offre': offre})

def recherche_offres(request):
    theme = Theme.objects.all()
    entreprise = Entreprise.objects.all()

    query = request.GET.get('query', '')
    entreprise_id = request.GET.get('entreprise', '')
    theme_id = request.GET.get('theme', '')
    date_min = request.GET.get('date_min', '')
    date_max = request.GET.get('date_max', '')

    queryset = Offre.objects.all()
    if entreprise_id:
        queryset = queryset.filter(entreprise__id=entreprise_id)
    if theme_id:
        queryset = queryset.filter(theme__id=theme_id)
    if date_min:
        queryset = queryset.filter(datePublication__gte=date_min)
    if date_max:
        queryset = queryset.filter(datePublication__lte=date_max)

    if query:
        queryset = queryset.filter(
            Q(titre__icontains=query) |
            Q(description__icontains=query) |
            Q(competences__icontains=query)
        )
    return render(request, 'etudiant/recherche_offres.html', {'results': queryset, 'theme': theme, 'entreprise': entreprise})


@login_required
def edit_etudiant(request):
    if request.user.type_utilisateur != 'etudiant':
        return redirect('page_d_erreur')

    profil_etudiant, created = ProfilEtudiant.objects.get_or_create(utilisateur=request.user)
    change_password_form = PasswordChangeForm(request.user)
    context = {
        'change_password_form': change_password_form,
    }
    if request.method == 'POST':
        form = EtudiantProfilForm(request.POST, instance=profil_etudiant)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('lesApprentiStage:home')
    else:
        form = EtudiantProfilForm(instance=profil_etudiant)

    return render(request, 'etudiant/edit_etudiant.html', {'form': form, 'change_password_form': change_password_form})


@login_required
def profile(request):
    etudiant = request.user.profiletudiant
    contrats = Contrat.objects.filter(etudiant=etudiant).select_related('entreprise', 'theme', 'tuteur', 'enseignant')
    documents = Document.objects.filter(contrat__etudiant=etudiant)
    evaluations = Evaluation.objects.filter(contrat__etudiant=etudiant)
    soutenance = Soutenance.objects.filter(idContrat__etudiant=request.user.profiletudiant)
    print(soutenance)

    context = {
        'etudiant': etudiant,
        'contrats': contrats,
        'documents': documents,
        'evaluations': evaluations,
        'soutenances': soutenance,
    }
    return render(request, 'etudiant/profile.html', context)

@login_required
def generer_convention_view(request, contrat_id):
    try:
        contrat = Contrat.objects.get(id=contrat_id, estValide=True, etudiant=request.user.profiletudiant)
        document_path = generer_convention(contrat)
        pdf_path = os.path.join(settings.BASE_DIR, 'documents/documents/Convention_'+contrat.etudiant.nomEtu+'.pdf')
        convert_docx_to_pdf(document_path, pdf_path)
        with open(pdf_path, 'rb') as doc:
            response = HttpResponse(doc.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename="Convention_{contrat.etudiant.nomEtu}.pdf"'
            return response
    except Contrat.DoesNotExist:
        return HttpResponse("Contrat non valide ou inexistant.")



def upload_csv(request):
    if request.method == "GET":
        return render(request, 'secretariat/upload_csv.html')

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        return HttpResponse("Le fichier n'est pas un CSV")

    file_data = csv_file.read().decode("utf-8")
    lines = file_data.split("\n")

    for line in lines:
        fields = line.split(",")
        if fields and len(fields) > 1:
            # Utilisez les nouvelles informations pour les étudiants
            annee = fields[0]
            nom = fields[1]
            prenom = fields[2]
            numEtu = fields[3]
            civilite = fields[4]
            adresse = fields[5]
            cp = fields[6]
            ville = fields[7]
            tel = fields[8]
            promo_nom = fields[9]
            departement_id = fields[10]

            try:
                departement = Departement.objects.get(id=departement_id)
            except Departement.DoesNotExist:
                return HttpResponse(f"Erreur : le département avec l'ID {departement_id} n'existe pas", status=400)

            username = nom + '_' + prenom
            password = make_password('password_par_defaut')
            user, created = Utilisateur.objects.get_or_create(username=username, defaults={'password': password, 'type_utilisateur': 'etudiant'})
            
            promo, created = Promo.objects.get_or_create(nomPromo=promo_nom, annee=annee, departement=departement)

            ProfilEtudiant.objects.update_or_create(
                utilisateur=user,
                nomEtu=nom,
                prenomEtu=prenom,
                numEtu=numEtu,
                civiliteEtu=civilite,
                adresseEtu=adresse,
                cpEtu=cp,
                villeEtu=ville,
                telEtu=tel,
                promo=promo,
                idDepartement=departement,
            )

    return redirect('lesApprentiStage:home')

def suivi_etudiants(request):
    user = request.user
    enseignant = ProfilEnseignant.objects.get(utilisateur=user)
    etudiants = ProfilEtudiant.objects.all()

    # Récupération des filtres
    promo_filter = request.GET.get('promo')
    entreprise_filter = request.GET.get('entreprise')
    departement_filter = request.GET.get('departement')
    theme_filter = request.GET.get('theme')
    promo_filter = request.GET.get('promo')
    statut_stage = request.GET.get('statut_stage')
    tuteur_filter = request.GET.get('tuteur')
    recherche_etudiant = request.GET.get('recherche_etudiant', '')


    if enseignant.roleEnseignant == ProfilEnseignant.CHEF_DEPARTEMENT:
        etudiants = etudiants.filter(idDepartement__chef=enseignant)
    elif enseignant.roleEnseignant == ProfilEnseignant.ENSEIGNANT_PROMO:
        promos_gerees = EnseignantPromo.objects.filter(enseignant=enseignant).values_list('promo', flat=True)
        etudiants = etudiants.filter(promo__in=promos_gerees)

    # Application des filtres
    if promo_filter:
        etudiants = etudiants.filter(promo_id=promo_filter)
    if entreprise_filter:
        etudiants = etudiants.filter(contrat__entreprise_id=entreprise_filter)
    if departement_filter:
        etudiants = etudiants.filter(idDepartement_id=departement_filter)
    if theme_filter:
        etudiants = etudiants.filter(contrat__theme_id=theme_filter)
    if statut_stage:
        if statut_stage == 'valide':
            etudiants = etudiants.filter(contrat__estValide=True)
        elif statut_stage == 'en_attente':
            etudiants = etudiants.filter(contrat__estValide=False)
        elif statut_stage == 'sans_stage':
            etudiants = etudiants.exclude(contrat__isnull=False)
    if tuteur_filter:
        etudiants = etudiants.filter(contrat__tuteur__id=tuteur_filter)
    if recherche_etudiant:
        etudiants = etudiants.filter(
            Q(nomEtu__icontains=recherche_etudiant) | 
            Q(prenomEtu__icontains=recherche_etudiant) |
            Q(numEtu__icontains=recherche_etudiant)
        )

    # Transmettre les options de filtrage au template
    promos = Promo.objects.all()
    entreprises = Entreprise.objects.all()
    departements = Departement.objects.all()
    themes = Theme.objects.all()
    tuteurs = Tuteur.objects.all()


    return render(request, 'enseignant/suivi_etudiants.html', {
        'etudiants': etudiants,
        'tuteurs': tuteurs,
        'promos': promos,
        'entreprises': entreprises,
        'departements': departements,
        'themes': themes
    })