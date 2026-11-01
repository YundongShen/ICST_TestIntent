import { getMeunMatcheys } from './SiderMenu';

const meun = ['/dashboard', '/userinfo', '/dashboard/name', '/userinfo/:id', '/userinfo/:id/info'];

describe('test meun match', () => {

  it('Secondary path', () => {
    expect(getMeunMatcheys(meun, '/dashboard/name')).toEqual(['/dashboard/name']);
  });

});
