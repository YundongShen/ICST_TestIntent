const request = require("supertest");
const app = require("./app");
describe("", () => {
  test("should return response 200 and helloo", done => {
    request(app)
      .get("/")
      .expect("Helllooooo")
      .expect(200, done);
  });

});
