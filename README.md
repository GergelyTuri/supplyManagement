# Supply management system

## Description

This is a supply management system for a small lab. It is built using FastApi framework and Streamlit as a front end. 

## Installation

### Requirements

Anaconda is recommended for installation.
The list of the required packages is in the `requirements.txt` file.

## Local Development and Usage

1. activate the environment

### FastApi Development

This command should be run from the root directory of the project.
```bash
uvicorn app.main:app --reload
```

### Streamlit Development

This command should be run from the `/streamlit_app` directory.
```bash
streamlit run app.py
```

## Production setup

### FastApi production

This is currently running on Google Cloud. [The running backend can be found here](https://elegant-tendril-245600.ue.r.appspot.com/).

### Streamlit production

This is currently running on Steramlit Community Cloud. The webapp can be found [here](https://supplymanagement-4ygoqikkk8rwjzzi4esa2h.streamlit.app/).
