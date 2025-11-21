import label_studio_sdk
import pandas as pd
import os

# ---------------------------------------------
# CONFIG
# ---------------------------------------------
LS_URL = "http://localhost:8080"
API_KEY = "435cdf627796163a32a3f8f562bd9c4b7ad315b0"


# ---------------------------------------------
# MAIN
# ---------------------------------------------
ls = label_studio_sdk.Client(url=LS_URL, api_key=API_KEY)
ls.check_connection()

def create_translation_rating_project(lang):
    LANG_DATASETS = {
        "deu": "tmp/multihal_deu_sample.csv",
        "fra": "tmp/multihal_fra_sample.csv",
        "spa": "tmp/multihal_spa_sample.csv",
        "por": "tmp/multihal_por_sample.csv",
        "ita": "tmp/multihal_ita_sample.csv",
    }
    
    # Pick language based on login
    if lang is None:
        raise ValueError(f"No language assigned for user '{lang}'")

    csv_path = LANG_DATASETS[lang]

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Missing dataset: {csv_path}")

    # Create project
    project = ls.start_project(
        title=f"Translation Rating ({lang})",
        description="Rate translation quality on a 1–5 scale.",
        label_config="""
<View>
  <Header value="Instructions" />
  <Text name="instructions" value="">
    Please rate the following translation. Use the scale as a guide for your rating.
    1. Completley unsensical translation
    2. Major semantic mismatches
    3. Partially good translation, an entity could be missing
    4. Acceptable translation with minor deviances but semantics are clear
    5. Perfect translation
  </Text>
  

  <Header value="Reference" />
  <Text name="ref_kg" value="Path: $ref_kg"/>
  <Text name="ref_q" value="Question: $ref_q"/>
  <Text name="ref_a" value="Answer: $ref_a"/>

  <Header value="Translation" />
  <Text name="trans_kg" value="Path: $trans_kg"/>
  <Text name="trans_q" value="Question: $trans_q"/>
  <Text name="trans_a" value="Answer: $trans_a"/>

  <Text name="Break3" value=" "/>
  <Rating name="quality" toName="trans_q" maxRating="5"/>
</View>

"""
    )

    # Import data
    df = pd.read_csv(csv_path)
    project.import_tasks(df.to_dict("records"))

    return project

# Example usage
project = create_translation_rating_project("deu")
print("Project created:", project.id)

# project = create_translation_rating_project("fra")
# print("Project created:", project.id)

# project = create_translation_rating_project("spa")
# print("Project created:", project.id)

# project = create_translation_rating_project("por")
# print("Project created:", project.id)

# project = create_translation_rating_project("ita")
# print("Project created:", project.id)
