'use strict'

const { expect } = require('chai')
const levenstein = require('./utils')

describe('Utils', () => {
  describe('Levenstein', () => {
    it('should calculate the distance between two different strings', () => {
      expect(levenstein('abc', 'def')).eq(3)
    })
  })
})
