# github-stats

github-stats is a CLI that calculates some statistics for a given GitHub organization.

Given an organization name, it returns the top 5 repositories having the more commits, and the top 5 developers having
more commits on that repo.

# How to run

It requires Python 3.9 or greater

First, install pip, the Python package manager:

For macOS:

    > python3 -m pip install --user --upgrade pip

Verify that pip is successfully installed:

    > python3 -m pip --version
    pip 21.0.1 from $HOME/Library/Python/3.9/lib/python/site-packages/pip (python 3.9)

Create a virtual environment:

    > python3 -m venv env

Activate the virtual environment:

    > source env/bin/activate

Confirm that you are in the virtual environment:

    > which python
    .../env/bin/python

Install dependencies:

    python3 -m pip install requests

Now you should be able to run the CLI, here is a sample usage:

    python main.py dogecoin

Sample response:

```
Top 5 repositories with more commits for dogecoin and top 5 contributors per repository:

Repository dogecoin has 13532 commits
  Biggest contributors:
    laanwj (4393 commits)
    sipa (1252 commits)
    gavinandresen (1102 commits)
    theuni (515 commits)
    TheBlueMatt (451 commits)
...
Repository gitian.sigs has 106 commits
  Biggest contributors:
    patricklodder (19 commits)
    langerhans (17 commits)
    stapler117 (4 commits)
    leofidus (3 commits)
    PartTimeLegend (1 commits)
```

## Run Tests

    python3 -m pip install pytest

    python -m pytest tests/* 

## Known limitations

* It only works for public organizations as Authentication is out of the scope.
* The request quota is tiny when making unauthenticated requests, thus, the 
  current version it only works for organizations with 100 repositories or fewer. 
  Even though it's pretty simple to support more repositories, it will exceed the request quota sooner than later.
* For time reasons, it lacks of proper test coverage, and the existing tests use real data instead of mocking data.
* At least the following good practices must be applied to consider this code production-ready:
    * Add unit test for edge cases, e.g., an organizations without repositories, or repositories without commits.
    * Regarding OOP, some classes must be created to better represent the model and to isolate the model 
      from the logic that should be encapsulated in services, some model classes could be Organization, Repository, Contributor,
      and a service could be GitHubAPIService, encapsulating the knowledge to access the GitHub API.
    * Replace the print statements by using a logging framework.
    * Add Git pre-hooks that run tests to prevent commits that might break some functionality, and also to 
      prevent commits that might not include proper test coverage.
    * Use some Python standard to manage the dependencies, e.g, having a requirements.txt containing all the dependencies  

      