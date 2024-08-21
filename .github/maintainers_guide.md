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

This project uses [mypy](https://mypy.readthedocs.io/en/stable/index.html) to check and infers types for your Python code.

```zsh
./scripts/run_mypy.sh
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

[TestPyPI](https://test.pypi.org/) is a separate instance of the Python Package
Index that allows you to try distribution tools and processes without affecting
the real index. This is useful with changes that relate to the package itself,
example the contents of the `pyproject.toml`

The following can be used to deploy this project on <https://test.pypi.org/>.

```zsh

./scripts/deploy_to_test_pypi.sh
```

#### Development Deployment

Deploying a new version of this library to Pypi is triggered by publishing a Github Release.
Before creating a new release, ensure that everything on a stable branch has
landed, then [run the tests](#run-all-the-unit-tests).

1. Create a branch in which the development release will live:
   - Bump the version number in adherence to
     [Semantic Versioning](http://semver.org/) and
     [Developmental Release](https://peps.python.org/pep-0440/#developmental-releases)
     in `slack_bolt/version.py`
     - Example the current version is `1.2.3` a proper development bump would be
       `1.2.3.dev0`
     - `.dev` will indicate to pip that this is a
       [Development Release](https://peps.python.org/pep-0440/#developmental-releases)
     - Note that the `dev` version can be bumped in development releases:
       `1.2.3.dev0` -> `1.2.3.dev1`
   - Commit with a message including the new version number. For example
     `1.2.3.dev0` & Push the commit to a branch where the development release
     will live (create it if it does not exist)
     - `git checkout -b future-release`
     - `git commit -m 'version 1.2.3.dev0'`
     - `git push -u origin future-release`
2. Create a new GitHub Release from the
   [Releases page](https://github.com/slackapi/python-slack-hooks/releases) by
   clicking the "Draft a new release" button.
3. Input the version manually into the "Choose a tag" input. You must use the
   same version found in `slack_bolt/version.py`

   - After you input the new version, click the "Create a new tag: x.x.x on
     publish" button. This won't create your tag immediately.
   - Auto-generate the release notes by clicking the "Auto-generate release
     notes" button. This will pull in changes that will be included in your
     release.
   - Edit the resulting notes to ensure they have decent messaging that are
     understandable by non-contributors, but each commit should still have it's
     own line.
   - Ensure that this version adheres to
     [semantic versioning](http://semver.org/) and
     [Developmental Release](https://peps.python.org/pep-0440/#developmental-releases).
     See [Versioning](#versioning-and-tags) for correct version format.

4. Set the "Target" input to the feature branch with the development changes.
5. Name the release title after the version tag. It should match the updated
   value from `slack_cli_hooks/version.py`!
6. Make any adjustments to generated release notes to make sure they are
   accessible and approachable and that an end-user with little context about
   this project could still understand.
7. Select "Set as a pre-release"
8. Publish the release by clicking the "Publish release" button!
9. After a few minutes, the corresponding version will be available on
   <https://pypi.org/project/slack-cli-hooks/>.
10. (Slack Internal) Communicate the release internally

#### Production Deployment

Deploying a new version of this library to Pypi is triggered by publishing a Github Release.
Before creating a new release, ensure that everything on the `main` branch since
the last tag is in a releasable state! At a minimum,
[run the tests](#run-all-the-unit-tests).

1. Create the commit for the release
   - Bump the version number in adherence to
     [Semantic Versioning](http://semver.org/) in `slack_bolt/version.py`
   - Commit with a message including the new version number. For example `1.2.3`
     & Push the commit to a branch and create a PR to sanity check.
     - `git checkout -b 1.2.3-release`
     - `git commit -m 'version 1.2.3'`
     - `git push {your-fork} 1.2.3-release`
   - Merge in release PR after getting an approval from at least one maintainer.
2. Create a new GitHub Release from the
   [Releases page](https://github.com/slackapi/python-slack-hooks/releases) by
   clicking the "Draft a new release" button.
3. Input the version manually into the "Choose a tag" input. You must use the
   same version found in `slack_bolt/version.py`

   - After you input the version, click the "Create a new tag: x.x.x on publish"
     button. This won't create your tag immediately.
   - Click the "Auto-generate release notes" button. This will pull in changes
     that will be included in your release.
   - Edit the resulting notes to ensure they have decent messaging that are
     understandable by non-contributors, but each commit should still have it's
     own line.
   - Ensure that this version adheres to
     [semantic versioning](http://semver.org/). See
     [Versioning](#versioning-and-tags) for correct version format.

4. Set the "Target" input to the "main" branch.
5. Name the release title after the version tag. It should match the updated
   value from `slack_cli_hooks/version.py`!
6. Make any adjustments to generated release notes to make sure they are
   accessible and approachable and that an end-user with little context about
   this project could still understand.
7. Publish the release by clicking the "Publish release" button!
8. After a few minutes, the corresponding version will be available on
   <https://pypi.org/project/slack-cli-hooks/>.
9. (Slack Internal) Communicate the release internally
   - Include a link to the GitHub release
10. (Slack Internal) Tweet by @SlackAPI
    - Not necessary for patch updates, might be needed for minor updates,
      definitely needed for major updates. Include a link to the GitHub release

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
