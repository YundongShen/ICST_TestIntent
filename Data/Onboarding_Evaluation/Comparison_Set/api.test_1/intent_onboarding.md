## Test Suite Overview

**Suite ID:** api.test_1.js

**Test cases:** 8

This suite verifies the core CRUD operations of the Books API, including listing, retrieving, creating, updating, and deleting book resources, while checking for correct status codes on both valid and invalid requests. New team members must note that tests rely on a shared, mutable server state without resetting between cases; specifically, the update and delete tests target the same hardcoded ID (1) and assume that previous operations have not removed or altered this specific record. Consequently, the execution order is critical, and running tests in isolation may cause failures if the required state does not exist. Additionally, the POST test creates a new book but does not verify its persistence or unique ID generation beyond the immediate response.

- **Book Resource CRUD Verification**
  - **Unique Dependencies:** `supertest`, `../server`
  - **List All Books** (dependencies: `supertest`, `../server`)
  - **Get Existing Book** (dependencies: `supertest`, `../server`)
  - **Get Non-Existent Book** (dependencies: `supertest`, `../server`)
  - **Create New Book** (dependencies: `supertest`, `../server`)
  - **Update Existing Book** (dependencies: `supertest`, `../server`)
  - **Update Non-Existent Book** (dependencies: `supertest`, `../server`)
  - **Delete Existing Book** (dependencies: `supertest`, `../server`)
  - **Delete Non-Existent Book** (dependencies: `supertest`, `../server`)

---

## Group 1: List All Books, Get Existing Book, Get Non-Existent Book

**Shared testing question:** Does the API correctly retrieve book resources?

### List All Books
<sub>[api.test_1.js:7-11](api.test_1.js#L7-L11)</sub>

**Test Objects**

`GET /api/books` Interface

**Test Goals**

Verify that calling this interface returns the expected status code and the response body is an array.

**Test Activities**

- Step 1: Send a GET request to `/api/books`.
- Step 2: Check that the status code is 200.
- Step 3: Check that the response body is an array.

### Get Existing Book
<sub>[api.test_1.js:14-18](api.test_1.js#L14-L18)</sub>

**Test Objects**

`GET /api/books/:id` Interface

**Test Goals**

Verify that requesting an existing resource returns a success status code with the correct data.

**Test Activities**

- Step 1: Send a GET request to `/api/books/1`.
- Step 2: Check that the status code is 200.
- Step 3: Check that the `id` field in the returned body is 1.

### Get Non-Existent Book
<sub>[api.test_1.js:21-24](api.test_1.js#L21-L24)</sub>

**Test Objects**

`GET /api/books/:id` API

**Test Goals**

Verify that requesting a non-existent resource returns an error status code.

**Test Activities**

- Step 1: Send a GET request to `/api/books/999`.
- Step 2: Check that the status code is 404.

---

## Group 2: Create New Book

**Shared testing question:** Does the API correctly create a new book resource?

### Create New Book
<sub>[api.test_1.js:27-41](api.test_1.js#L27-L41)</sub>

**Test Objects**

`POST /api/books` API

**Test Goals**

Verify that creating a new book with valid data returns a success response with the correct book information.

**Test Activities**

- Step 1: Construct new book data (title: "Dune", author: "Frank Herbert", genre: "Sci-Fi", copiesAvailable: 4).
- Step 2: Send a POST request to `/api/books`, carrying the above JSON data.
- Step 3: Check that the status code is 201.
- Step 4: Check that the `title` in the returned body is "Dune".

---

## Group 3: Update Existing Book, Update Non-Existent Book

**Shared testing question:** Does the API correctly update existing book resources?

### Update Existing Book
<sub>[api.test_1.js:44-51](api.test_1.js#L44-L51)</sub>

**Test Objects**

`PUT /api/books/:id` API

**Test Goals**

Verify that updating an existing book returns a success status code and the book data is updated.

**Test Activities**

- Step 1: Send a PUT request to `/api/books/1`, with the body containing `{ title: "Updated Title" }`.
- Step 2: Check that the status code is 200.
- Step 3: Check that the `title` in the returned body is "Updated Title".

### Update Non-Existent Book
<sub>[api.test_1.js:54-60](api.test_1.js#L54-L60)</sub>

**Test Objects**

`PUT /api/books/:id` API

**Test Goals**

Verify that updating a non-existent book returns an error.

**Test Activities**

- Step 1: Send a PUT request to `/api/books/999`, with the body containing `{ title: "No Book" }`.
- Step 2: Check that the status code is 404.

---

## Group 4: Delete Existing Book, Delete Non-Existent Book

**Shared testing question:** Does the API correctly delete book resources?

### Delete Existing Book
<sub>[api.test_1.js:63-66](api.test_1.js#L63-L66)</sub>

**Test Objects**

`DELETE /api/books/:id` Interface

**Test Goals**

Verify that deleting an existing book returns a success status code.

**Test Activities**

- Step 1: Send a DELETE request to `/api/books/1`.
- Step 2: Check that the status code is 200.

### Delete Non-Existent Book
<sub>[api.test_1.js:69-72](api.test_1.js#L69-L72)</sub>

**Test Objects**

`DELETE /api/books/:id` Interface

**Test Goals**

Verify that deleting a non-existent book returns an error.

**Test Activities**

- Step 1: Send a DELETE request to `/api/books/999`.
- Step 2: The status code is 404.
