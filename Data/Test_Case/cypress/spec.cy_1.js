// describe('template spec', () => {
  // it('passes', () => {
    // cy.visit('https://the-internet.herokuapp.com/login')
  // })
// })

describe('Login Tests', () => {
  const baseUrl = 'https://the-internet.herokuapp.com/login';

  beforeEach(() => {
    cy.visit(baseUrl);
  });

  it('Login com Sucesso', () => {
    cy.get('#username').type('tomsmith');
    cy.get('#password').type('SuperSecretPassword!');
    cy.get('button[type="submit"]').click();

    cy.get('.flash.success').should('contain', 'You logged into a secure area!');
  });

});
