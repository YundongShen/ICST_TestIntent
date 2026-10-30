# Onboarding: Comment Update Test Suite

This document outlines the structure and requirements for the `put.test.js` file, which validates the comment update functionality.

## Purpose
This integration test verifies the `PUT /comment/:id` endpoint. It ensures that authenticated users can successfully update comment content and that the system correctly handles requests with missing data.

## Prerequisites and Setup
- **Dependencies**: The test relies on `supertest` for HTTP requests, `mongodb` for database interaction, and `jsonwebtoken` for authentication.
- **Secret Key**: Authentication uses a hardcoded secret: `tHI$_iSz_a_Very_$trong&_SeCRet_queYZ_fOR_Team32`.
- **Database**: Tests connect to a MongoDB instance via `./dbFunctions`. The suite requires a running database to execute.
- **Server**: The test imports the application instance from `./server`.

## Test Flow
1.  **Initialization (`beforeAll`)**:
    - Establishes a database connection.
    - Creates a test user (`testUser`) in the `users` collection.
    - Posts a new comment to the `/comment` endpoint to generate a valid `testCommentID`.
2.  **Execution**:
    - **Success Case**: Sends a `PUT` request with a valid `content` field. It asserts a `200` status, `application/json` content type, and verifies the database record reflects the new content.
    - **Failure Case**: Sends a `PUT` request without the `content` field. It asserts a `404` status code.
3.  **Cleanup (`afterAll`)**:
    - Deletes the test user and the specific test comment.
    - Closes all MongoDB connections to prevent resource leaks.

## Key Considerations for Developers
- **Authentication**: All requests must include the `Authorization` header with the generated JWT.
- **Data Integrity**: The success test explicitly queries the database to confirm the update persisted, not just that the API returned a success status.
- **Error Handling**: The suite expects a `404` response when required fields (specifically `content`) are omitted.
- **Configuration**: If you encounter `afterEach` errors, ensure `jest` is added to the `env` key in `.eslintrc.json`.
- **Idempotency**: The cleanup function handles errors gracefully but logs them; ensure your changes do not leave orphaned data if the cleanup fails.
