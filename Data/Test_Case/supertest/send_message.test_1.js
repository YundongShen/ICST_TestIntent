const createServer = require("./App")
const request = require("supertest");
const app = require("./App");

describe('POST /send-message', function() {
    it('responds with json', function(done) {
      request(app)
        .post('/send-message')
        .send({name: 'john'})
        .set('Accept', 'application/json')
        .expect('Content-Type', /json/)
        .expect(400, done);
    });
  });
