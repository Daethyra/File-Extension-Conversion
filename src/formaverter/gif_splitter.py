import os
from PIL import Image, ImageSequence

def gif_split(gif_path, output_path):
    
    # Get the original GIF filename with extension
    original_gifname = gif_path.split(os.path.sep)[-1]
    
    # Converts gif to list of frames
    with Image.open(gif_path) as img:
        # Create the output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Loop through each frame in the GIF
        for i in range(img.n_frames):
            # Seek to current frame
            img.seek(i)
            
            # Copy frame
            frame = img.copy()
            
            # Save frame as PNG to retain transparency
            frame_filename = f"{original_gifname}_{i:03d}.png"
            frame.save(os.path.join(output_path, frame_filename), format="PNG")
        print(f"Split {img.n_frames} frames from {original_gifname} into {output_path}.")
