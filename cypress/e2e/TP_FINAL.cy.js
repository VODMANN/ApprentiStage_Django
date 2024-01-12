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
    
    cy.get(':nth-child(3) > .nav-link').click();
    cy.get('#id_username').type('secretaire789');
    cy.get('#id_password').type('secretairepassword');
    cy.get('#submit').click();
  })
})