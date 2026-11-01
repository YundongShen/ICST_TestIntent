///<reference types="cypress" />

describe('XHR test', () => {

  it('cy.request 02', () => {
    cy.request({
      url: "https://jsonplaceholder.cypress.io/comments",
      method: "GET",
    }).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.length(500);
      expect(response).to.have.property('headers')
      expect(response.headers['content-type']).to.eq('application/json; charset=utf-8');
    })
  });

});
