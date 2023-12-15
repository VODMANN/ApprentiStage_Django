describe('Connexion', () => {
  it('passes', () => {
    cy.visit('http://127.0.0.1:8000/');
    cy.get(':nth-child(3) > .nav-link').click();
    cy.get('#id_username').type('enzo');
    cy.get('#id_password').type('enzo');
    cy.get('#submit').click();
  })
})

describe('Création d\'une offre', () => {
  beforeEach(() => {
      cy.visit('http://127.0.0.1:8000/');
      cy.get(':nth-child(3) > .nav-link').click();
      cy.get('#id_username').type('enzo');
      cy.get('#id_password').type('enzo');
      cy.get('#submit').click();
  })
  it('passes', () => {
    cy.visit('http://127.0.0.1:8000/');
    cy.get('#cardsdefault > :nth-child(4) > .card > .card-body > .btn').click();
    cy.get('#filtre_select').select('Offre'); 
    cy.get('#offre_table > .text-center > .btn').click();
    cy.get('.form-entreprise').within(() => {
      cy.get('input[name="titre"]').type('Titre du poste');
      cy.get('input[name="mailRh"]').type('exemple@mail.com');
      cy.get('input[name="duree"]').type('Temps plein');
      cy.get('textarea[name="description"]').type('Description du poste');
      cy.get('textarea[name="competences"]').type('Python, django');
      cy.get('select[name="entreprise"]').select('Entreprise XYZ');
      cy.get('select[name="theme"]').select('Développement Web');
    });
  
    cy.get('.form-actions').within(() => {
      cy.get('button[type="submit"]').click();
    });
    
  })
})