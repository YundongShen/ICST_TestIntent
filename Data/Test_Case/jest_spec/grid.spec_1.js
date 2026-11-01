var { Grid } = require('./grid');

describe("Grid", () => {
    describe("creation", () => {
        it('should fail when providing an invalid seed by the length', () => {
            expect(() => Grid.create(3, 3, "1 0 0 1 1 0")).toThrowErrorMatchingSnapshot();
        });
    });

});
