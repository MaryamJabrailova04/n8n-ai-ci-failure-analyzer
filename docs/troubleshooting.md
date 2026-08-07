Webhook 404
       Cause: The test URL is being used, but the n8n test listener is not active.
          |
          |__ __ Solution: For testing, select "Listen for test event".
                           For production, activate the workflow.




GitHub API 401
       Cause: The token is incorrect or has expired.




GitHub API 403
       Cause: The token does not have "Actions" or "Issues" permissions.
              
              


Job log is empty
      Possible causes: Incorrect job ID
                       GitHub token permissions
                       The response is in binary format
                       Log retention period has expired




AI JSON parse error
     Cause: The model added a Markdown code fence at the beginning of the response.
        |
        |__ __ Solution: The Parse node removes code fences and provides a fallback.
