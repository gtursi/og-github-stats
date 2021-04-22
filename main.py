import operator
import sys
import requests
from urllib.parse import urlparse, parse_qsl

GH_MAX_PAGE_SIZE = 100


def get_github_organization_stats(organization, number_of_biggest_repos=5, number_of_biggest_contributors=5):
    if not isinstance(organization, str) or not organization.strip():
        raise ValueError('organization is required and must be a string')

    repos = _get_repos(organization)

    repos_with_more_commits = _get_repos_with_more_commits(organization, repos, number_of_biggest_repos)

    biggest_contributors_per_repo = _get_biggest_contributors_per_repo(organization, repos_with_more_commits.keys(),
                                                                       number_of_biggest_contributors)

    return {"repos_with_more_commits": repos_with_more_commits,
            "biggest_contributors_per_repo": biggest_contributors_per_repo}


def _get_repos(organization):
    """
    Fetches the repositories for the given GitHub organization.
    Caveat: this version only works for organizations with 100 repositories or fewer. As there is no way to sort the
    results by the number of commits, then it's mandatory to fetch all the repositories.

    :param organization: The organization to fetch the repositories from
    :return: a list with the names of the repositories for the given organization
    """
    query_url = f"https://api.github.com/orgs/{organization}/repos"
    repos = _github_request(query_url, {'type': 'public', 'per_page': GH_MAX_PAGE_SIZE}).json()
    print(f"The organization {organization} has {len(repos)} repositories")
    return list(map(lambda repo: repo['name'], repos))


def _get_repos_with_more_commits(organization, repos, number_of_biggest_repos):
    """
    Given an organization and it repositories, it only returns the repos with more commits and its number of commits

    :param organization: The organization owner of the repositories
    :param repos: The list of repository names that belongs to the organization
    :param number_of_biggest_repos: the number of repos to return, sorted by the descending number of commits
    :return: A sorted dictionary with the repositories with more commits and its numbers of commits
    """
    commits_by_repo = {}

    for repo_name in repos:
        commits_by_repo[repo_name] = _calculate_commits_per_repo(organization, repo_name)

    # The order of dictionaries is guaranteed since Python 3.7
    return dict(sorted(commits_by_repo.items(), key=operator.itemgetter(1), reverse=True)[:number_of_biggest_repos])


def _calculate_commits_per_repo(organization, repo):
    """
    Given an organization and a repo within that organization, it returns the number of commits fot that repo

    :param organization: The organization that owns the repo
    :param repo: The repo to count the number of commits for
    :return: The number of commit for the given organization and repo
    """
    commits_url = f'https://api.github.com/repos/{organization}/{repo}/commits'
    commits_response = _github_request(commits_url, {'page_number': 1, 'per_page': GH_MAX_PAGE_SIZE})
    last_page = 1

    if 'last' in commits_response.links:
        last_page_url = commits_response.links['last']['url']
        last_page_url_query = urlparse(last_page_url).query
        last_page = int(dict(parse_qsl(last_page_url_query))['page'])
        commits_response = requests.request('GET', last_page_url)

    number_of_commits = (last_page - 1) * GH_MAX_PAGE_SIZE + len(commits_response.json())

    print(f"Number of commits for repository {repo}: {number_of_commits}")
    return number_of_commits


def _get_biggest_contributors_per_repo(organization, repos, number_of_biggest_contributors):
    """
    Given a list of repos for an organization, it searches for the biggest contributors for each repo

    :param organization: The organization that owns the repos
    :param repos: A list of repository names belonging to the given organization
    :param number_of_biggest_contributors: the number of contributors to return, sorted by the descending number
    of commits
    :return: A list of dictionaries with the contributor as the key, and the number of commits for that user as the
    value, sorted by its values (number of commits)
    """
    biggest_contributors_per_repo = dict()

    for repo_name in repos:
        query_url = f"https://api.github.com/repos/{organization}/{repo_name}/contributors"
        # by default, results are sorted by descending numbers of commits
        contributors = _github_request(query_url, {'per_page': number_of_biggest_contributors}).json()
        biggest_contributors_per_repo[repo_name] = list(
            map(lambda c: {'contributor': c['login'], 'number_of_commits': c['contributions']}, contributors))

    return biggest_contributors_per_repo


def _github_request(url, params):
    """
    Sends a GET request. It raises an error if the response status code is not 200.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send in the query string for the :class:`Request`.
    """
    response = requests.get(url, params)
    response.raise_for_status()
    return response


if __name__ == "__main__":
    org = sys.argv[1]
    stats = get_github_organization_stats(org, 5, 5)

    print(f"Top 5 repositories with more commits for {org} and top 5 contributors per repository:")

    for repository, repo_commits in stats['repos_with_more_commits'].items():
        print(f"Repository {repository} has {repo_commits} commits")
        print("  Biggest contributors:")
        biggest_contributors = stats['biggest_contributors_per_repo'][repository]
        for contributor_stats in biggest_contributors:
            print(f"    {contributor_stats['contributor']} ({contributor_stats['number_of_commits']} commits)")
