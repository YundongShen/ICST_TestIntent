const request = require("supertest");
const server = require("./server.js");

describe("server.js index route", () => {
  it("should return 200 status code", async () => {
    const response = await request(server).get("/");

    expect(response.status).toEqual(200);
  });

});
