# Supply management system

## Description

This is a supply management system for a small lab. It is built using FastApi framework and Streamlit as a front end. 

## Installation

### Requirements

Anaconda is recommended for installation.
The list of the required packages is in the `requirements.txt` file.

## Local Development and Usage

1. activate the environment

### FastApi

This command should be run from the root directory of the project.
```bash
uvicorn app.main:app --reload
```

### Streamlit

This command should be run from the `/streamlit_app` directory.
```bash
streamlit run app.py
```

## Production setup

### FastApi

This is currently running on Google Cloud.

### Streamlit

This is currently running on Steramlit Community Cloud.
