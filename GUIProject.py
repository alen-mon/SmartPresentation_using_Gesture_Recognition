import cv2
import pyglet
import requests
from cvzone.HandTrackingModule import HandDetector
import os
import numpy as np
import time
from tkinter import StringVar, filedialog
import subprocess
import customtkinter
from Con_Form_Aspose import cfAspose
from Con_Form_Inbuilt import cfInbuilt
from Con_Form_REST_POST import cfRestPost
from PIL import Image, ImageTk
import tkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("700x600")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=5, padx=15, fill="both", expand=True)


def run_script():
    venv_path = 'venv'  # replace with the actual path to your venv
    script_path = 'main.py'  # replace with the actual path to your Python script
    subprocess.run([f"{venv_path}/Scripts/python", script_path, get_input()])


def upload():
    file_path = filedialog.askopenfilename(filetypes=[("Powerpoint", '.ppt'),
                                                      ("Powerpoint", '.pptx'),
                                                      ("PDF", '.pdf'),
                                                      ("Document", '.doc'),
                                                      ("Document", '.docx')
                                                      ])

    if file_path:
        UploadPath.delete(1.0, customtkinter.END)
        UploadPath.insert(customtkinter.END, file_path)
        return file_path


def reset_button():
    run_button.configure(text="Upload & Run Reformatter", fg_color='light green')


def run_selected_function(selected_function):
    # Call the selected function
    selected_function()


def function_1():
    file_path = upload()
    run_button.configure(text="Waiting.....")
    if (cfRestPost(file_path)):
        print("Option 1 selected" + file_path)
        run_button.configure(text="Success")


def function_2():
    file_path = upload()
    run_button.configure(text="Waiting.....")
    if (cfInbuilt(file_path)):
        print("Option 2 selected" + file_path)
    run_button.configure(text="Success")


def function_3():
    file_path = upload()
    run_button.configure(text="Waiting.....")
    if (cfAspose(file_path)):
        print("Option 2 selected" + file_path)
        run_button.configure(text="Failed", fg_color="red")
        UploadPath.configure(text_color="red")


label = customtkinter.CTkLabel(master=frame, text="Smart Gesture Presentation", font=("Arial", 20))
label.pack(pady=12, padx=10)

frame_reformatter = customtkinter.CTkFrame(frame)
frame_reformatter.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame_reformatter, text="Select and Reformat Your Presentation File",
                               font=("Arial", 20))
label.pack(pady=12, padx=10)

frame_reformatter_combo = customtkinter.CTkFrame(frame_reformatter)
frame_reformatter_combo.pack(pady=20, padx=60, fill="both")


def update_label():
    selected_item = combobox.get()
    if selected_item == "Com_Fom_Rest_Convert":
        label_desc.configure(
            text=f"ONLINE CONVERTER (Recommended) \nHighly compatible and supports many file formats\nSupports :PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX,\n** Processing times may be longer than other methods **")
    elif selected_item == "Com_Fom_Aspose":
        label_desc.configure(
            text=f" OFFLINE LIBRARY , lightweight and fast\n Supports only :PPTX,PPT,PPS,PPA, and ODP \n ** Watermarked if using a free version **")
    elif selected_item == "Com_Fom_Inbuilt":
        label_desc.configure(
            text=f"INBUILT APPLICATION , Very Fast and Operates Offline \nSupports only :PPTX,PPT\n ** Might fail if the Powerpoint installation is unlicensed or corrupted **")
    root.after(500, update_label)


combobox = customtkinter.CTkComboBox(master=frame_reformatter_combo, values=["Com_Fom_Rest_Convert",
                                                                             "Com_Fom_Aspose",
                                                                             "Com_Fom_Inbuilt"], width=200)
combobox.set("Select_Reformatter")
combobox.bind("<<ComboboxSelected>>", lambda event: update_label(combobox.get()))
combobox["state"] = 'readonly'
combobox.pack(side=customtkinter.LEFT, pady=12, padx=10)

run_button = customtkinter.CTkButton(
    master=frame_reformatter_combo,
    text="Upload & Run Reformatter",
    command=lambda: run_selected_function(selected_function=selected_function_mapping[combobox.get()])
)

