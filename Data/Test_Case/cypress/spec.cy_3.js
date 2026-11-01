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

  it('Validação de Campos Obrigatórios', () => {
    cy.get('button[type="submit"]').click();

    cy.get('.flash.error').should('contain', 'Your username is invalid!');
  });
});
