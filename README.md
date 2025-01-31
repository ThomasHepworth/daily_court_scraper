## Daily Court Scraper

A basic web scraper powered by `dlt` that scrapes the daily court schedule from the UK [Xhibit Court List](http://xhibit.justice.gov.uk/court_lists.htm). The scraper runs daily at 6am via a Github action and outputs data in JSONL format to the `data` directory.

## Data Pipeline Overview

This pipeline follows a structured workflow, as illustrated in the diagram below:

![Pipeline Diagram](./docs/images/daily_court_scraper.excalidraw.png)

### Pipeline Stages

1. **Scraper:**
   The pipeline begins by retrieving the daily court schedule from the UK Xhibit Court List. This is handled by a simple Python script that utilises the `requests` and `beautifulsoup4` libraries to scrape the necessary data.

2. **Extract-Load with `dlt`:**
   Once extracted, the raw data is passed to `dlt` for **extraction, normalisation, and loading**. `dlt` processes the scraped information, parses it, and stores it in a structured **JSONL file**.

3. **Transformation with `dbt`:**
   The structured data is then processed using `dbt`, which applies transformations to create a well-defined model for analysis. These transformations are housed in the `court_transformer` directory.

### Orchestration

The **extract-load process is fully automated** using a [GitHub Action that runs daily at 6 AM](./.github/workflows/update-court-data.yml). This action triggers the scraper, passes the data to `dlt` for processing, and outputs the final files to the `court_data` directory. Each dataset is **timestamped**, allowing users to locate the data for a specific day by referencing the corresponding file.

## Getting Started

### Dependency Management

This project utilises a `pyproject.toml` in conjunction with [`uv`](https://docs.astral.sh/uv/) to manage dependencies. The top-level dependencies are defined in the [pyproject.toml](../pyproject.toml) file and can be compiled into a lock file [uv.lock](./uv.lock) using `uv`.

To compile the dependencies, run the following command:
```sh
uv sync pyproject.toml
```

To install the dependencies, run the following command:
```sh
uv pip install -r pyproject.toml --all-extras
```

## Running the Scraper

To execute the scraper, run the following command:

```sh
python3 -m main.py
```

This will retrieve the daily court schedule and store the output in the `court_data` directory.

---

# dbt

The `dbt` project is responsible for transforming the raw data into a structured format. It is located within the `dbt` directory, specifically under the `court_scraper_dbt` folder.

Before running any `dbt` commands, ensure you have installed all necessary dependencies (see the section on [Dependency Management](#dependency-management)). You must also configure the `dbt` profile to connect to the correct database. This profile is defined in the `profiles.yml` file. To point `dbt` to this file, set the `DBT_PROFILES_DIR` environment variable:

```sh
export DBT_PROFILES_DIR='../.dbt'
```

> [!NOTE]
> To persist this setting across terminal sessions, add the export command to your `.bashrc` or `.zshrc` file.

---

## Running dbt

The `dbt` models are located in the `court_transformer` directory and are structured as follows:

- **Staging:** Loads raw data into the database.
- **Transform:** Applies transformations to structure the data for analysis.

To run the transformation models, use:

```sh
dbt run --select court_transformer
```

To run the associated tests for data integrity:

```sh
dbt test --select court_transformer
```

For a more detailed guide on `dbt` commands and functionality, refer to the official [dbt documentation](https://docs.getdbt.com/).

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
- [daily-scraper.yml](./.github/workflows/daily-scraper.yml): Runs the scraper daily at 6am