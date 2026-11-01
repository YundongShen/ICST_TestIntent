describe("Test suite - conjunto de pruebas", () => {
    
    it("Prueba E2E- UnhappyPath", () =>{
        cy.visit("http://localhost:3000")
        cy.get('.ml-auto.items-center > .flex').click()
        cy.get('#user').type('9999999')
        cy.get('#password').type('9999')
        cy.get('.z-0').click()
        cy.get('[data-content=""] > div').should('be.visible')
    })
    
    
})
