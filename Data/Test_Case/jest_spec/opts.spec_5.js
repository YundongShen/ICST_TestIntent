const { getSizes, getVariances, getSeed } = require('./opts');

describe('themer-wallpaper-trianglify options', () => {
  it('should parse a single variance option', () => {
    expect(getVariances('0.61')).toEqual([0.61]);
  });
});
