import "cypress-xpath"

describe("Amazon",()=>{

it("Email Login",()=>{

cy.visit("https://www.amazon.in/")
cy.get("#nav-link-accountList").trigger('mouseover')
cy.get("#nav-link-accountList").click()
cy.get("[type=email").type('grewal.pukhraj@gmail.com')
cy.get(".a-button-input").click()
cy.get("#ap_password").type("Password@1")
cy.get("#signInSubmit").click()

})

})
