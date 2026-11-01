const { getSizes, getVariances, getSeed } = require('./opts');

describe('themer-wallpaper-trianglify options', () => {
  it('should parse a single resolution option', () => {
    expect(getSizes('200x200')).toEqual([{ h: 200, w: 200 }]);
  });
});
