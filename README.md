# Trigger Workflow

A personal automation project to monitor and trigger actions based on changes in `urls.json` or on a schedule, with optional manual execution and Telegram notifications.

---

## Features

* **Automatic Trigger on JSON Change**: Executes when `urls.json` is modified in the `github-workflow` branch.
* **Scheduled Execution**: Runs every 6 hours automatically.
* **Manual Execution**: Can be triggered via GitHub Actions UI anytime.
* **Telegram Notifications**: Sends alerts using `TELEGRAM_BOT_TOKEN` and `CHAT_ID` environment variables.
* **Python 3.13**: Uses pip dependencies from `requirements.txt`.
* **`uv` Environment**: Uses `uv` to manage virtual environment and package installation.

---

## Branching Strategy

* `main`: Local development branch. Changes here do not trigger workflows.
* `github-workflow`: Automation branch. Workflow lives here. Triggers are active on this branch.

> Manual runs and scheduled runs require the workflow file to exist on the branch. Scheduled runs execute only on the repository’s default branch.

---

## Setup

1. Clone the repository:

```bash
git clone <repo-url>
cd Trigger
```

2. Create and activate `uv` environment:

```bash
uv venv
uv activate
```

3. Install dependencies:

```bash
uv pip install -r requirements.txt
```

---

## Workflow Details

**File:** `.github/workflows/run.yaml`

**Triggers:**

* Push to `urls.json` on `github-workflow` branch
* Scheduled every 6 hours
* Manual execution via GitHub UI

**Job Steps:**

1. Checkout `github-workflow`
2. Setup Python 3.13
3. Install dependencies (`pip install -r requirements.txt`)
4. Run `python src/main.py`

---

## Usage

* Edit `urls.json` in `github-workflow` to trigger workflow automatically.
* Use GitHub Actions UI to run manually.
* Workflow outputs notifications via Telegram based on `main.py` logic.
* Use `uv` for all local virtual environment and dependency management.

---

## Notes

* Treat `github-workflow` as the production branch for automation.
* Keep `main` for local testing and development.
* Workflow runs on Ubuntu (`ubuntu-latest`) with a 10-minute timeout.
