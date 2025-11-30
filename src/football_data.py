import pandas as pd
import numpy as np
from typing import Dict, Tuple
import os

class FootballData:
    def __init__(self):
        # Skip 8 junk header rows
        self.home_tracking = pd.read_csv(
            "data/metrica/data/Sample_Game_1/Sample_Game_1_RawTrackingData_Home_Team.csv",
            skiprows=8, low_memory=False
        )
        self.away_tracking = pd.read_csv(
            "data/metrica/data/Sample_Game_1/Sample_Game_1_RawTrackingData_Away_Team.csv", 
            skiprows=8, low_memory=False
        )
        
        print(f"✅ Home: {len(self.home_tracking)} frames")
        print(f"✅ Away: {len(self.away_tracking)} frames")
        
        self.frame_rate = 25  # Hz
        self.total_duration = len(self.home_tracking) / self.frame_rate
    
    def get_frame(self, timestamp: float) -> Dict[str, Tuple[float, float]]:
        frame_idx = min(int(timestamp * self.frame_rate), len(self.home_tracking) - 1)
        
        home_row = self.home_tracking.iloc[frame_idx]
        away_row = self.away_tracking.iloc[frame_idx]
        
        positions = {}
        
        # Home team players (columns 3-22: Home_1_x, Home_1_y, Home_2_x, Home_2_y...)
        for i in range(11):
            col_start = 3 + i * 2
            x = home_row.iloc[col_start]
            y = home_row.iloc[col_start + 1]
            if pd.notna(x) and pd.notna(y):
                positions[f"H{i+1}"] = (float(x), float(y))
        
        # Away team players (same column structure)
        for i in range(11):
            col_start = 3 + i * 2
            x = away_row.iloc[col_start]
            y = away_row.iloc[col_start + 1]
            if pd.notna(x) and pd.notna(y):
                positions[f"A{i+1}"] = (float(x), float(y))
        
        # Ball (usually last 2 columns)
        ball_x = home_row.iloc[-2] if len(home_row) > 1 else np.nan
        ball_y = home_row.iloc[-1]
        if pd.notna(ball_x) and pd.notna(ball_y):
            positions['ball'] = (float(ball_x), float(ball_y))
            
        return positions

# Test it!
if __name__ == "__main__":
    data = FootballData()
    print(f"Match duration: {data.total_duration/60:.1f} minutes")
    
    # Test different timestamps
    for t in [10.0, 100.0, 500.0]:
        frame = data.get_frame(t)
        print(f"Frame at {t}s: {len(frame)} objects")
        if frame:
            print("Sample:", list(frame.items())[:3])
