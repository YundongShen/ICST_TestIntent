# Examples
## Example 1: Unit Test Code for the `BugAntSolid` Icon
The following React unit test verifies that the `BugAntSolid` icon component can be rendered without errors and that the rendered element is present in the document.


**React Unit Test for the BugAntSolid Icon**

```jsx
import * as React from "react"
import { cleanup, render, screen } from "@testing-library/react"

import BugAntSolid from "../bug-ant-solid"

describe("BugAntSolid", () => {
  it("should render the icon without errors", async () => {
    render(<BugAntSolid data-testid="icon" />)

    const svgElement = screen.getByTestId("icon")

    expect(svgElement).toBeInTheDocument()

    cleanup()
  })
})
```


This unit test provides a basic instance of Test Intent. It contains one clearly identifiable Test Object, one focused Test Goal, and a short sequence of Test Activities. This simple structure makes it possible to distinguish the entity under verification from the operations and auxiliary elements used to perform the test.

**Test Object.**
The extracted Test Object is the `BugAntSolid` icon component. It is the entity whose behavior is observed through component rendering and the subsequent presence check. Other elements in the artifact support the execution of the test but are not themselves under verification. In particular, `describe` and `it` organize the test structure, while `render`, `screen.getByTestId`, and `toBeInTheDocument()` are used to exercise, locate, and inspect the component. The variable `svgElement` only stores the retrieved element. None of these auxiliary elements constitutes an additional Test Object.

**Test Goal.**
The extracted Test Goal is to verify the correctness of the core rendering function of the `BugAntSolid` icon component. In this test, rendering correctness is assessed through two observable conditions: the component is rendered without raising an error, and the resulting element is present in the document. The test does not examine visual properties beyond these conditions. This goal presents a clear and verifiable quality requirement for the test object.

**Test Activities.**
The extracted Test Activities form an ordered execution sequence. The test first imports `React`, the testing-library utilities, and the component under test. It then defines the test scope through `describe` and `it`, renders the component with a fixed `data-testid`, locates the rendered element, checks that the element is present in the document, and cleans up the rendered test environment. These activities have different roles in the test: some prepare and organize the execution, while others trigger the target behavior, obtain the observation, and evaluate the result.

The `BugAntSolid` component provides the common reference for the Test Goal and Test Activities. The Test Goal states what must be established about the component, while the Test Activities provide the execution and observations used to make that judgment. Together, the three elements give a structured account of the verification expressed by this test. The following examples extend this basic case to more complex object boundaries, non-functional goals, manual test descriptions, and information distributed across related test artifacts.


## Example 2: Integration Test Code for the Admin Index API
The following condensed integration test covers the query and synchronization functions of the Admin Index API. Lifecycle hooks, repeated synchronization cases, and detailed metadata checks are omitted for brevity.


**Condensed Integration Test for the Admin Index API**

```javascript
import { medusaIntegrationTestRunner } from "@medusajs/test-utils"
import { adminHeaders } from "../../../helpers/create-admin-user"
// ...

process.env.ENABLE_INDEX_MODULE = "true"

medusaIntegrationTestRunner({
  testSuite: ({ api }) => {
    // ...
    describe("Admin Index API", () => {
      it("GET /admin/index/details returns valid metadata", async () => {
        const resp = await api.get(
          "/admin/index/details",
          adminHeaders
        )
        expect(resp.status).toEqual(200)
        // ...
      })

      it("POST /admin/index/sync rejects invalid strategy", async () => {
        const resp = await api.post(
          "/admin/index/sync",
          { strategy: "invalid" },
          adminHeaders
        )
        expect(resp.response.status).toEqual(400)
      })
      // ...
    })
  },
})
```


Unlike the unit test in Example 1, this integration test contains multiple endpoints together with framework constructs, request utilities, variables, and environment settings. The example focuses on how Test Objects are distinguished from the auxiliary elements required to execute the test.

