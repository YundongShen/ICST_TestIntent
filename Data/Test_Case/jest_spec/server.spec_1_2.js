const request = require("supertest");
const server = require("./server.js");

describe("server.js index route", () => {

  it("should return a response in text format", async () => {
    const response = await request(server).get("/");

    expect(response.type).toEqual("text/html");
  });

});
