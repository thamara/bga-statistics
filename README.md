# Board Game Arena Statistics

TODO

## Setting environment
Create a venv or similar, source it and install the requirements dependencies:

```bash
$ python3 -m venv <your_venv>
$ source <your_venv>/bin/activate # or execute <your_venv>\Scripts\activate on Windows
$ pip3 install -r requirements.txt
```

## Running the main application
Change the `player_id` in `main.py` to your player id.
Just run the main python script and it will generate a file `stats.html` under `output` with your Statistics.

```bash
python3 main.py
```

## Running the python dashboard
Change the `player_id` in `main.py` to your player id.
To start running the python dashboard, execute:
```bash
streamlit run dashboard.py
```

## Security
To avoid having to input email and password, you can create a file called `.security`, such as:

```json
{
    "email": "example_email@gmail.com",
    "password": "MY_VERY_SECRET_PASSWORD"
}
```

The `.security` file is ignored and not commited.