**Test Objects.**
The extracted Test Objects are the two API endpoints `GET /admin/index/details` and `POST /admin/index/sync`. The test invokes these endpoints and evaluates their returned behavior. The first endpoint is examined through its response to a metadata query, while the second is examined through its handling of an invalid synchronization strategy. The remaining elements serve auxiliary roles. The constructs `describe` and `it` organize the test cases, and `medusaIntegrationTestRunner` establishes and runs the integration-testing context. They control the structure and execution of the test but do not represent business entities under verification. The methods `api.get` and `api.post` send requests to the endpoints; they provide access to the Test Objects but are not independent verification targets. The matcher `toEqual` evaluates an observed result and is therefore a judgment mechanism rather than the entity being judged. The variable `resp` stores an endpoint response, while `adminHeaders` supplies the request configuration required for authenticated access. Neither element is itself examined by the test. The setting `ENABLE_INDEX_MODULE` enables the required execution environment, but the setting is not a business function verified by this test. The boundary of the Test Objects is therefore determined by the role of each element in verification, not by whether the element appears in the test code.

**Test Goal.**
The extracted Test Goal is to confirm the functional reliability of the Admin Index API in the integrated environment. In the condensed code, this goal is reflected in two representative checks: the details endpoint should return a successful response for a valid metadata request, and the synchronization endpoint should reject an invalid strategy. The complete artifact contains further checks of metadata and synchronization behavior that support the same goal.

**Test Activities.**
At a specific level, the extracted Test Activities include importing the required dependencies, enabling the index module, initializing the integration-test runner, defining the test cases, sending requests to the two endpoints, recording their responses, and validating the returned status values. At a more general level, the same process can be described as configuring the integration environment, exercising the query and synchronization functions of the Admin Index API, and validating the resulting responses. The second description combines related operations but preserves the Test Objects, Test Goal, and execution logic of the first. The level of detail can therefore be adjusted according to the intended use of the extracted Test Intent, provided that the description still explains how the target behavior is triggered, observed, and evaluated.

In this case, the two endpoints define the scope of verification, and the Test Goal expresses the common purpose of examining their behavior in the integrated environment. The Test Activities support this purpose in different ways: request and assertion operations directly exercise and evaluate the endpoints, while framework and configuration operations establish the conditions required for execution. This relationship allows the three elements to remain semantically consistent without requiring every activity to act directly on a Test Object.

## Example 3: k6 Load Test Code for API Performance
The following k6 load test examines the performance and stability of a target API under a specified concurrent workload.


**k6 Load Test for API Performance Verification**

```javascript
import http from "k6/http"
import { sleep, check } from "k6"

export const options = {
  vus: 10,
  duration: "30s",
  thresholds: {
    http_req_duration: ["p(95)<500"],
    http_req_failed: ["rate<0.01"]
  }
}

export default function() {
  const response = http.get(
    "https://test-api.k6.io"
  )

  check(response, {
    "status is 200":
      (r) => r.status === 200,
    "response time is acceptable":
      (r) => r.timings.duration < 500
  })

  sleep(1)
}
```


This example extends the analysis from functional verification to a non-functional testing scenario. The preceding examples examine component rendering and API behavior, whereas this test examines runtime performance under simulated concurrent access. Despite this change in quality focus, the basis for identifying the Test Object remains the same. The target API accessed through `http.get` is the entity whose behavior is exercised and observed. The Test Object is therefore determined by its role in verification, not by whether the test addresses a functional or non-functional property.

The specific forms of the Test Goal and Test Activities change in performance testing, but their semantic roles remain stable. The Test Goal is to verify the performance and stability of the target API under concurrent user access. Instead of describing an expected functional result, it defines quantitative criteria for the configured workload: 10 virtual users over 30 seconds, a 95th-percentile request duration below 500 milliseconds, and a request failure rate below 1%. The Test Activities include load configuration, concurrent user simulation, repeated request execution, response inspection, and quantitative threshold evaluation. These operations differ from those used in functional tests, but they serve the same semantic purpose: they produce the observations required to assess whether the Test Goal is satisfied.

