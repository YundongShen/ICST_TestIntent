import {
  fileviewString,
  pullFileviewString,
  pullTreeviewString,
  treeviewString,
} from './paths'

describe('pullFileviewString', () => {
  it('returns a string', () => {
    expect(
      pullFileviewString({ owner: 'foo', repo: 'bar', pullId: '123' })
    ).toBe('foo/bar/pull/123/blob')
  })
})
