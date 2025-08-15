from pathlib import Path
import pandas as pd
import numpy as np  
pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.options.display.width = 0

troot_folder = Path("Files")
troot_folder.mkdir(parents=True, exist_ok=True) 

tcsv_game_files = [file for file in troot_folder.glob("*.csv") if not file.name.startswith("merged")]
if not tcsv_game_files:
    raise FileNotFoundError("No CSV files found in the 'Files/' directory.")

trackman_games = pd.concat((pd.read_csv(file).drop(columns=['Notes'], errors='ignore') for file in tcsv_game_files), ignore_index=True)
trackman_games = trackman_games.drop(columns=['Notes', 'Runner1st', 'Runner2nd', 'Runner3rd'], errors='ignore')

if "OutsOnPlay" in trackman_games.columns and "KorBB" in trackman_games.columns:
    trackman_games["OutsOnPlay"] = (trackman_games["OutsOnPlay"] + (trackman_games["KorBB"] == "Strikeout").astype(int))



output_path = troot_folder / "merged_trackman_games.csv"
trackman_games.to_csv(output_path, index=False)