# Pizza feedback app (starter)

Type a customer comment and a rating. The app labels the comment (positive or negative),
saves it to a CSV, and shows:
1. how many comments are positive vs negative,
2. the average rating for each label,
3. the comments to read carefully: a positive label with a low rating, or a negative label with a high rating.

## Run it in Colab or locally
    pip install streamlit pandas requests
    streamlit run app.py
The app works without an API key (it uses a crude keyword rule and says so). To use the LLM,
add a free Groq key (no credit card): `GROQ_API_KEY` in Colab Secrets / environment, or in
`.streamlit/secrets.toml` as `GROQ_API_KEY = "..."`. Never put the key in a file you share.

## Your homework: make it about a different business
Pick a business other than pizza delivery. Edit only the lines marked `CHANGE THIS`:
- `labeler.py`: BUSINESS, LABELS (keep it to two), GUIDE (your rules for hard cases)
- `app.py`: TITLE, the rating range, what counts as a low or high rating
- `feedback.csv`: replace with about 20 comments and ratings of your own

Then check: which comments got flagged? Did the flag catch comments you would want to read?
Change one rule in GUIDE and see what changes.

## Deploy (free)
Put the files in a GitHub repo, then create the app on Streamlit Community Cloud and add
GROQ_API_KEY under the app's Secrets. Saved files can disappear when the app restarts, so use the Download CSV button.
