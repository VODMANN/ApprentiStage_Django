describe('Connexion', () => {
  it('passes', () => {
    cy.visit('http://127.0.0.1:8000/');
    cy.get(':nth-child(3) > .nav-link').click();
    cy.get('#id_username').type('etudiant123');
    cy.get('#id_password').type('etudiantpassword');
    cy.get('#submit').click();
  })
})

describe('Création d\'une offre', () => {
  it('passes', () => {
    cy.visit('http://127.0.0.1:8000/');
    cy.get(':nth-child(2) > .nav-link').click();
    cy.get('#form-offre').within(() => {

    });
  
    cy.get('#id_titre').type('Offre développement web')
    cy.get('#id_mailRh').type('exemple@mail.com')
    cy.get('#id_duree').type('3 mois')
    cy.get('#id_description').type('Description de l\'offre')
    cy.get('#id_competences').type('Compétences requises')
    cy.get('#id_entreprise').select('Entreprise XYZ - 456 Rue des Entreprises - 12345 - Ville Entreprise')
    cy.get('#id_theme').select('Développement Web')
    cy.get('#form-offre > [type="submit"]').click()
    

  })
})

describe('Validation des offres', () => {
  it('passes', () => {
    cy.visit('http://127.0.0.1:8000/');
    cy.get(':nth-child(3) > .nav-link').click();
    cy.get('#id_username').type('secretaire789');
    cy.get('#id_password').type('secretairepassword');
    cy.get('#submit').click();

    cy.get('[href="/secretariat/validation_offre/"]').click();
    cy.get('.valid-button').click({ multiple: true });
  })
})

describe('Delete des offres', () => {
  it('passes', () => {
    cy.visit('http://127.0.0.1:8000/');
    cy.get(':nth-child(3) > .nav-link').click();
    cy.get('#id_username').type('secretaire789');
    cy.get('#id_password').type('secretairepassword');
    cy.get('#submit').click();

    cy.get('[href="/secretariat/validation_offre/"]').click();
    cy.get('.delete-button').click({ multiple: true });
  })
})

describe('Modification d\'un étudiant', () => {
  it('passes', () => {
    cy.visit('http://127.0.0.1:8000/');
    cy.get(':nth-child(3) > .nav-link').click();
    cy.get('#id_username').type('secretaire789');
    cy.get('#id_password').type('secretairepassword');
    cy.get('#submit').click();

    cy.get(':nth-child(2) > .nav-link').click();
    cy.get('#filtre_select').select('etudiant');
    cy.get('#etudiant_table > .table > tbody > :nth-child(1) > .text-right > .btn-group > .btn-secondary').click();

    cy.get('#id_nomEtu').clear().type('YourName');
    cy.get('#id_prenomEtu').clear().type('YourFirstName');
    cy.get('#id_numEtu').clear().type('123456789');
    cy.get('#id_numDossier').clear().type('9876');
    cy.get('#id_ineEtu').clear().type('2147483');
    cy.get('#id_prenom2Etu').clear().type('YourSecondName');
    cy.get('#id_civiliteEtu').clear().type('Mr');
    cy.get('#id_adresseEtu').clear().type('123 Main Street');
    cy.get('#id_mailEtu').clear().type('your.email@example.com');
    cy.get('#id_telEtu').clear().type('9876543210');
    cy.get('#id_dateNEtu').clear().type('10/02/2022');
    cy.get('#id_lieuNEtu').clear().type('City');
    cy.get('#id_departementNEtu').clear().type('YourDepartment');
    cy.get('#id_nationaliteEtu').clear().type('YourNationality');
    cy.get('#id_cpEtu').clear().type('12345');
    cy.get('#id_villeEtu').clear().type('YourCity');
    cy.get('#id_adresseParent').clear().type('456 Parent Avenue');
    cy.get('#id_cpParent').clear().type('54321');
    cy.get('#id_villeParent').clear().type('ParentCity');
    cy.get('#id_telParent').clear().type('8765432109');
    cy.get('#id_mailParent').clear().type('parents.email@example.com');
    
    // Select options from dropdowns
    cy.get('#id_promo').select('3A');
    cy.get('#id_idDepartement').select('Département Informatique');

    // Submit the form
    cy.get('.form-actions').contains('Enregistrer les modifications').click();

  })
})