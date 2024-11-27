## Daily Court Scraper

A basic web scraper powered by `dlt` that scrapes the daily court schedule from the UK [Xhibit Court List](http://xhibit.justice.gov.uk/court_lists.htm). The scraper runs daily at 6am via a Github action and outputs data in JSONL format to the `data` directory.

## Getting Started

### Dependency Management

This project utilises a `pyproject.toml` in conjunction with [`uv`](https://docs.astral.sh/uv/) to manage dependencies. The top-level dependencies are defined in the [pyproject.toml](../pyproject.toml) file and can be compiled into a lock file [uv.lock](./uv.lock) using `uv`.

To compile the dependencies, run the following command:
```sh
uv sync pyproject.toml
```

To install the dependencies, run the following command:
```sh
uv pip sync pyproject.toml
```

### Linting and Code Formatting

#### Ruff

All linting is orchestrated using `ruff`. A full list of rules can be located within [pyproject.toml](../pyproject.toml).

To run, simply use the following command:
```sh
ruff check && ruff format
```

This will perform both linting and code formatting in a single action. Should you wish for `ruff` to automatically fix any issues, simply include the `--fix` flag.

### CI/CD

GitHub Actions are stored in `.github/workflows/`. Workflows are triggered on different actions.

This project uses the following workflows:
- [lint-and-format.yml](./.github/workflows/lint-and-format.yml): Runs linting and formatting on PRs to main

## Running the Scraper

To run the scraper, simply execute the following command:
```sh
python3 -m main.py
```

This will scrape the daily court schedule and output the data to the `court_data` directory.
