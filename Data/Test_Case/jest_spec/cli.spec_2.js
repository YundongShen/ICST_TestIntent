const cli = require('./cli')

describe('parseCozyURL', () => {

  it('check if trailing slash is removed', async () => {
    const urlIn = 'https://toto.mycozy.cloud/'

    expect(cli.parseCozyURL(urlIn)).toBe('https://toto.mycozy.cloud')
  })

})
