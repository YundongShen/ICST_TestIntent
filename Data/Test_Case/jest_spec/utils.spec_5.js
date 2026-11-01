'use strict'

const { expect } = require('chai')
const levenstein = require('./utils')

describe('Utils', () => {
  describe('Levenstein', () => {
    it('should calculate the distance between mail.com & gnaul.com', () => {
      expect(levenstein('mail.com', 'gnaul.com')).eq(3)
    })
  })
})
