const cli = require('./cli')

describe('parseCozyURL', () => {
  it('check if no trailing slash is present in url', async () => {
    const urlIn = 'https://toto.mycozy.cloud'

    expect(cli.parseCozyURL(urlIn)).toBe('https://toto.mycozy.cloud')
  })

})
