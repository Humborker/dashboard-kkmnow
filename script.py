import matplotlib.pyplot as plt  # basic visualisation
import pandas as pd  # pandas
import pyarrow.parquet as pq
import pyarrow as pa  # as online files are stored in parquet, pyarrow is used to bypass need to import native requests and csv libraries
import numpy as np
BLOOD_DATA = "https://storage.data.gov.my/healthcare/blood_donations.parquet"
BLOOD_STATE_DATA = (
    "https://storage.data.gov.my/healthcare/blood_donations_state.parquet"
)
HEALTH_SCREENINGS = "https://storage.data.gov.my/healthcare/pekab40_screenings.parquet"
ORGAN_PLEDGES = "https://storage.data.gov.my/healthcare/organ_pledges_state.parquet"
ORGAN_PLEDGES_STATE = (
    "https://storage.data.gov.my/healthcare/pekab40_screenings_state.parquet"
)
FUNDING = "https://storage.data.gov.my/healthcare/mnha.parquet"
df_blood = pd.read_parquet(BLOOD_DATA)
df_blood_state = pd.read_parquet(BLOOD_STATE_DATA)
df_health_screen = pd.read_parquet(HEALTH_SCREENINGS)
df_organ_pledges = pd.read_parquet(ORGAN_PLEDGES)
df_organ_pledges_state = pd.read_parquet(ORGAN_PLEDGES_STATE)
df_funding = pd.read_parquet(FUNDING)
print("Successful testing!")

