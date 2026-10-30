# Books API Test Suite Onboarding Guide

## Overview
This document provides an overview of the `api.test_1.js` file within the project's test suite. This file contains integration tests for the Books API, verifying the behavior of the server endpoints using `supertest`. The tests ensure that the API correctly handles standard CRUD (Create, Read, Update, Delete) operations and returns appropriate HTTP status codes for both successful requests and error conditions.

## Test Environment and Dependencies
The test file relies on the following setup:
- **Framework**: The tests use the `describe` and `test` functions, indicating the use of Jest or a compatible test runner.
- **HTTP Client**: The `supertest` library is used to simulate HTTP requests against the application.
- **Application Entry**: The tests import the server instance directly from `../server`. This means the tests run against the actual application logic, not a mocked version.
- **Asynchronous Execution**: All test cases are marked as `async`, utilizing `await` to handle promises returned by the HTTP requests.

## Covered Endpoints and Behaviors
The test suite covers the `/api/books` resource with the following specific scenarios:

### 1. Retrieving Books (GET)
- **List All Books**: A `GET` request to `/api/books` is expected to return a `200 OK` status. The response body must be a JavaScript array.
- **Get Single Book**: A `GET` request to `/api/books/:id` (e.g., `/api/books/1`) is expected to return a `200 OK` status. The response body must contain an `id` field matching the requested ID.
- **Invalid ID**: A `GET` request to `/api/books/:id` with a non-existent ID (e.g., `999`) must return a `404 Not Found` status.

### 2. Creating Books (POST)
- **Create New Book**: A `POST` request to `/api/books` must accept a JSON payload containing `title`, `author`, `genre`, and `copiesAvailable`.
- **Success Criteria**: The endpoint must return a `201 Created` status. The response body must include the `title` provided in the request payload.

### 3. Updating Books (PUT)
- **Update Existing Book**: A `PUT` request to `/api/books/:id` (e.g., `/api/books/1`) must accept a JSON payload with updated fields (e.g., `title`).
- **Success Criteria**: The endpoint must return a `200 OK` status. The response body must reflect the updated value.
- **Invalid ID**: A `PUT` request to a non-existent ID (e.g., `999`) must return a `404 Not Found` status.

### 4. Deleting Books (DELETE)
- **Delete Existing Book**: A `DELETE` request to `/api/books/:id` (e.g., `/api/books/1`) must return a `200 OK` status.
- **Invalid ID**: A `DELETE` request to a non-existent ID (e.g., `999`) must return a `404 Not Found` status.

## Key Implementation Details for Developers
Before modifying the server code or adding new tests, note the following constraints and expectations derived from the existing suite:

1.  **Hardcoded IDs**: The tests rely on specific hardcoded IDs. Specifically, ID `1` is assumed to exist for Read, Update, and Delete operations, while ID `999` is assumed to not exist for error handling tests. If the underlying data storage is reset or changed, these tests may fail if ID `1` is not pre-seeded.
2.  **Response Structure**:
    -   List endpoints must return an array.
    -   Single resource endpoints must return an object with an `id` property.
    -   Create and Update endpoints must echo the modified data in the response body.
3.  **Status Codes**:
    -   `200` is used for successful GET, PUT, and DELETE operations.
    -   `201` is strictly required for successful POST operations.
    -   `404` is the standard response for any operation targeting a non-existent resource.
4.  **Request Payloads**: The POST test expects a specific set of fields (`title`, `author`, `genre`, `copiesAvailable`). While the test only asserts on the `title` in the response, the input object structure should be respected to ensure the test passes.

## Running the Tests
To verify your changes, run the test suite using the project's standard test command. Ensure the server is configured to handle the requests defined in `../server` without requiring external database connections if the tests rely on in-memory state or a test database.

## Next Steps
When adding new features to the Books API:
1.  Identify which endpoint is affected.
2.  Write a new `test` block following the existing patterns (using `request(app).method('/path')`).
3.  Assert the expected HTTP status code.
4.  Assert the specific properties in the response body to ensure data integrity.