selected_function_mapping = {
    "Com_Fom_Rest_Convert": function_1,
    "Com_Fom_Aspose": function_2,
    "Com_Fom_Inbuilt": function_3
}
run_button.pack(side=customtkinter.RIGHT, pady=12, padx=10)

UploadPath = customtkinter.CTkTextbox(master=frame_reformatter, height=2, text_color="green")
UploadPath.pack(pady=12, padx=10)
UploadPath["state"] = 'readonly'
UploadPath.insert(customtkinter.END, text="/Path")

label_desc = customtkinter.CTkLabel(master=frame_reformatter, text="...")
label_desc.pack(pady=12, padx=10)
root.after(500, update_label)


class App:
    def __init__(self, window, canvas, video_url):
        self.window = window
        self.canvas = canvas
        self.cap = cv2.VideoCapture(video_url)
        self.update()

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            self.photo = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, image=self.photo, anchor=customtkinter.NW)
            self.window.after(15, self.update)
        else:
            self.cap.release()
            self.canvas.create_text(150, 75, text='Error capturing video!', fill='red', font=('Arial', 14))


frame_Arguments = customtkinter.CTkFrame(frame)
frame_Arguments.pack(side=customtkinter.RIGHT, pady=20, padx=60, fill="both", expand=True)
label = customtkinter.CTkLabel(master=frame_Arguments, text="IP Camera Devices",
                               font=("Arial", 20))
label.pack(pady=12, padx=10)

canvas = customtkinter.CTkCanvas(frame_Arguments, width=100, height=70)
canvas.pack()
canvas.configure(bg="black")


def toggle_entry_state():
    app = App(frame_Arguments, canvas, 0)
    if checkbox.get() == 0:
        text_input_ip.configure(state='disabled', border_color="#454545", placeholder_text_color="#313233",
                                placeholder_text="USING DEVICE CAMERA")
        text_input_port.configure(state='disabled', border_color="#454545", placeholder_text_color="#313233")
        get_input_button.configure(state="disabled", fg_color="#454545")
        app.cap.release()
        app = App(frame_Arguments, canvas, 0)
    else:
        text_input_ip.configure(state='normal', border_color="#808080", placeholder_text_color="#808080")
        text_input_port.configure(state='normal', border_color="#808080", placeholder_text_color="#808080")
        get_input_button.configure(state="normal", fg_color="#808080")
        app.cap.release()
        url = get_input()
        app = App(frame_Arguments, canvas, url)


def get_input():
    if checkbox.get():
        url = "http://" + text_input_ip.get() + ":" + text_input_port.get() + "/video"
        print("Input text:", url)
        return url
    else:
        print("Using device camera")
        return 0


checked = customtkinter.BooleanVar(value=False)
checkbox = customtkinter.CTkCheckBox(master=frame_Arguments, text="Enable IP Camera", variable=checked,
                                     command=toggle_entry_state)
checkbox.pack(pady=12, padx=10)

text_input_ip = customtkinter.CTkEntry(master=frame_Arguments, height=2, placeholder_text="IPAddress",
                                       font=('Roboto', 12, 'bold'), state='disabled', border_color="#454545",
                                       placeholder_text_color="#313233")
text_input_ip.pack(pady=12, padx=10)

text_input_port = customtkinter.CTkEntry(master=frame_Arguments, height=2, placeholder_text="Port",
                                         font=('Roboto', 12, 'bold'), state='disabled', border_color="#454545",
                                         placeholder_text_color="#313233")
text_input_port.pack(pady=12, padx=10)

get_input_button = customtkinter.CTkButton(master=frame_Arguments, text="Get Input",
                                           command=get_input, state="disabled")
get_input_button.pack(pady=12, padx=10)

frame_Presentation = customtkinter.CTkFrame(frame)
frame_Presentation.pack(side=customtkinter.LEFT, pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame_Presentation, text="Presentation",
                               font=("Arial", 20))
label.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame_Presentation, text="Start Presenting", command=run_script)
button.pack(side=customtkinter.BOTTOM, pady=12, padx=10)

root.mainloop()
