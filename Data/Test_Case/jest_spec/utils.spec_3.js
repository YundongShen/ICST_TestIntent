'use strict'

const { expect } = require('chai')
const levenstein = require('./utils')

describe('Utils', () => {
  describe('Levenstein', () => {
    it('should calculate the distance between two similar strings', () => {
      expect(levenstein('gmail.com', 'gnail.com')).eq(1)
    })
  })
})
