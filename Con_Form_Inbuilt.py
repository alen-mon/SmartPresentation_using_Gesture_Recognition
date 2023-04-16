import tkinter as tk
from tkinter import filedialog


# Create GUI window for selecting PowerPoint file
def cfInbuilt(file_path):
    import os
    import comtypes.client
    output_folder = 'PNG_Images'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert PowerPoint to PNG
    powerpoint = comtypes.client.CreateObject('Powerpoint.Application')
    powerpoint.Visible = 1
    presentation = powerpoint.Presentations.Open(file_path)
    slide_count = presentation.Slides.Count
    if not presentation:
        return False
    for i in range(slide_count):
        slide = presentation.Slides[i + 1]
        slide.Export(os.path.join(output_folder, f'Slide{i + 1}.png'), 'PNG')

    # Close PowerPoint application
    powerpoint.Quit()
    return True
