## Prompt

```text
Below is one test file from the project's test suite. Generate a natural language summary of each test case and the overall test suite. 

Use only what the test file shows. Do not invent behavior that is not in the code. Write in English and use no emoji. Each test case summary should be no more than one paragraph long.

Test file: {file_name}

{source}
```

## Generated Document

### Overall Test Suite Summary
The `ESClientTest` class is a Spring Boot integration test suite designed to validate the core functionalities of an Elasticsearch client implementation, specifically focusing on the `QueryDAO` component. Running against a test profile, the suite verifies the complete lifecycle of document management within an Elasticsearch index. It ensures that documents can be successfully indexed, retrieved using both global and pattern-based queries, and ultimately removed from the system, confirming that the data store is clean after deletion operations.

### Test Case Summaries

**testA**
This test case verifies the ability to index a new document into the Elasticsearch cluster. It creates a `Document` instance with specific field values and passes it to the `indexRequest` method of the `QueryDAO` component. The test asserts that the result of this indexing operation is not null, confirming that the request was successfully processed and returned a valid response object.

**testB**
This test validates the functionality of the `matchAllQuery` method, which is intended to retrieve all documents currently stored in the index. It executes the query and asserts that the resulting list is not empty. This check ensures that the document indexed in the previous test case is persistently stored and can be retrieved without errors.

**testC**
This test case checks the implementation of wildcard search capabilities within the `QueryDAO`. It invokes the `wildcardQuery` method with the search term "akd" and asserts that the returned list of documents is not empty. This confirms that the search logic correctly identifies and returns documents containing the specified substring pattern, such as the surname "Akdoan" from the test data.

**testD**
This test ensures the integrity of the deletion process and the ability to clear the index. It first retrieves all documents using a match-all query, iterates through them to delete each one individually by ID, and then triggers a refresh request to make the changes immediately visible. Finally, it asserts that a subsequent match-all query returns an empty list, verifying that all documents have been successfully removed from the index.
