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

  it('Login com Credenciais Incorretas', () => {
    cy.get('#username').type('invalidUser');
    cy.get('#password').type('invalidPassword');
    cy.get('button[type="submit"]').click();

    cy.get('.flash.error').should('contain', 'Your username is invalid!');
  });

});
