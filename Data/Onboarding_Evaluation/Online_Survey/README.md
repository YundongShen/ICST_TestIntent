# Online survey

These files reproduce the `module-spec-v3` interface and database setup. Cloudflare Pages hosts the site; Supabase handles allocation, draft saving, and submission.

## Files

- `site/`: uploadable static site.
- `database/setup_module_spec_v3.sql`: tables, response validation, allocation functions, and export view.
- `database/open_live_module_spec_v3.sql`: enables formal recruitment after setup.
- `database/export_completed.sql`: selects submitted live responses for this study.

`site/config.js` is a configuration template. The original project's URL and key are not included.

## Deploy another instance

1. Create a Supabase project. Run the complete setup SQL in its SQL Editor.
2. Set the project URL and publishable key in `site/config.js`.
3. Upload the contents of `site/` as a Cloudflare Pages deployment.
4. Use `?mode=test` for trials. Test and live allocation counters are separate.
5. Run the opening SQL when formal collection should start. The root URL uses live mode.

The setup SQL initializes a new study with live collection closed. Re-running it preserves existing response rows and allocation counters.

## Read the records

| Field | Meaning |
| --- | --- |
| `created_at` | The server created the response session |
| `assigned_at` | The server assigned A, B, or C after instructions |
| `submitted_at` | The participant completed final submission |
| `condition` | A, B, or C |
| `roles` and `role_*` | Multiple-selection role answers |
| `testing_experience` | The selected experience category |
| `familiarity_language`, `familiarity_playwright`, `familiarity_html_dom`, `familiarity_css_bootstrap` | Current familiarity items |
| `comprehension_*` | The three comprehension answers and optional explanation |
| `understanding_*`, `extension_*` | Ratings, cannot-judge reasons, and open comments |

The export view retains some older fields for compatibility. The current questionnaire uses the fields listed above. A saved draft is not a completed submission.

The three [standalone HTML copies](../Survey_HTML/) have fixed conditions and keep answers in the browser. They show the questionnaire without connecting to the study database. They do not provide random allocation or online collection.

The participation note provides the researcher's withdrawal contact. Data removal and anonymization are researcher procedures; browser session IDs do not perform them automatically.
