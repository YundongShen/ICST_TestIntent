const request = require('supertest');
const app = require('../server');

describe('Books API', () => {

    // GET invalid ID
    test('GET /api/books/:id should return 404 for invalid ID', async () => {
        const res = await request(app).get('/api/books/999');
        expect(res.statusCode).toBe(404);
    });

});
