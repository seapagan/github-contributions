# GitHub Contributions Viewer <!-- omit in toc -->

This is a very small example showing how to view a GitHub user's contributions
to third-party repositories directly from your terminal. Perhaps in the future
this could be expanded to include more features, but for now it is a simple
example.

> [!NOTE]
>
> Due to limitations in the GitHub GraphQL API where it is not possible to
> filter results directly by user, this application retrieves the last 100 pull
> requests and last 50 Issues from contributed Repositories and then filters
> them by the specified user.
>
> This can be slow for larger repositories. It will also mean that older
> contributions may not be displayed on the verbose display, though they will be
> included in the standard list.

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Features

- Retrieve and display contributions to third-party repositories
- Easy-to-use command-line interface
- Uses GitHub's GraphQL API for efficient data retrieval

## Installation

1. Clone this repository:

   ```terminal
   git clone https://github.com/yourusername/github-contributions.git
   cd github-contributions
   ```

2. Install the required dependencies.
   - We use [uv](https://github.com/astral-sh/uv) to manage the dependencies
and virtual environment. To install the dependencies and create a virtual
environment, run the following command:

      ```terminal
      uv sync
      ```

      This will also install the package **LOCALLY** as the `gh-tools`
      command-line tool - in other words only available when you are in the
      activated virtual environment.

      If you don't have `uv` installed, you can install it first using `pipx`
      (preferred) or `pip`:

      ```terminal
      pip install uv
      ```

   - If you prefer to use `pip` directly, you can install the dependencies into
     your **current virtual environment** using:

      ```terminal
      pip install -r requirements.txt
      ```

      It is generally **not recommended** to install packages outside of a
      virtual environment unless you are happy to have your global Python
      environment modified.

## Usage

Before running the application, you need to set up a GitHub personal access token:

1. Create a personal access token on GitHub (Settings -> Developer settings ->
   Personal access tokens)
2. Set the token as an environment variable:

   ```terminal
   export GITHUB_TOKEN=your_token_here
   ```

To run the application:

```terminal
gh-tools contrib -u USERNAME
```

> [!NOTE]
>
> If you have installed this using app `pip` directly, you will need to run the
> application as below instead of `gh-tools`:
>
> ```terminal
> python src/main.py contrib -u USERNAME
> ```

Replace `USERNAME` with the GitHub username you want to check.

## License

The MIT License (MIT)
Copyright (c) 2024 Grant Ramsay

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
