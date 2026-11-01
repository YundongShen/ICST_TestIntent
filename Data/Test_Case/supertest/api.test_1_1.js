const request = require('supertest');
const app = require('../server');

describe('Books API', () => {

    // GET all books
    test('GET /api/books should return all books', async () => {
        const res = await request(app).get('/api/books');
        expect(res.statusCode).toBe(200);
        expect(Array.isArray(res.body)).toBe(true);
    });

});
