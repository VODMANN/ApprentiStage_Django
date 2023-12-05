describe('template spec', () => {
  it('passes', () => {
    cy.visit('http://127.0.0.1:8000/');
    cy.get(':nth-child(3) > .nav-link').click();
    cy.get('#id_username').type('enzo');
    cy.get('#id_password').type('enzo');
    cy.get('#submit').click();
  })
})