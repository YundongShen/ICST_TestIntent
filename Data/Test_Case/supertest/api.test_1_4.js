const request = require('supertest');
const app = require('../server');

describe('Books API', () => {

    // POST new book
    test('POST /api/books should create a new book', async () => {
        const newBook = {
            title: "Dune",
            author: "Frank Herbert",
            genre: "Sci-Fi",
            copiesAvailable: 4
        };

        const res = await request(app)
            .post('/api/books')
            .send(newBook);

        expect(res.statusCode).toBe(201);
        expect(res.body.title).toBe("Dune");
    });

});
