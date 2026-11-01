const request = require('supertest');

const app = require('./app.js');

describe('Sanitize configuration object', () => {
    beforeAll(() => {
        global.config = require('./authConfig.js');
    });

    it('should not contain client Id', () => {
        const regexGuid = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
        expect(regexGuid.test(config.credentials.clientID)).toBe(false);
    });

});
