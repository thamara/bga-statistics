# Board Game Arena Statistics

TODO

## Running

Change the `player_id` in `main.py` to your player id.
Just run the main python script and it will generate a file `stats.html` under `output` with your Statistics.

```bash
./main.py
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