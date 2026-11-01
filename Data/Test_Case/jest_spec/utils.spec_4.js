'use strict'

const { expect } = require('chai')
const levenstein = require('./utils')

describe('Utils', () => {
  describe('Levenstein', () => {
    it('should calculate the distance between gmail.com & gnaul.com', () => {
      expect(levenstein('gmail.com', 'gnaul.com')).eq(2)
    })
  })
})
