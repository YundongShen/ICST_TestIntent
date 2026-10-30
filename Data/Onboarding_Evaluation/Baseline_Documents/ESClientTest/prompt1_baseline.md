## Prompt

```text
Below is one test file from the project's test suite. Generate a natural language summary of each test case. 

Use only what the test file shows. Do not invent behavior that is not in the code. Write in English and use no emoji. Each summary should be no more than one paragraph long.

Test file: {file_name}

{source}
```

## Generated Document

The testA method verifies that the indexRequest operation successfully returns a non-null result when attempting to index a new Document instance containing specific name and message fields.

The testB method ensures that executing a match-all query against the database returns a list that is not empty, confirming that data exists in the index prior to deletion operations.

The testC method validates that a wildcard search for the string "akd" successfully retrieves results, confirming that the wildcard query functionality works as expected for partial text matching.

The testD method performs a cleanup sequence by retrieving all documents, deleting each one individually, refreshing the index, and finally asserting that a subsequent match-all query returns an empty list to confirm all data was removed.
