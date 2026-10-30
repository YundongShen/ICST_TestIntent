# Intent Onboarding Document

The document connects what a test targets, why it exists, and how it exercises the system. Its structure follows the extracted Test Objects, Test Goals, and Test Activities.

| Section | Contents | Purpose |
| --- | --- | --- |
| Test suite overview | File name, test count, short summary, and dependencies | Give a starting point for reading the suite |
| Test-case groups | Cases organized around a shared testing question | Make common goals and relations visible |
| Individual test case | Test name and source location | Let the reader return to the code |
| Test Objects | The elements or behavior targeted by the case | Explain what is tested |
| Test Goals | The intended verification objective | Explain why the case is included |
| Test Activities | The sequence of actions and checks | Explain how the case works |

The `module.spec` document also records visible implementation caveats in its overview. Its per-case goals describe intended checks; readers can inspect the source to see how those checks are implemented.

The current evaluation uses [this fixed document](Comparison_Set/module.spec/intent_onboarding.md). It is shown beside the same code used in the other two conditions. The study examines comprehension and perceived support for planning a new test.
