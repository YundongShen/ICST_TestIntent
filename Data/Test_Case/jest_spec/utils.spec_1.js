'use strict'

const { expect } = require('chai')
const levenstein = require('./utils')

describe('Utils', () => {
  describe('Levenstein', () => {
    it('should calculate the distance between two identical strings', () => {
      expect(levenstein('aaa', 'aaa')).eq(0)
    })
  })
})
