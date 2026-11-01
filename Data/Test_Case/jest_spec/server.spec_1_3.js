const request = require("supertest");
const server = require("./server.js");

describe("server.js index route", () => {

  it("should return a string with expected content", async () => {
    const expected = "Hello City";

    const response = await request(server).get("/");

    expect(response.text).toMatch(expected);
  });
});
