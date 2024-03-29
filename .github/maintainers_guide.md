# Maintainers Guide

This document describes tools, tasks and workflow that one needs to be familiar with in order to effectively maintain
this project. If you use this package within your own software as is but don't plan on modifying it, this guide is
**not** for you.

## Tools

### Python (and friends)

We recommend using [pyenv](https://github.com/pyenv/pyenv) for Python runtime management. If you use macOS, follow the following steps:

```zsh
brew update
brew install pyenv
```

Install necessary Python runtimes for development/testing. You can rely on GitHub Actions for testing with various major versions.

```zsh
pyenv install -l | grep -v "-e[conda|stackless|pypy]"

pyenv install 3.9.18 # select the latest patch version
pyenv local 3.9.18

pyenv versions
  system
  3.6.10
  3.7.7
* 3.9.18 (set by /path-to-python-slack-hooks/.python-version)

pyenv rehash
```

Then, you can create a new Virtual Environment this way:

```zsh
python -m venv env_3.9.18
source env_3.9.18/bin/activate
```

## Tasks

### Testing

#### Run All the Unit Tests

If you make some changes to this project, please write corresponding unit tests as much as possible. You can easily run all the tests by running the following scripts.

If this is your first time to run tests, although it may take a bit longer, running the following script is the easiest.

```zsh
./scripts/install_and_run_tests.sh
```

To simply install all the development dependencies for this project.

```zsh
./scripts/install.sh
```

Once you installed all the required dependencies, you can use the following.

```zsh
./scripts/run_tests.sh
./scripts/run_tests.sh tests/scenario_test/test_get_hooks.py
```

To format this project

```zsh
./scripts/format.sh
```

To lint this project

```zsh
./scripts/lint.sh
```

This project uses [pytype](https://google.github.io/pytype/) to check and infers types for your Python code.

```zsh
./scripts/run_pytype.sh
```

#### Develop Locally

If you want to test the package locally you can.

1. Build the package locally
   - Run

     ```zsh
     scripts/build_pypi_package.sh
     ```

   - This will create a `.whl` file in the `./dist` folder
2. Use the built package
   - Example `/dist/slack_cli_hooks-1.2.3-py2.py3-none-any.whl` was created
   - From anywhere on your machine you can install this package to a project with

     ```zsh
     pip install <project path>/dist/slack_cli_hooks-1.2.3-py2.py3-none-any.whl
     ```

### Releasing

#### test.pypi.org deployment

It is possible to deploy this project on <https://test.pypi.org/> in order to try out packaging and deploy related changes

```zsh
./scripts/deploy_to_test_pypi.sh
```

#### Development Deployment

1. Create a branch in which the development release will live:
    - Bump the version number in adherence to [Semantic Versioning](http://semver.org/) and [Developmental Release](https://peps.python.org/pep-0440/#developmental-releases) in `slack_cli_hooks/version.py`
      - Example the current version is `1.2.3` a proper development bump would be `1.3.0.dev0`
      - `.dev` will indicate to pip that this is a [Development Release](https://peps.python.org/pep-0440/#developmental-releases)
      - Note that the `dev` version can be bumped in development releases: `1.3.0.dev0` -> `1.3.0.dev1`
    - Commit with a message including the new version number. For example `1.3.0.dev0` & Push the commit to a branch where the development release will live (create it if it does not exist)
      - `git checkout -b future-release`
      - `git add slack_cli_hooks/version.py`
      - `git commit -m 'version 1.3.0.dev0'`
      - `git push future-release`
    - Create a git tag for the release. For example `git tag 1.3.0.dev0`.
    - Push the tag up to github with `git push origin --tags`

2. Distribute the release
   - Use the latest stable Python runtime
   - `python -m venv .venv`
   - `scripts/deploy_to_prod_pypi.sh`
   - You do not need to create a GitHub release

3. (Slack Internal) Communicate the release internally

#### Production Deployment

1. Create the commit for the release:
   - Bump the version number in adherence to [Semantic Versioning](http://semver.org/) in `slack_cli_hooks/version.py`
   - Commit with a message including the new version number. For example `1.2.3` & Push the commit to a branch and create a PR to sanity check.
     - `git checkout -b 1.2.3-release`
     - `git add slack_cli_hooks/version.py`
     - `git commit -m 'version 1.2.3'`
     - `git push {your-fork} 1.2.3-release`
   - Create a release PR and get an approval from at least one maintainer.
   - Merge in your release PR.

2. Distribute the release
   - Use the latest stable Python runtime
   - `python -m venv .venv`
   - `/scripts/deploy_to_prod_pypi.sh`
   - Create a GitHub release - <https://github.com/slackapi/python-slack-hooks/releases>
   - Click `Draft a new release`
   - Input the new version you set in [version.py](../slack_cli_hooks/version.py) manually as the `choose a tag` input (example `1.2.3`)
   - After you input the new version, click the "Create a new tag: x.x.x on publish" button.
   - Set the "Target" input to the "main" branch.
   - Name the release title after the version tag.
   - Auto-generate the release notes by clicking the "Auto-generate release notes" button.
   - Make any adjustments to generated release notes to make sure they are accessible and approachable and that an end-user with little context about this project could still understand.
   - Publish the release by clicking the "Publish release" button!

3. (Slack Internal) Communicate the release internally
   - Include a link to the GitHub release

4. (Slack Internal) Tweet by @SlackAPI
   - Not necessary for patch updates, might be needed for minor updates, definitely needed for major updates. Include a link to the GitHub release

## Workflow

### Versioning and Tags

This project uses semantic versioning, expressed through the numbering scheme of
[PEP-0440](https://www.python.org/dev/peps/pep-0440/).

### Branches

`main` is where active development occurs. Long running named feature branches are occasionally created for
collaboration on a feature that has a large scope (because everyone cannot push commits to another person's open Pull
Request). At some point in the future after a major version increment, there may be maintenance branches for older major
versions.

### Issue Management

Labels are used to run issues through an organized workflow. Here are the basic definitions:

- `bug`: A confirmed bug report. A bug is considered confirmed when reproduction steps have been
  documented and the issue has been reproduced.
- `enhancement`: A feature request for something this package might not already do.
- `docs`: An issue that is purely about documentation work.
- `tests`: An issue that is purely about testing work.
- `discussion`: An issue that is purely meant to hold a discussion. Typically the maintainers are looking for feedback in this issues.
- `question`: An issue that is like a support request because the user's usage was not correct.

**Triage** is the process of taking new issues that aren't yet "seen" and marking them with a basic level of information
with labels. An issue should have **one** of the following labels applied: `bug`, `enhancement`, `question`,
`needs feedback`, `docs`, `tests`, or `discussion`.

Issues are closed when a resolution has been reached. If for any reason a closed issue seems relevant once again,
reopening is great and better than creating a duplicate issue.

## Everything else

When in doubt, find the other maintainers and ask.
