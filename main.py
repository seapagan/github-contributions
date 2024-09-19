"""Example of an application that retrieves GitHub contributions for a user.

Only THIRD PARTY contributions are considered. The user must provide a GitHub
token to authenticate with the GitHub API. The token must be stored in the
GITHUB_TOKEN environment variable.
"""

import os

import requests
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com/graphql"

QUERY = """
query($username: String!) {
  user(login: $username) {
    repositoriesContributedTo(
      first: 100,
      contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY],
      includeUserRepositories: false
    ) {
      nodes {
        nameWithOwner
        url
        pullRequests(
            first: 5,
            orderBy: {field: CREATED_AT, direction: DESC},
            states: [OPEN, MERGED]) {
          nodes {
            title
            url
            author {
              login
            }
          }
        }
        issues(
            first: 5,
            orderBy: {field: CREATED_AT, direction: DESC},
            states: [OPEN, CLOSED]) {
          nodes {
            title
            url
            author {
              login
            }
          }
        }
      }
    }
  }
}
"""


def get_contributions(username: str) -> list[dict[str, any]]:
    """Get GitHub (third party) contributions for a given user."""
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    variables = {"username": username}
    response = requests.post(
        GITHUB_API_URL,
        json={"query": QUERY, "variables": variables},
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    return [
        {
            "name": repo["nameWithOwner"],
            "url": repo["url"],
            "prs": [
                {"title": pr["title"], "url": pr["url"]}
                for pr in repo["pullRequests"]["nodes"]
                if pr["author"]["login"] == username
            ],
            "issues": [
                {"title": issue["title"], "url": issue["url"]}
                for issue in repo["issues"]["nodes"]
                if issue["author"]["login"] == username
            ],
        }
        for repo in data["data"]["user"]["repositoriesContributedTo"]["nodes"]
    ]


@app.command()
def main(
    username: str = typer.Option(
        ..., "--username", "-u", help="GitHub username"
    ),
    *,
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed information including PRs and Issues",
    ),
) -> None:
    """Print GitHub contributions for a given user."""
    try:
        contributions = get_contributions(username)

        console = Console(width=120)

        if not verbose:
            # Simple table for non-verbose output
            table = Table(
                title=f"Third-Party GitHub Contributions for {username}"
            )
            table.add_column("Repository", style="cyan")
            table.add_column("URL", style="magenta")

            for repo in contributions:
                table.add_row(repo["name"], repo["url"])

            console.print("\n",table,"\n")
        else:
            # Detailed output for verbose mode
            for repo in contributions:
                table = Table(expand=True)
                table.add_column("Type", style="cyan")
                table.add_column("Title", style="magenta")
                table.add_column("URL", style="green")

                for pr in repo["prs"]:
                    table.add_row("PR", pr["title"], pr["url"])

                for issue in repo["issues"]:
                    table.add_row("Issue", issue["title"], issue["url"])

                panel = Panel(
                    table,
                    title=f"[bold][cyan]Contributions to {repo['name']}",
                    title_align="left",
                    expand=True,
                )
                console.print(panel)
                console.print()  # Add a blank line between repos

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
