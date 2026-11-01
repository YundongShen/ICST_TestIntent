import {
  fileviewString,
  pullFileviewString,
  pullTreeviewString,
  treeviewString,
} from './paths'

describe('pullTreeviewString', () => {
  it('returns a string', () => {
    expect(
      pullTreeviewString({ owner: 'foo', repo: 'bar', pullId: '123' })
    ).toBe('foo/bar/pull/123/tree')
  })
})
