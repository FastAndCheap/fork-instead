# fork-instead
Let others know that they should instead fork your repository and fix issues locally

## Usage

You can change the response comment message using the `message` option. The default
response comment message is:

`Sorry, this repository is working as intended - please fork this repository and fix any "issues" locally.`

You can toggle responding to issues and pull requests individually by using the
`on-issues` and `on-pull-requests` options.  The default behavior is to run for both
issues and pull requests.

You can also toggle automatically locking the conversation and closing the issue or
pull request using the `auto-lock` and `auto-close` options respectively.  The default
behavior is to both lock and close.

Note that a token with write permissions for issues and/or pull requests is required
(as necessary).

```yaml
name: Remind users that your code is fine as is

on:
  issues:
    types: [opened, reopened]
  pull_request:
    types: [opened]

jobs:
  notify:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write
    steps:
      - uses: FastAndCheap/fork-instead@main
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          on-issues: true
          on-pull-requests: true
          lock: true
          close: true
```
