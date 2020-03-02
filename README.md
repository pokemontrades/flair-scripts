# flair-scripts

## newreddit.py

For migrating /r/pokemontrades flair to new reddit.

### Usage

1. Install Python 3 and PRAW. PRAW installation instructions: https://praw.readthedocs.io/en/latest/getting_started/installation.html
2. Create a Reddit app with option: `script`, redirect URI: `http://localhost:8080`.
3. Save [this script](https://praw.readthedocs.io/en/latest/tutorials/refresh_token.html#refresh-token) to your machine as `refreshtoken.py` and then run `python3 refreshtoken.py`.
4. When prompted by the refresh token script, enter your Reddit app's client ID/secret, and scopes `flair,modflair`. Copy+paste the URL it gives you into your browser and authorize the app with your account.
5. You should now have a refresh token. Add the app info + refresh token to the auth info at the top of `newreddit.py`.
6. Ensure `newreddit.py` is using the correct sub to avoid unwanted changes!
3. `python3 newreddit.py`
