# Onboarding Guide: ESClientTest.java

## Overview
This document outlines the purpose and behavior of `ESClientTest.java`, a unit test class for the Elasticsearch client integration within the project. This test suite validates the core data access operations performed by the `QueryDAO` component.

## Test Environment and Configuration
Before modifying or running these tests, note the following setup requirements:
- **Framework**: The tests use JUnit 4 with the Spring Test Context (`SpringRunner`).
- **Context**: The application context is loaded via `@SpringBootTest`, specifically initializing `ElasticSearchStarter`.
- **Profile**: Tests run exclusively against the `test` Spring profile (`@ActiveProfiles("test")`). Ensure your local environment or test configuration supports this profile.
- **Execution Order**: Methods are executed alphabetically (`@FixMethodOrder(MethodSorters.NAME_ASCENDING)`). This ordering is critical because later tests depend on the state created by earlier tests.

## What the Tests Verify
The suite validates four distinct scenarios involving the `QueryDAO` interface and the `Document` entity:

1.  **Indexing (testA)**: Verifies that a new `Document` instance can be successfully indexed. The test asserts that the `indexRequest` method returns a non-null result.
2.  **Full Retrieval (testB)**: Confirms that the `matchAllQuery` method returns a non-empty list immediately after indexing. This ensures data persistence and basic retrieval functionality.
3.  **Wildcard Search (testC)**: Validates search capabilities using wildcards. It checks that a query for the pattern "akd" (matching the surname "Akdoan" from the test data) returns results.
4.  **Cleanup and Verification (testD)**: This is a destructive test designed to reset the state. It retrieves all documents, iterates through them to delete each one by ID, and calls `refreshRequest` to ensure the index is updated. Finally, it asserts that `matchAllQuery` returns an empty list, confirming successful deletion.

## Key Dependencies and Entities
- **QueryDAO**: The primary Data Access Object under test. It handles indexing, querying, deletion, and index refreshing.
- **Document**: The entity class representing data stored in Elasticsearch. The test initializes a specific document with the name "Hseyin Akdoan" and content "Hello!".
- **ElasticSearchStarter**: The configuration class required to boot the test context.

## Important Considerations for Developers
- **State Dependency**: Because tests run in alphabetical order, `testD` clears the database. If you add new tests, ensure they do not assume data exists after `testD` runs, or place them before `testD` in the naming sequence.
- **IO Handling**: `testD` declares `throws IOException`. Be aware that file system or network operations related to Elasticsearch may throw exceptions during deletion or refresh cycles.
- **Data Isolation**: The test suite does not appear to use database transaction rollbacks between methods. The cleanup in `testD` is manual. When adding new tests, consider how they interact with this manual cleanup to avoid flaky tests.
