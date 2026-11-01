describe('Test Kalkulatora', () => {
  beforeEach(() => {
    cy.visit('http://127.0.0.1:8080'); 
  });

  it('Czyszczenie ekranu', () => {
      cy.get('[data-key="9"]').click();
      cy.get('[data-key="clear"]').click();

      cy.get('.display .input').should('have.text', '');
      cy.get('.display .output').should('have.text', '');
  });
});
