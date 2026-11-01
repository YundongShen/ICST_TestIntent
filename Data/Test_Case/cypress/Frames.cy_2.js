
describe('Frames',()=>{

it('iFrame 2 using custom command',()=>{
    cy.visit('https://the-internet.herokuapp.com/iframe');

    cy.getIframe('#mce_0_ifr').type("Hello {cmd+a}");       
    cy.get("[aria-label='Bold']").click();
    
})


})
