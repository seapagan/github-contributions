"""Example of an application that retrieves GitHub contributions for a user.

Only THIRD PARTY contributions are considered. The user must provide a GitHub
token to authenticate with the GitHub API. The token must be stored in the
GITHUB_TOKEN environment variable.
"""

import os

import requests
import typer

app = typer.Typer()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com/graphql"

QUERY = """
{
  user(login: "%s") {
    repositoriesContributedTo(
      first: 100,
      contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY],
      includeUserRepositories: false
      ) {
      nodes {
        nameWithOwner
        url
      }
    }
  }
}
"""


def get_contributions(username: str) -> list[dict[str, str]]:
    """Get GitHub (third party) contributions for a given user."""
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    query = QUERY % username
    response = requests.post(
        GITHUB_API_URL, json={"query": query}, headers=headers, timeout=10
    )
    response.raise_for_status()
    data = response.json()
    return [
        {"name": repo["nameWithOwner"], "url": repo["url"]}
        for repo in data["data"]["user"]["repositoriesContributedTo"]["nodes"]
    ]


@app.command()
def main(
    username: str = typer.Option(
        ..., "--username", "-u", help="GitHub username"
    ),
) -> None:
    """Print GitHub contributions for a given user."""
    try:
        contributions = get_contributions(username)
        typer.echo(f"\nThird-Party GitHub Contributions for {username}:")
        for repo in contributions:
            typer.echo(f"- {repo['name']} ({repo['url']})")
    except requests.HTTPError as e:
        typer.echo(f"Error: {e}", err=True)
    except KeyError:
        typer.echo(
            "Error: Unable to retrieve contributions. Check the username and "
            "your token.",
            err=True,
        )


if __name__ == "__main__":
    app()
