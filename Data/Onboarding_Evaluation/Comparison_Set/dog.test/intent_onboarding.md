## Test Suite Overview

**Suite ID:** dog.test.js

**Test cases:** 4

This suite verifies the behavior of the POST /users/connection login endpoint, confirming that valid credentials return a token while missing fields, wrong passwords, or non-existent users trigger specific error responses. The tests run against an in-memory MongoDB instance initialized once for the entire suite, with a fresh user account created before each individual test case. Note that all test cases expect an HTTP 200 status code regardless of success or failure; errors are communicated solely through the response body's result and error fields rather than HTTP status codes.

- **Login Interface Validation Suite**
  - **Unique Dependencies:** `supertest`, `mongoose`, `mongodb-memory-server`, `bcrypt`, `./app`, `./models/users`
  - **Valid Credentials Login** (dependencies: `supertest`, `mongoose`, `mongodb-memory-server`, `bcrypt`, `./app`, `./models/users`)
  - **Missing Fields Login** (dependencies: `supertest`, `mongoose`, `mongodb-memory-server`, `bcrypt`, `./app`, `./models/users`)
  - **Incorrect Password Login** (dependencies: `supertest`, `mongoose`, `mongodb-memory-server`, `bcrypt`, `./app`, `./models/users`)
  - **Non-existent User Login** (dependencies: `supertest`, `mongoose`, `mongodb-memory-server`, `bcrypt`, `./app`, `./models/users`)

---

## Group 1: Valid Credentials Login, Missing Fields Login, Incorrect Password Login, Non-existent User Login

**Shared testing question:** How does the login interface handle various authentication scenarios including valid credentials, missing fields, incorrect passwords, and non-existent users?

### Valid Credentials Login
<sub>[dog.test.js:45-57](dog.test.js#L45-L57)</sub>

**Test Objects**

`POST /users/connection` Login Interface

**Test Goals**

Verify that login with correct credentials returns a successful result with a valid token.

**Test Activities**

- Step 1: Create a user before each test.
- Step 2: Send a POST request to `/users/connection` with the correct email address and password.
- Step 3: Check that the status code is 200, `result` in the body is true, and `token` and `username` are consistent with those created.

### Missing Fields Login
<sub>[dog.test.js:59-69](dog.test.js#L59-L69)</sub>

**Test Objects**

`POST /users/connection` Login Interface

**Test Goals**

Verify that login without required fields returns a failure result with an appropriate error message.

**Test Activities**

- Step 1: Send a POST request to `/users/connection`, sending only the password and not the email address.
- Step 2: Check that the status code is 200, `result` is false, and `error` is "Missing or empty fields".

### Incorrect Password Login
<sub>[dog.test.js:71-82](dog.test.js#L71-L82)</sub>

**Test Objects**

POST /users/connection Login Interface

**Test Goals**

Verify that login with an incorrect password fails and returns the appropriate error message.

**Test Activities**

- Step 1: Send a POST request with a correct email address but an incorrect password `"wrongpassword"`.
- Step 2: Check for a 200 status code, `result` of `false`, and `error` of `"User not found or wrong password"`.

### Non-existent User Login
<sub>[dog.test.js:84-95](dog.test.js#L84-L95)</sub>

**Test Objects**

POST /users/connection Login Interface

**Test Goals**

Verify that login with a non-existent email address fails and returns the appropriate error message.

**Test Activities**

- Step 1: Send a POST request with a non-existent email address `"nonexistent@example.com"` and a correct password.
- Step 2: Check for a 200 status code, `result` of `false`, and `error` of `"User not found or wrong password"`.
