# Earlier baseline generation record

This file records the earlier onboarding-style baseline setup. It is retained for the comparison materials.

The current survey condition B uses the summary prompt and generated text in [Baseline_Documents/module.spec/prompt3_baseline.md](Baseline_Documents/module.spec/prompt3_baseline.md). That file is the prompt record for the selected survey baseline.

The earlier baseline was generated from the complete test file with the following prompt:

## Prompt

```text
You are helping a developer who has just joined this project. Below is one test file from the project's test suite.

Write an onboarding document in Markdown that helps this new team member understand the test suite: what it tests and what they should know before working on it.

Use only what the test file shows. Do not invent behavior that is not in the code.
Write in English, use no emoji, and keep it under {max_words} words.

Test file: {file_name}

{source}
```

## Placeholders

| Placeholder   | Value                    |
| ------------- | ------------------------ |
| `{file_name}` | the test file name       |
| `{source}`    | its complete source code |
| `{max_words}` | see **Word limit** below |

## Word limit

For each suite, `{max_words}` is the word count of its Intent Onboarding Document, rounded up to the next multiple of 50. This count uses the Intent version before an overview was added. For example, 452 words gives a 500-word limit.

## Recorded model settings

Baseline generation uses Qwen3.5-27B, with thinking disabled and max_tokens set to 8000, as in the Intent generation setting.
