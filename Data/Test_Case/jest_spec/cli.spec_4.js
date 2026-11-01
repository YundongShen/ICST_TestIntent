const cli = require('./cli')

describe('parseCozyURL', () => {

  it("should throw an error if the url doesn't start with 'http'", async () => {
    const cozyUrl = 'toto.mycozy.cloud'

    try {
      cli.parseCozyURL(cozyUrl)
    } catch (e) {
      expect(e.message).toMatch('Cozy url must start with `http`')
    }
  })
})
