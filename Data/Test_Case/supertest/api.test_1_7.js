const request = require('supertest');
const app = require('../server');

describe('Books API', () => {

    // DELETE book
    test('DELETE /api/books/:id should delete a book', async () => {
        const res = await request(app).delete('/api/books/1');
        expect(res.statusCode).toBe(200);
    });

});
