# FARM-Authentication

This code is an example FARM (FastAPI, React, MongoDB) project with Authentication.

It was written to accompany the MongoDB developer article "[Adding Authentication to your FARM Stack App](https://developer.mongodb.com/how-to/FARM-Stack-Authentication)". You should probably read that blog post before running the code here, but if you want to get started quickly short instructions are below.

## Installation

Install into your currently active [Python environment](https://docs.python.org/3/tutorial/venv.html) with:

```bash
python3 -m pip install -r requirements.txt
```

## Configuration

You'll need to set the following environment variables before running the project:

```bash
    # The following will work on Linux & OSX:
    export DEBUG_MODE=True
    export DB_URL="mongodb+srv://<username>:<password>@<url>/farmstack?retryWrites=true&w=majority"
    export JWT_SECRET_KEY="<secret value>"
    export REALM_APP_ID="<realm id>"
```

## Run It

Run the code with the following command:

```bash
uvicorn main:app --reload
```
