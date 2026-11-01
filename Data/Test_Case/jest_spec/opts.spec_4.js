const { getSizes, getVariances, getSeed } = require('./opts');

describe('themer-wallpaper-trianglify options', () => {
  it('should throw when a malformed resolution option is given', () => {
    expect(() => getSizes('100xFoo')).toThrow();
  });
});
