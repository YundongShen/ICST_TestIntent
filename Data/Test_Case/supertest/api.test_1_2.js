const request = require('supertest');
const app = require('../server');

describe('Books API', () => {

    // GET by valid ID
    test('GET /api/books/:id should return a book', async () => {
        const res = await request(app).get('/api/books/1');
        expect(res.statusCode).toBe(200);
        expect(res.body.id).toBe(1);
    });

});
