## Test Suite Overview

**Suite ID:** sample.test_3.js

**Test cases:** 4

This suite verifies that the application's configuration file is loadable and sanitized to prevent GUID leakage, while also confirming that the main API endpoint rejects unauthenticated requests. New contributors must note that the first test block relies on a `beforeAll` hook to populate a global `config` variable, which subsequent tests in that block depend on. Additionally, the second block sets `NODE_ENV` to 'test' in its `beforeAll` hook and never resets it. The suite uses `supertest` for HTTP assertions and does not mock external services, meaning tests validate actual route behavior against the loaded application instance.

- **Auth Config and API Security**
  - **Unique Dependencies:** `supertest`, `./app.js`, `./authConfig.js`
  - **Load Config Object** (dependencies: `supertest`, `./app.js`, `./authConfig.js`)
  - **Check Client ID Safety** (dependencies: `supertest`, `./app.js`, `./authConfig.js`)
  - **Check Tenant ID Safety** (dependencies: `supertest`, `./app.js`, `./authConfig.js`)
  - **Verify API Auth Enforcement** (dependencies: `supertest`, `./app.js`, `./authConfig.js`)

---

## Group 1: Load Config Object, Check Client ID Safety, Check Tenant ID Safety

**Shared testing question:** Does the application configuration file load correctly and exclude sensitive credentials?

### Load Config Object
<sub>[sample.test_3.js:10-12](sample.test_3.js#L10-L12)</sub>

**Test Objects**

The `authConfig.js` configuration file

**Test Goals**

Confirm that the configuration object can be loaded and defined correctly.

**Test Activities**

- Step 1: Load `authConfig.js` before testing and assign it to the global `config`.
- Step 2: Assert that `config` is not undefined.

### Check Client ID Safety
<sub>[sample.test_3.js:14-17](sample.test_3.js#L14-L17)</sub>

**Test Objects**

The `credentials.clientID` field in `authConfig.js`

**Test Goals**

Verify that the client ID field does not contain a real GUID to prevent sensitive information leakage.

**Test Activities**

- Step 1: Use a GUID regular expression to match `config.credentials.clientID`.
- Step 2: Assert that the match result is false.

### Check Tenant ID Safety
<sub>[sample.test_3.js:19-22](sample.test_3.js#L19-L22)</sub>

**Test Objects**

The `credentials.tenantId` field in `authConfig.js`

**Test Goals**

Verify that the tenant ID field does not contain a real GUID to prevent sensitive information leakage.

**Test Activities**

- Step 1: Use a GUID regular expression to match `config.credentials.tenantId`.
- Step 2: Assert the match result as false.

---

## Group 2: Verify API Auth Enforcement

**Shared testing question:** Does the API endpoint enforce authentication for unauthenticated requests?

### Verify API Auth Enforcement
<sub>[sample.test_3.js:31-36](sample.test_3.js#L31-L36)</sub>

**Test Objects**

`GET /api` API

**Test Goals**

Verify that the API endpoint rejects unauthenticated requests.

**Test Activities**

- Step 1: Set the environment variable `NODE_ENV` to `'test'`.
- Step 2: Send a GET request to `/api`.
- Step 3: Assert the response status code as 401.
