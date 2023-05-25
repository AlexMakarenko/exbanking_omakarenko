# Welcome to exbanking_omakarenko

## To run tests:
- Clone the repository
- You should have Python3
- Install virtual env `python3 -m venv /path/to/new/virtual/environment`
- Activate venv `source <venv>/bin/activate`
- Install dependencies `pip install -r requirements.txt`
- Run tests `pytest -v tests --alluredir=allure_report`

## To open the report:
- [Install allure](https://formulae.brew.sh/formula/allure), on mac it's `brew install allure`
- [Install openjdk](https://formulae.brew.sh/formula/openjdk), on mac it's `brew install openjdk`
- Open the report: `allure serve allure_report`
