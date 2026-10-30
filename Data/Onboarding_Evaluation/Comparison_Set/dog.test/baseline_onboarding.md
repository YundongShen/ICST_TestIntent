# Onboarding Guide: User Authentication Test Suite

Welcome to the project. This document outlines the structure, behavior, and requirements of the `dog.test.js` file, which validates the user authentication endpoint.

## Test Environment Setup

The test suite relies on an in-memory MongoDB instance to ensure isolation and speed. Before running tests, understand the following setup:

*   **Database**: The suite uses `mongodb-memory-server` to spin up a temporary MongoDB instance.
*   **Lifecycle**:
    *   `beforeAll`: Connects Mongoose to the in-memory server URI.
    *   `afterAll`: Closes the Mongoose connection and stops the server.
*   **Dependencies**: The tests require `supertest` for HTTP requests, `mongoose` for database interaction, `bcrypt` for password hashing, and the main `app` and `User` model files.

## Scope of Testing

This file exclusively tests the `POST /users/connection` endpoint. It verifies the login logic by checking various input scenarios against a pre-seeded user.

### Test Data Preparation

Each test case runs within a `beforeEach` block that performs the following setup:
1.  Defines a test user with the username "Ranni", email "ranni@mail.fr", and password "123".
2.  Hashes the password using `bcrypt` with a salt round of 10.
3.  Creates a document in the `User` collection containing the email, hashed password, a specific hardcoded token (`6lHCyi-6Vg8QDMhR3ZXBKlQNU070hQvS`), and the username.

### Validated Scenarios

The suite contains four specific test cases:

1.  **Successful Login**:
    *   **Input**: Valid email and correct password.
    *   **Expected Output**: HTTP 200 status, `result` set to `true`, and the response body includes the stored `token` and `username`.

2.  **Missing Email**:
    *   **Input**: Password provided, but email is omitted.
    *   **Expected Output**: HTTP 200 status, `result` set to `false`, and an error message: "Missing or empty fields".

3.  **Incorrect Password**:
    *   **Input**: Valid email with an incorrect password ("wrongpassword").
    *   **Expected Output**: HTTP 200 status, `result` set to `false`, and an error message: "User not found or wrong password".

4.  **User Not Found**:
    *   **Input**: Non-existent email with any password.
    *   **Expected Output**: HTTP 200 status, `result` set to `false`, and the same error message as the incorrect password scenario: "User not found or wrong password".

## Key Implementation Details for Developers

*   **Response Structure**: All responses, whether successful or failed, return an HTTP 200 status code. Success and failure are distinguished by the `result` boolean field in the JSON body.
*   **Error Handling**: The API does not differentiate between a non-existent user and a wrong password in the error message. Both scenarios return "User not found or wrong password" to prevent user enumeration attacks.
*   **Password Verification**: The application logic must handle password hashing internally. The test sends the plain text password, implying the controller compares the input against the stored hash.
*   **Token Management**: The test assumes the token is pre-generated and stored in the database upon user creation. The login endpoint retrieves and returns this existing token rather than generating a new one.

When modifying the authentication logic, ensure these specific response formats and error messages remain consistent to prevent test failures.
