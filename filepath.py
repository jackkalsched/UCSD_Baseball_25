from pathlib import Path
import pandas as pd
import numpy as np  
pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.options.display.width = 0

troot_folder = Path("Files/")

tcsv_game_files = [file for file in troot_folder.glob("*.csv") if not file.name.startswith("merged")]
if not tcsv_game_files:
    raise FileNotFoundError("No CSV files found in the 'Files/' directory.")

trackman_games = pd.concat((pd.read_csv(file).drop(columns=['Notes'], errors='ignore') for file in tcsv_game_files), ignore_index=True)
trackman_games = trackman_games.drop(columns=['Notes'], errors='ignore')

output_path = troot_folder / "merged_trackman_games.csv"
trackman_games.to_csv(output_path, index=False)

df = pd.read_csv(output_path)

df.loc[:, 'OutsOnPlay'] = df.apply(lambda x: x['OutsOnPlay']+1 if x['KorBB'] == 'Strikeout' else x['OutsOnPlay'], axis=1)
output_file_path = troot_folder / "merged_trackman_games.csv"
df.to_csv(output_file_path, index=False)

print(f"Processed data saved to {output_file_path}")
print(df.shape)