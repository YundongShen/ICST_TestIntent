describe('Test Kalkulatora', () => {
  beforeEach(() => {
    cy.visit('http://127.0.0.1:8080'); 
  });

  it('Mnożenie 6 × 7 = 42', () => {
      cy.get('[data-key="6"]').click();
      cy.get('[data-key="*"]').click();
      cy.get('[data-key="7"]').click();
      cy.get('[data-key="="]').click();

      cy.get('.display .output').should('have.text', '42');
  });

});
