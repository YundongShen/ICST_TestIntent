const request = require('supertest');

const app = require('./app.js');

describe('Sanitize configuration object', () => {
    beforeAll(() => {
        global.config = require('./authConfig.js');
    });

    it('should define the config object', () => {
        expect(config).toBeDefined();
    });

});
