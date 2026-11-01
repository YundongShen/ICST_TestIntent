const { getSizes, getVariances, getSeed } = require('./opts');

describe('themer-wallpaper-trianglify options', () => {
  it('should parse multiple variance options', () => {
    expect(getVariances(['0.333', '0.1', '1'])).toEqual([0.333, 0.1, 1]);
  });
});
