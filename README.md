CI/CD pipeline failures often require engineers to manually open workflow
runs, inspect multiple job logs, identify relevant errors, and create
tracking issues. This process is repetitive and increases mean time to
diagnosis.

This project provides an event-driven automation workflow that receives
failed GitHub Actions workflow events, retrieves the failed job logs,
sanitizes sensitive data, analyzes the failure with an LLM, and creates a
structured GitHub issue for human review.
