const { getSizes, getVariances, getSeed } = require('./opts');

describe('themer-wallpaper-trianglify options', () => {
  it('should throw when an invalid variance option is given', () => {
    expect(() => getVariances('1.1')).toThrow();
    expect(() => getVariances('-1')).toThrow();
    expect(() => getVariances('foo')).toThrow();
  });
});
