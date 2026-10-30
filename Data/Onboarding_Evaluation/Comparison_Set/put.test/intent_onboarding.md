## Test Suite Overview

**Suite ID:** put.test.js

**Test cases:** 2

This suite verifies the PUT /comment/:id endpoint's ability to update comments and reject requests missing required content. It relies on a shared MongoDB connection established in beforeAll, which also pre-seeds a user and a comment to generate a test ID used by all cases. The afterAll hook cleans up this specific test data and closes the database. Both tests depend on the comment created during setup, so the suite will fail if that initial data insertion does not complete successfully; the two tests do not depend on each other's order. Note that the second test expects a 404 status for missing content, which may differ from standard validation error codes.

- **Comment Update Validation**
  - **Unique Dependencies:** `supertest`, `mongodb`, `jsonwebtoken`, `./dbFunctions`, `./server`
  - **Valid Comment Update** (dependencies: `supertest`, `mongodb`, `jsonwebtoken`, `./dbFunctions`, `./server`)
  - **Missing Field Rejection** (dependencies: `supertest`, `mongodb`, `jsonwebtoken`, `./dbFunctions`, `./server`)

---

## Group 1: Valid Comment Update, Missing Field Rejection

**Shared testing question:** Does the comment update endpoint correctly handle valid update requests versus requests missing required fields?

### Valid Comment Update
<sub>[put.test.js:73-83](put.test.js#L73-L83)</sub>

**Test Objects**

`PUT /comment/:id` Updates the comment interface.

**Test Goals**

Verify that sending the correct update content with a valid token results in the comment being successfully updated in the database.

**Test Activities**

- Step 1: Before testing, insert a test user into the database, then create a test comment using the `/comment` interface, recording the comment's `_id`.
- Step 2: Send a PUT request to `/comment/{testCommentID}`, including the Authorization header and the new `content` field.
- Step 3: Check that the response status code is 200 and the Content-Type is `application/json`.
- Step 4: Retrieve the comment from the database and verify that `content` has changed to `"music is my life"`.

### Missing Field Rejection
<sub>[put.test.js:85-90](put.test.js#L85-L90)</sub>

**Test Objects**

`PUT /comment/:id` Update comment API

**Test Goals**

Verify that updating a comment without the required `content` field returns an error.

**Test Activities**

- Step 1: Use the same comment ID as the previous test case.
- Step 2: Send a PUT request to `/comment/{testCommentID}`, only passing `commentId`, not `content`.
- Step 3: Check that the response status code is 404.
