const request = require("supertest");
const app = require("./app");
describe("", () => {

  test("should return wm", async () => {
    await request(app)
      .get("/watermelon")
      .expect(200)
      .expect("watermelon 🐓");
  });
});
