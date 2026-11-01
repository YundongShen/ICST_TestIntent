const { getSizes, getVariances, getSeed } = require('./opts');

describe('themer-wallpaper-trianglify options', () => {
  it('should parse multiple resolution options', () => {
    expect(getSizes(['100x200', '300x400'])).toEqual([{ w: 100, h: 200}, { w: 300, h: 400 }]);
  });
});
