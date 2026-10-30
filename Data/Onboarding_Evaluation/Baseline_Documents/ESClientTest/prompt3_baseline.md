## Prompt

```text
Below is one test file from the project's test suite. Generate a natural language summary of each test case and the overall test suite. 

Use only what the test file shows. Do not invent behavior that is not in the code. Write in English and use no emoji.

Test file: {file_name}

{source}
```

## Generated Document

### Overall Test Suite Summary
The `ESClientTest` class is a Spring Boot integration test suite designed to validate the functionality of an Elasticsearch client and its associated Data Access Object (`QueryDAO`). The tests run against a specific "test" profile and are ordered alphabetically by method name. The suite verifies the complete lifecycle of document management, including indexing a new document, retrieving documents via full-text and wildcard queries, and performing bulk deletion followed by an index refresh to ensure data consistency.

### Test Case Summaries

*   **testA**: Verifies that the `indexRequest` method successfully processes a new `Document` instance containing specific personal details (first name "Hseyin", last name "Akdoan", and content "Hello!") and returns a non-null result, confirming the indexing operation was initiated or completed.

*   **testB**: Confirms that the `matchAllQuery` method functions correctly by retrieving a list of documents that is not empty, ensuring that the document indexed in the previous step is present and searchable in the Elasticsearch index.

*   **testC**: Validates the `wildcardQuery` method by searching for the term "akd". It asserts that the resulting list of documents is not empty, verifying that the search engine correctly identifies the document with the last name "Akdoan" using a partial string match.

*   **testD**: Tests the deletion and refresh workflow. It retrieves all current documents, iterates through them to delete each one individually, and then calls `refreshRequest` to update the index state. Finally, it asserts that a subsequent `matchAllQuery` returns an empty list, confirming that all documents were successfully removed and the index reflects this change immediately.
