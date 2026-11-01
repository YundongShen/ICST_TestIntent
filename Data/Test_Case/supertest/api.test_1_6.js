const request = require('supertest');
const app = require('../server');

describe('Books API', () => {

    // PUT invalid ID
    test('PUT /api/books/:id should return 404 if not found', async () => {
        const res = await request(app)
            .put('/api/books/999')
            .send({ title: "No Book" });

        expect(res.statusCode).toBe(404);
    });

});
