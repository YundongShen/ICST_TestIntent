const request = require('supertest');
const app = require('../server');

describe('Books API', () => {

    // DELETE invalid ID
    test('DELETE /api/books/:id should return 404 if not found', async () => {
        const res = await request(app).delete('/api/books/999');
        expect(res.statusCode).toBe(404);
    });

});
