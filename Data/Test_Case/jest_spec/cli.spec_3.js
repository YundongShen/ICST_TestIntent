const cli = require('./cli')

describe('parseCozyURL', () => {

  it('check if app suffix is removed', async () => {
    const urlIn = 'https://toto-drive.mycozy.cloud/'

    expect(cli.parseCozyURL(urlIn)).toBe('https://toto.mycozy.cloud')
  })

})
