///<reference types="cypress" />

describe('XHR test', () => {

  it('cy.request 03', () => {
    cy.request("https://jsonplaceholder.cypress.io/comments")
    .its('headers')
    .its('content-type')
    .should('include', 'application/json');

    cy.request("https://jsonplaceholder.cypress.io/comments")
    .its('status')
    .should('eq', 200);
  });

});
