import { getMeunMatcheys } from './SiderMenu';

const meun = ['/dashboard', '/userinfo', '/dashboard/name', '/userinfo/:id', '/userinfo/:id/info'];

describe('test meun match', () => {

  it('Parameter path', () => {
    expect(getMeunMatcheys(meun, '/userinfo/2144')).toEqual(['/userinfo/:id']);
  });

});
