# analysis/reportgenerator.py

from ydata_profiling import ProfileReport
import pandas as pd

def generate_profile_report(df: pd.DataFrame, output_file: str = "data_profile.html") -> str:
    profile = ydata_profiling.ProfileReport(df, title="Data Profile Report", explorative=True)
    profile.to_file(output_file=output_file)
    return output_file
