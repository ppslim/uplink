# Third party imports
import pytest

# Local imports.
import uplink
from uplink import utils

# Constants
BASE_URL = "https://api.github.com/"


def _get_url(url):
    return utils.urlparse.urljoin(BASE_URL, url)


@uplink.headers({"Accept": "application/vnd.github.v3.full+json"})
class GitHubService(uplink.Consumer):
    @uplink.get("/users/{user}/repos")
    def get_repos(self, user): pass

    @uplink.Path
    @uplink.Path
    @uplink.Query
    @uplink.get("/repos/{owner}/{repo}/issues")
    def get_issues(self, owner, repo, sort): pass

    @uplink.args(uplink.Path, uplink.Path, uplink.Query)
    @uplink.get("/repos/{owner}/{repo}/pulls")
    def get_pull_requests(self, owner, repo, state): pass


@pytest.fixture
def github_service_and_client(transaction_hook_mock):
    return (
        GitHubService(base_url=BASE_URL, hook=transaction_hook_mock),
        transaction_hook_mock
    )


def test_get_repo(github_service_and_client):
    service, transaction_hook_mock = github_service_and_client
    service.get_repos("prkumar")
    transaction_hook_mock.audit_request.assert_called_with(
        "GET", _get_url("/users/prkumar/repos"), {
            "headers": {
                "Accept": "application/vnd.github.v3.full+json"
            },
        }
    )


def test_get_issues(github_service_and_client):
    service, transaction_hook_mock = github_service_and_client
    service.get_issues("prkumar", "uplink", sort="updated")
    transaction_hook_mock.audit_request.assert_called_with(
        "GET", _get_url("/repos/prkumar/uplink/issues"), {
            "headers": {
                "Accept": "application/vnd.github.v3.full+json"
            },
            "params": {
                "sort": "updated"
            }
        }
    )


def test_get_pull_requests(github_service_and_client):
    service, transaction_hook_mock = github_service_and_client
    service.get_pull_requests("prkumar", "uplink", state="open")
    transaction_hook_mock.audit_request.assert_called_with(
        "GET", _get_url("/repos/prkumar/uplink/pulls"), {
            "headers": {
                "Accept": "application/vnd.github.v3.full+json"
            },
            "params": {
                "state": "open"
            }
        }
    )

