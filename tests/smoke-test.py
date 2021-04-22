import pytest

from main import get_github_organization_stats


@pytest.mark.parametrize("organization", [None, ''])
def test_getting_stats_invalid_inputs(organization):
    with pytest.raises(Exception) as expected_exception:
        get_github_organization_stats(organization)
    assert "organization is required and must be a string" in str(expected_exception.value)


@pytest.mark.parametrize("organization", ['dogecoin'])
def test_getting_stats_invalid_inputs(organization):
    stats = get_github_organization_stats(organization)

    assert stats is not None

    assert stats['repos_with_more_commits'] is not None

    # TODO: add test cases for organizations with less than 5 repositories
    assert len(stats['repos_with_more_commits']) == 5

    # TODO: assert that stats matches the expected result (mock data required)

    for repository, repo_commits in stats['repos_with_more_commits'].items():
        assert isinstance(repository, str)
        assert isinstance(repo_commits, int)

        repo_contributors_stats = stats['biggest_contributors_per_repo'][repository]
        assert repo_contributors_stats is not None

        # TODO: add test cases for repos with less than 5
        assert len(repo_contributors_stats) == 5

        # TODO: assert that repo_contributors_stats matches the expected result (mock data required)

        for contributor_stats in repo_contributors_stats:
            assert isinstance(contributor_stats['contributor'], str)
            assert isinstance(contributor_stats['number_of_commits'], int)
