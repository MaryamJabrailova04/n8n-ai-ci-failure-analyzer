# n8n Workflow Implementation

## Webhook

**Node Type:** Webhook  
**Purpose:** Receives `workflow_run` events from GitHub.  
**Input:** GitHub webhook payload.  
**Processing:** Accepts the POST request and exposes the payload.  
**Output:** Raw webhook data.  
**Failure Behavior:** Failed requests are handled by the n8n error workflow.

## Is Completed Failure?

**Node Type:** IF  
**Purpose:** Filters only completed failed workflows.  
**Input:** `action`, `workflow_run.conclusion`.  
**Processing:** Checks `action = completed` and `conclusion = failure`.  
**Output:** Failed events continue; all other events stop.  
**Failure Behavior:** Invalid payloads are ignored.

## Extract Run Metadata

**Node Type:** Edit Fields  
**Purpose:** Creates a normalized workflow context.  
**Input:** Repository, owner, run ID, branch, commit SHA, run URL.  
**Processing:** Maps GitHub payload fields into reusable variables.  
**Output:** `owner`, `repository`, `runId`, `workflowName`, `branch`, `commitSha`, `runUrl`.  
**Failure Behavior:** Missing fields cause downstream API requests to fail.

## Get Workflow Jobs

**Node Type:** HTTP Request  
**Purpose:** Retrieves jobs for the failed workflow run.  
**Input:** `owner`, `repository`, `runId`.  
**Endpoint:** `GET /repos/{owner}/{repo}/actions/runs/{run_id}/jobs`  
**Output:** Array of workflow jobs and conclusions.  
**Failure Behavior:** API, permission, or token failures go to the error workflow.

## Split Workflow Jobs

**Node Type:** Split Out  
**Purpose:** Processes each workflow job separately.  
**Input:** `jobs` array.  
**Processing:** Splits the array into individual n8n items.  
**Output:** One item per GitHub Actions job.  
**Failure Behavior:** Empty or invalid arrays stop processing.

## Is Failed Job?

**Node Type:** IF  
**Purpose:** Keeps only failed jobs.  
**Input:** `jobs.conclusion`.  
**Processing:** Checks whether the conclusion is `failure`.  
**Output:** Failed jobs continue to log collection.  
**Failure Behavior:** Non-failed jobs stop.

## Prepare Failed Job Metadata

**Node Type:** Edit Fields  
**Purpose:** Combines job data with workflow metadata.  
**Input:** Job ID, job name, run metadata.  
**Processing:** Preserves context after splitting jobs.  
**Output:** Job and workflow metadata in one object.  
**Failure Behavior:** Missing metadata prevents log retrieval.

## Download Failed Job Log

**Node Type:** HTTP Request  
**Purpose:** Downloads the failed job log.  
**Input:** `owner`, `repository`, `jobId`.  
**Endpoint:** `GET /repos/{owner}/{repo}/actions/jobs/{job_id}/logs`  
**Output:** Failed job log content.  
**Failure Behavior:** API errors, invalid job IDs, or missing permissions trigger the error workflow.

## Sanitize and Limit Log

**Node Type:** Code  
**Purpose:** Removes sensitive data and reduces log size before LLM analysis.  
**Input:** Job log and metadata.  
**Processing:** Removes ANSI codes, masks tokens/secrets, keeps the last 300 lines, and limits content size.  
**Output:** Sanitized log and preserved metadata.  
**Failure Behavior:** Empty logs continue with limited analysis context.

## Analyze CI Failure

**Node Type:** Basic LLM Chain / Gemini Chat Model  
**Purpose:** Produces a structured CI failure analysis.  
**Input:** Sanitized log, repository, job, branch, commit SHA, run URL.  
**Processing:** Requests JSON with summary, category, root cause, evidence, fixes, and confidence.  
**Output:** Structured LLM response.  
**Failure Behavior:** Model or credential errors trigger the error workflow.

## Parse AI Analysis

**Node Type:** Code  
**Purpose:** Validates the LLM JSON response.  
**Input:** Model output and workflow metadata.  
**Processing:** Removes Markdown fences and parses JSON.  
**Output:** Normalized `analysis` object.  
**Failure Behavior:** Creates an `UNKNOWN` fallback analysis for manual review.

## Search Existing Issues

**Node Type:** GitHub / HTTP Request  
**Purpose:** Prevents duplicate issues.  
**Input:** Repository name, run ID, job ID.  
**Processing:** Searches for `n8n-ci-run:{runId}-job:{jobId}` marker.  
**Output:** Existing issue result or empty result.  
**Failure Behavior:** Search errors trigger the error workflow.

## Duplicate Exists?

**Node Type:** IF  
**Purpose:** Decides whether to create a new issue or update an existing one.  
**Input:** Issue search result.  
**Processing:** Checks whether the marker already exists.  
**Output:** Existing issue → comment; no issue → create issue.  
**Failure Behavior:** Unknown search results must not create duplicates.

## Build Issue Content

**Node Type:** Edit Fields  
**Purpose:** Creates the GitHub Issue title and body.  
**Input:** Workflow metadata and parsed AI analysis.  
**Processing:** Formats execution details, evidence, root cause, and remediation steps.  
**Output:** `issueTitle` and `issueBody`.  
**Failure Behavior:** Missing analysis fields remain visible for manual investigation.

## Create Issue

**Node Type:** GitHub  
**Purpose:** Creates a human-reviewable CI failure issue.  
**Input:** Repository, issue title, issue body.  
**Processing:** Creates an issue with `ci-failure`, `automated-analysis`, and `needs-review` labels.  
**Output:** Created GitHub Issue.  
**Failure Behavior:** API or permission errors trigger the error workflow.

## Add Comment

**Node Type:** GitHub  
**Purpose:** Updates an existing issue for duplicate webhook deliveries.  
**Input:** Existing issue number and current event context.  
**Processing:** Adds a comment instead of creating a duplicate issue.  
**Output:** New comment on the existing issue.  
**Failure Behavior:** Update errors trigger the error workflow.

## n8n Workflow Error Handler

**Node Type:** Error Trigger → Edit Fields → Telegram  
**Purpose:** Notifies the operator when the main workflow fails.  
**Input:** Failed execution context.  
**Processing:** Extracts workflow name, failed node, error message, and execution URL.  
**Output:** Telegram alert.  
**Failure Behavior:** Failed alerts remain visible in n8n execution history.
