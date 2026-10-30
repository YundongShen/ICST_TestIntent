## Prompt

```text
Generate an Onboarding document, firstly, an overview of the Test Intent, and secondly, information for each Test Case.

Use only what the test file shows. Do not invent behavior that is not in the code. Write in English and use no emoji.

Test file: {file_name}

{source}
```

## Generated Document

# Onboarding Document: ESClientTest.java

## 1. Test Intent Overview

The `ESClientTest` class is a JUnit test suite designed to verify the functionality of the `QueryDAO` component within a Spring Boot application configured for ElasticSearch. The tests run against a specific test profile and utilize a `Document` entity with predefined data ("Hseyin", "Akdoan", "Hello!").

The primary objectives of this test suite are:
*   **Indexing Verification**: To confirm that a new document can be successfully indexed via the `indexRequest` method.
*   **Query Validation**: To ensure that both full-match queries (`matchAllQuery`) and partial wildcard queries (`wildcardQuery`) return non-empty results when data exists.
*   **Deletion and Cleanup**: To verify the ability to retrieve all documents, delete them individually, refresh the index, and confirm that the index is subsequently empty.

The test execution order is explicitly enforced to be alphabetical by method name (`NAME_ASCENDING`) to ensure that data creation (Test A) precedes data retrieval (Tests B and C) and that data cleanup (Test D) occurs last.

---

## 2. Test Case Details

### Test Case: testA
*   **Method Name**: `testA`
*   **Objective**: Verify that the `indexRequest` method successfully processes a document and returns a non-null result.
*   **Preconditions**:
    *   A `Document` object is instantiated with the following fields:
        *   ID: `null`
        *   First Name: "Hseyin"
        *   Last Name: "Akdoan"
        *   Content: "Hello!"
    *   The `QueryDAO` bean is injected.
*   **Execution Steps**:
    1.  Invoke `dao.indexRequest(doc)` passing the pre-instantiated document.
*   **Expected Result**:
    *   The method must return a value that is not `null`.
    *   Assertion used: `assertNotNull`.

### Test Case: testB
*   **Method Name**: `testB`
*   **Objective**: Verify that a "match all" query returns a populated list of documents.
*   **Preconditions**:
    *   The document from `testA` must have been indexed previously (due to alphabetical execution order).
*   **Execution Steps**:
    1.  Invoke `dao.matchAllQuery()`.
    2.  Check if the returned list is empty.
*   **Expected Result**:
    *   The returned list must **not** be empty.
    *   Assertion used: `assertFalse` on the `isEmpty()` check.

### Test Case: testC
*   **Method Name**: `testC`
*   **Objective**: Verify that a wildcard query successfully retrieves documents matching a specific substring.
*   **Preconditions**:
    *   The document from `testA` must exist in the index.
*   **Execution Steps**:
    1.  Invoke `dao.wildcardQuery("akd")`.
    2.  Check if the returned list is empty.
*   **Expected Result**:
    *   The query for the substring "akd" (matching "Akdoan") must return a list that is **not** empty.
    *   Assertion used: `assertFalse` on the `isEmpty()` check.

### Test Case: testD
*   **Method Name**: `testD`
*   **Objective**: Verify the complete deletion of all documents and the subsequent empty state of the index.
*   **Preconditions**:
    *   Documents exist in the index from previous tests.
*   **Execution Steps**:
    1.  Invoke `dao.matchAllQuery()` to retrieve a `List<Document>`.
    2.  Iterate through the list and call `dao.deleteDocument(doc.getId())` for every document found.
    3.  Invoke `dao.refreshRequest()` to ensure the deletion is visible.
    4.  Invoke `dao.matchAllQuery()` again to retrieve the current state of the index.
    5.  Check if the resulting list is empty.
*   **Expected Result**:
    *   After the deletion and refresh cycle, the "match all" query must return an empty list.
    *   Assertion used: `assertTrue` on the `isEmpty()` check.
