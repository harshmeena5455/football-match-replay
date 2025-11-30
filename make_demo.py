from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.football_data import FootballData
import numpy as np
import os

class DemoRecorder:
    def __init__(self):
        self.data = FootballData()
    
    def record_demo(self):
        frames = []
        print("🎥 Recording 15s demo GIF...")
        
        for frame_idx in range(0, 375, 5):  # 15 seconds
            t = frame_idx / 25.0
            
            plt.figure(figsize=(14, 10))
            plt.xlim(0, 1)
            plt.ylim(0, 1)
            plt.gca().set_facecolor('darkgreen')
            plt.title(f"Football Match Replay | Time: {t:.1f}s", color='white', fontsize=16)
            
            # Pitch
            plt.axhline(0.5, color='white', lw=5)
            plt.axvline(0.5, color='white', lw=5)
            
            # Players
            frame_data = self.data.get_frame(t)
            for player_id, (x, y) in frame_data.items():
                if player_id == 'ball':
                    plt.scatter(x, y, c='white', s=300, edgecolors='black', linewidth=2, zorder=10)
                else:
                    color = 'blue' if player_id.startswith('H') else 'red'
                    plt.scatter(x, y, c=color, s=150, edgecolors='white', linewidth=1, zorder=5)
                    plt.text(x, y+0.02, player_id, ha='center', va='bottom', 
                            fontsize=12, color=color, weight='bold', zorder=6)
            
            plt.axis('off')
            plt.tight_layout(pad=0)
            
            # Save frame → PIL → array
            plt.savefig('temp_frame.png', dpi=100, bbox_inches='tight', pad_inches=0)
            img = Image.open('temp_frame.png')
            frames.append(np.array(img))
            
            plt.close('all')
            os.remove('temp_frame.png')
            print(f"Frame {len(frames)}/75 ✓")
        
        # FIXED: Resize + PIL GIF save
        frames = [Image.fromarray(frame).resize((1200, 800)) for frame in frames]
        frames[0].save('demo.gif', save_all=True, append_images=frames[1:], 
                      duration=50, loop=0, optimize=True)
        print("✅ demo.gif SAVED!")
        print(f"📁 File size: {os.path.getsize('demo.gif')/1024/1024:.1f} MB")

if __name__ == "__main__":
    recorder = DemoRecorder()
    recorder.record_demo()
