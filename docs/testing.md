
| Test Case          | Input                           | Expected Result                 |
| ------------------ | ------------------------------- | ------------------------------- |
| Successful CI      | Tests pass                      | No issue is created             |
| Failed test        | Pytest assertion fails          | An issue is created             |
| Dependency failure | Incorrect package version       | Dependency category is assigned |
| Invalid webhook    | Invalid payload                 | Workflow stops                  |
| Duplicate delivery | The same run is received again  | No new issue is created         |
| AI invalid JSON    | Model returns an invalid format | Fallback analysis is used       |
| GitHub API error   | Invalid token                   | Error workflow starts           |
| Secret in log      | Test token appears in the log   | `[REDACTED]` is displayed       |
