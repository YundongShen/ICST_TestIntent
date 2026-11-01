
describe('Frames',()=>{

it('iframe 3 using Iframe plugin',()=>{
    cy.visit('https://the-internet.herokuapp.com/iframe')

    cy.frameLoaded('#mce_0_ifr');           // to load the frame
    cy.iframe('#mce_0_ifr').type("Hello {cmd+a}");
    cy.get("[aria-label='Bold']").click()

})


})
