const request = require('supertest');

const app = require('./app.js');

describe('Ensure routes served', () => {

    beforeAll(() => {
        process.env.NODE_ENV = 'test';
    });

    it('should protect todolist endpoint', async () => {
        const res = await request(app)
            .get('/api');

        expect(res.statusCode).toEqual(401);
    });
});
