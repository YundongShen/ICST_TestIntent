describe("Test suite - conjunto de pruebas", () => {
    it("Validar pagina de inicio", () =>{
        cy.visit("http://localhost:3000")
        cy.get('.ml-auto.items-center > .flex').click()
        cy.get('#user').should('exist')
        cy.get('#password').should('exist')
        cy.get('.z-0').should('be.visible')
    })
    
    
})
