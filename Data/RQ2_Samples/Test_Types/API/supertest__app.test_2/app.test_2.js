const request = require("supertest");
const app = require("./app");
describe("", () => {

  test("should return wm ", done => {
    request(app)
      .get("/watermelon")
      .expect("watermelon 🐓")
      .expect(200, done);
  });
});