This example distinguishes the semantic structure of Test Intent from the testing techniques used to realize it. Functional and performance tests use different operations and judgment criteria, but both identify an entity under verification, define what must be established about that entity, and specify how the required evidence is obtained. The example therefore supports the use of the same Test Intent structure for both functional and non-functional verification without treating their execution procedures as equivalent.

## Example 4: Manual Test Case for `view-bookmarks`
The following condensed manual test case verifies that a bookmarks file is detected and that its contents are displayed in the expected interface locations. Non-essential details are omitted for brevity.


**Condensed Manual Test Case for view-bookmarks**

```text
Test Case ID: view-bookmarks

Test Case Description:
Verify that a bookmarks file is detected and displayed at the appropriate locations.

Steps/Description:
1. Open the top-level "Bookmarks" menu and select a bookmark from the list.
2. Click "Bookmarks" on the bookmarks or personal toolbar.
3. Open the sidebar and select the "Bookmarks" panel.
4. Select "Manage Bookmarks" from the top-level "Bookmarks" menu.

Expected Results:
1. Bookmarks and folders, including the Personal Toolbar Folder, appear as menu items. A folder menu item has a solid triangle indicating that a submenu is available.
2. Bookmarks have a green ribbon icon, folders have a folder icon, and the Personal Toolbar Folder has a combined icon.
3. The Manage Bookmarks window appears and is populated with bookmarks and folders.
```


Unlike the preceding code-based examples, this test is expressed through a description, a sequence of manual steps, and a set of expected results. The Test Objects are the bookmarks menu, personal toolbar, sidebar panel, Manage Bookmarks window, and the underlying functionality that populates these interfaces with bookmark data. The steps identify where these entities are accessed, while the expected results specify the behaviors and states to be observed. The Test Objects can therefore be identified from their roles in the verification, even though the artifact contains no executable test code.

This example also shows how a general Test Activity can be refined into an executable sequence. For example, checking the bookmarks menu requires the tester to open the top-level menu, select a bookmark, and compare the displayed items and icons with the expected results. The general activity states which part of the interface is to be examined, while the refined steps state how the required observations are obtained. The activity description therefore moves from general to specific without changing its purpose.

The Test Goal is to verify that the bookmarks file is detected and that its contents are displayed correctly at the specified interface locations. This goal covers several Test Objects rather than a single component or endpoint. The activities performed through the menu, toolbar, sidebar, and Manage Bookmarks window produce observations about different Test Objects, but all of these observations contribute to the same Test Goal. This example shows how Test Intent represents a manual test whose verification evidence is distributed across several interface locations without requiring a fixed one-to-one relationship between Test Objects and Test Activities.

## Example 5: Contact Us Form Test with Cucumber and Java Step Definitions
The following excerpts are taken from the Cucumber feature file and Java step definitions for the Contact Us Form test. Non-essential content is omitted for brevity.


**Condensed Cucumber Feature for the Contact Us Form Test**

```gherkin
Feature: Contact Us Form
Scenario: Contact Us Form
Then Verify GET IN TOUCH is visible
# Additional steps omitted
```


**Condensed Java Step Definition for the Contact Us Form Test**

```java
public class ContactUs_StepDefs {
  @Then("Verify GET IN TOUCH is visible")
  public void verify_get_in_touch_is_visible() {
    BrowserUtils.verifyElementDisplayed(
      contactUsPage.getInTouchText
    );
  }
  // Additional definitions omitted
}
```


The Cucumber feature file and the Java step definition serve different purposes. The feature file describes the expected behavior in a readable scenario, while the step definition implements the same behavior as an executable check. The `@Then` annotation connects the scenario step to the corresponding Java method. In both artifacts, the Test Object is the `GET IN TOUCH` element, and the core verification behavior is to check whether this element is visible. Their different forms and uses affect how the verification is described and executed, but do not change its semantic content. This example shows that test artifacts faithfully derived from the same Test Intent preserve the same Test Object and core verification logic.
