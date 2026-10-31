import { describe, expect, it } from "vitest";
import { render, fireEvent } from "@testing-library/vue";

import App from "./App.vue";

describe("App", () => {

  it("count increments correctly", async () => {
    const { getAllByRole } = render(App);

    const initialCountButton = getAllByRole("button").at(0);
    expect(initialCountButton).toBeDefined();
    expect(initialCountButton.innerHTML).toEqual("count is 0");

    await fireEvent.click(initialCountButton);

    expect(initialCountButton.innerHTML).toEqual("count is 1");
  });
});
