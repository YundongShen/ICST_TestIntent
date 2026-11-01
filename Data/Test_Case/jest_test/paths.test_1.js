import {
  fileviewString,
  pullFileviewString,
  pullTreeviewString,
  treeviewString,
} from './paths'

describe('treeviewString', () => {
  it('returns a string', () => {
    expect(treeviewString({ owner: 'foo', repo: 'bar' })).toBe('foo/bar/tree')
  })
})
