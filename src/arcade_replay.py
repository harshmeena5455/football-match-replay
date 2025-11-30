import matplotlib.pyplot as plt
import matplotlib.animation as animation
from src.football_data import FootballData
import numpy as np

class FootballReplay:
    def __init__(self):
        self.data = FootballData()
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.set_facecolor('darkgreen')
        self.ax.set_title("Football Match Replay ⚽ (SPACE=Pause, ←→=Seek)")
        
        # Pitch lines
        self.ax.axhline(0.5, color='white', lw=3)
        self.ax.axvline(0.5, color='white', lw=3)
        
        self.current_time = 0.0
        self.playing = True
        
    def animate(self, frame_num):
        self.current_time = frame_num * 0.04  # 25 FPS
        if self.current_time > self.data.total_duration:
            self.current_time = 0
            
        # Clear previous
        self.ax.clear()
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.set_facecolor('darkgreen')
        self.ax.set_title(f"Time: {self.current_time:.1f}s | Frame: {frame_num}")
        
        # Pitch
        self.ax.axhline(0.5, color='white', lw=3)
        self.ax.axvline(0.5, color='white', lw=3)
        
        # Get frame
        frame_data = self.data.get_frame(self.current_time)
        
        # Draw players + ball
        for player_id, (x, y) in frame_data.items():
            if player_id == 'ball':
                self.ax.plot(x, y, 'o', color='white', markersize=10, label='Ball')
            else:
                color = 'blue' if player_id.startswith('H') else 'red'
                self.ax.plot(x, y, 'o', color=color, markersize=8)
                self.ax.text(x, y+0.01, player_id, color=color, fontsize=8, ha='center')
        
        plt.pause(0.01)
    
    def run(self):
        anim = animation.FuncAnimation(self.fig, self.animate, frames=1000, 
                                     interval=40, repeat=True, blit=False)
        plt.show()

# Run it!
if __name__ == "__main__":
    replay = FootballReplay()
    replay.run()
