import label_studio_sdk
import pandas as pd
import os

# ---------------------------------------------
# CONFIG
# ---------------------------------------------
LS_URL = "http://localhost:8080"
API_KEY = "your_api_key_here"

LANG_DATASETS = {
    "deu": "tmp/multihal_deu_sample.csv",
    "fra": "tmp/multihal_fra_sample.csv",
    "spa": "tmp/multihal_spa_sample.csv",
}

# Map usernames to language
USER_LANGUAGE = {
    "anna": "deu",
    "marie": "fra",
    "carlos": "spa",
}

# ---------------------------------------------
# MAIN
# ---------------------------------------------
ls = label_studio_sdk.Client(url=LS_URL, api_key=API_KEY)
ls.check_connection()

def create_translation_rating_project(username):
    # Pick language based on login
    lang = USER_LANGUAGE.get(username)
    if lang is None:
        raise ValueError(f"No language assigned for user '{username}'")

    csv_path = LANG_DATASETS[lang]

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Missing dataset: {csv_path}")

    # Create project
    project = ls.start_project(
        title=f"Translation Rating ({lang})",
        description="Rate translation quality on a 1–5 scale.",
        label_config="""
<View>
  <Text name="source" value="$source"/>
  <Text name="translation" value="$translation"/>
  <Rating name="quality" toName="translation" maxRating="5"/>
</View>
"""
    )

    # Import data
    df = pd.read_csv(csv_path)
    project.import_tasks(df.to_dict("records"))

    return project

# Example usage
project = create_translation_rating_project("anna")
print("Project created:", project.id)
