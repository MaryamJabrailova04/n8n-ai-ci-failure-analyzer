Developer
   │
   ▼
GitHub Repository
   │
   ▼
GitHub Actions
   │
   ▼
GitHub Webhook
   │
   ▼
n8n
   │
   ├── GitHub REST API
   ├── Google Gemini API
   └── GitHub Issues




Component responsibilities

  - GitHub Actions: Executes CI tests.

  - GitHub Webhook: Publishes workflow completion events.

  - n8n: Orchestrates event validation, log retrieval, sanitization,
         AI analysis, duplicate detection, and issue creation.

  - GitHub REST API: Provides job metadata and logs.

  - Google Gemini: Generates a probable root cause and remediation suggestions.

  - GitHub Issues: Stores the analysis for human review.
