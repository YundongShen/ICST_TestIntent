const request = require('supertest');
const app = require('../server');

describe('Books API', () => {

    // PUT update book
    test('PUT /api/books/:id should update a book', async () => {
        const res = await request(app)
            .put('/api/books/1')
            .send({ title: "Updated Title" });

        expect(res.statusCode).toBe(200);
        expect(res.body.title).toBe("Updated Title");
    });

});
