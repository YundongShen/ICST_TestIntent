## Test Suite Overview

**Suite ID:** ESClientTest.java

**Test cases:** 4

This suite validates core Elasticsearch operations within the QueryDAO, including indexing, full-text retrieval, wildcard searching, and data cleanup. A critical dependency exists between test cases due to the @FixMethodOrder annotation enforcing execution by name (A through D). TestA populates the index, which TestB and TestC rely on to verify non-empty query results. TestD subsequently clears this shared state by deleting all documents and refreshing the index. Because the tests share a single Spring context and database state, their order is mandatory; running them out of sequence or in parallel will cause failures as later tests expect data created by earlier ones.

- **Elasticsearch Client Operations**
  - **Unique Dependencies:** `com.kodcu`, `lombok`, `org.junit`, `org.springframework`
  - **Verify Indexing Success** (dependencies: `com.kodcu`, `lombok`, `org.junit`, `org.springframework`)
  - **Verify Full Query Data** (dependencies: `com.kodcu`, `lombok`, `org.junit`, `org.springframework`)
  - **Verify Wildcard Query Results** (dependencies: `com.kodcu`, `lombok`, `org.junit`, `org.springframework`)
  - **Verify Deletion and Consistency** (dependencies: `com.kodcu`, `lombok`, `org.junit`, `org.springframework`)

---

## Group 1: Verify Indexing Success, Verify Full Query Data, Verify Wildcard Query Results

**Shared testing question:** Does the Elasticsearch client correctly perform document indexing and retrieval operations?

### Verify Indexing Success
<sub>[ESClientTest.java:35-38](ESClientTest.java#L35-L38)</sub>

**Test Objects**

`QueryDAO.indexRequest` Method

**Test Goals**

Verify that the Elasticsearch indexing operation is successful.

**Test Activities**

- Step 1: Construct a test document.
- Step 2: Call `dao.indexRequest(doc)`.
- Step 3: Assert that the return value is not null.

### Verify Full Query Data
<sub>[ESClientTest.java:40-43](ESClientTest.java#L40-L43)</sub>

**Test Objects**

`QueryDAO.matchAllQuery` Method

**Test Goals**

Verify that a full query returns data and the result list is not empty.

**Test Activities**

- Step 1: Call `dao.matchAllQuery()`.
- Step 2: Assert that the returned list is not empty.

### Verify Wildcard Query Results
<sub>[ESClientTest.java:45-48](ESClientTest.java#L45-L48)</sub>

**Test Objects**

`QueryDAO.wildcardQuery` Method

**Test Goals**

Verify that a wildcard query returns matching results.

**Test Activities**

- Step 1: Call `dao.wildcardQuery("akd")`.
- Step 2: Assert that the returned list is not empty.

---

## Group 2: Verify Deletion and Consistency

**Shared testing question:** Does the Elasticsearch client correctly handle the complete lifecycle of document deletion and index state consistency?

### Verify Deletion and Consistency
<sub>[ESClientTest.java:50-56](ESClientTest.java#L50-L56)</sub>

**Test Objects**

Combination of the `matchAllQuery`, `deleteDocument`, and `refreshRequest` methods of `QueryDAO`

**Test Goals**

Verify that after retrieving all documents, deleting them one by one and refreshing the index, the final full query result is empty, meaning all data has been cleared.

**Test Activities**

- Step 1: Call `dao.matchAllQuery()` to retrieve the list of all documents.
- Step 2: Iterate through the list, calling `dao.deleteDocument(doc.getId())` to delete each document.
- Step 3: Call `dao.refreshRequest()` to refresh the index.
- Step 4: Call `dao.matchAllQuery()` again and assert that the returned list is empty.
