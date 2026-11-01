import {
  fileviewString,
  pullFileviewString,
  pullTreeviewString,
  treeviewString,
} from './paths'

describe('fileviewString', () => {
  it('returns a string', () => {
    expect(fileviewString({ owner: 'foo', repo: 'bar' })).toBe('foo/bar/blob')
  })
})
