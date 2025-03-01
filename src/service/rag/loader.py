import os
from urllib.parse import urlparse

from langchain_community.document_loaders.github import GithubFileLoader

from utils.errors import NotGithubDomainError


class GithubLoader:
    def __init__(self, url: str):
        self.path = self._parse_path(url)
        self.repo = self._parse_repo(url)
        self.loader = None

    def _parse_path(self, url: str):
        return url.split("main/")[-1]

    def _parse_repo(self, url: str):
        parsed_url = urlparse(url)

        if parsed_url.netloc != "github.com":
            raise NotGithubDomainError("invalid domain")

        return parsed_url.path.split("/tree")[0][1:]

    def load(self):
        self.loader = GithubFileLoader(
            access_token=os.getenv("GITHUB_TOKEN"),
            github_api_url="https://api.github.com",
            file_filter=lambda file_path: self.path in file_path,
            branch="main",
            repo=self.repo,
        )

        return self.loader
