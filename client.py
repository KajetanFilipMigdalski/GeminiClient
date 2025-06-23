import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import ttk
from tkinter import filedialog
import google.generativeai as genai
import os

hideapi = True

chat_session = None

def main():
    global chat_session

    if chat_session is None:
        genai.configure(api_key=entry.get())

        generation_config ={
            "temperature": scale_temperature.get(),
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name=como_model.get() if como_model.get() else "gemini-2.0-flash",
            generation_config=generation_config,
            system_instruction=instructions.get("1.0", tk.END).strip()
        )

        chat_session = model.start_chat(
            history=[]
        )

    response = chat_session.send_message(prompt.get("1.0", tk.END).strip())

    for stream in response:
        text_area.configure(state='normal')
        text_area.insert(tk.END, stream.text)
        text_area.configure(state='disabled')
        text_area.see(tk.END)

    prompt.delete("1.0", tk.END)

def save():
    with open("save.txt", "w") as file:
        file.write(instructions.get("1.0", tk.END).strip() + "\n")

def hs():
    global hideapi
    if hideapi == True:
        entry.config(show="")
        button_hs.config(text="Hide")
        hideapi = False
    else:
        entry.config(show="*")
        button_hs.config(text="Show")
        hideapi = True

def reset():
    global chat_session
    chat_session = None
    text_area.configure(state='normal')
    text_area.delete("1.0", tk.END)
    text_area.configure(state='disabled')

window = tk.Tk()

window.title("AI Chat Client")
window.geometry("400x500")
icon = tk.PhotoImage(file="icon.png")
window.iconphoto(False, icon)
window.config(bg="black")   

label = tk.Label(window, 
                 text="Start chatting with AI.", 
                 bg="black", 
                 fg="white")
label.pack()

option_frame = tk.Frame(window, bg="black")
option_frame.pack()

entry = tk.Entry(option_frame, 
                 bg="black", 
                 fg="white", 
                 insertbackground="white", 
                 show="")
entry.grid(row=0, column=0, padx=5)
entry.insert(0, "Enter your API here.")

button_hs = tk.Button(option_frame,
                      text="Hide",
                      bg="black",
                      fg="white",
                      activebackground="white",
                      command=hs)
button_hs.grid(row=0, column=1, padx=5)

button_save = tk.Button(option_frame,
                         text="Save",
                         bg="black",
                         fg="white",
                         activebackground="white",
                         command=save)
button_save.grid(row=0, column=3, padx=5)

button_reset = tk.Button(option_frame,
                         text="Reset",
                         bg="black",
                         fg="white",
                         activebackground="white",
                         command= reset)
button_reset.grid(row=0, column=2, padx=5)


text_area = st.ScrolledText(window,
                            width = 40, 
                            height = 8,
                            bg="black",
                            fg="white",
                            insertbackground="white")

text_area.pack(pady=10)

text_area.configure(state ='disabled')

prompt_frame = tk.Frame(window, bg="black")
prompt_frame.pack()

prompt = tk.Text(prompt_frame,
                 width=34,
                 height=3,
                 bg="black",
                 fg="white",
                 insertbackground="white")
prompt.grid(row=0, column=0, padx=10)

submit_frame = tk.Frame(prompt_frame, bg="black")
submit_frame.grid(row=0, column=1, padx=5)

button_submit = tk.Button(submit_frame,
                            text="Submit",
                            bg="black",
                            fg="white",
                            activebackground="white",
                            command=main)
button_submit.grid(row=0, column=0, padx=5)

label = tk.Label(window, 
                 text="Run settings:", 
                 bg="black", 
                 fg="white")
label.pack(pady=5)

model_frame = tk.Frame(window, bg="black")
model_frame.pack(pady=5)

label_model = tk.Label(model_frame,
                       text="Model:",
                       bg="black",
                       fg="white")
label_model.grid(row=0, column=0, padx=5)

como_model = ttk.Combobox(model_frame,
                          values=["gemini-2.0-flash",
                                  "gemini-2.0-flash-lite",
                                  "gemini-2.5-pro",
                                  "gemini-2.5-flash",
                                  "gemma-3n-e4b-it",
                                  "gemma-3-1b-it",
                                  "gemma-3-4b-it",
                                  "gemma-3-12b-it",
                                  "gemma-3-27b-it",
                                  "learnlm-2.0-flash-experimental",])
como_model.grid(row=0, column=1, padx=5)

temperature_frame = tk.Frame(window, bg="black")
temperature_frame.pack(pady=5)

label_temperature = tk.Label(temperature_frame,
                             text="Temperature:",
                             bg="black",
                             fg="white")
label_temperature.grid(row=0, column=0, padx=5)
scale_temperature = tk.Scale(temperature_frame,
                              from_=0.0,
                              to=2.0,
                              resolution=0.05,
                              orient=tk.HORIZONTAL,
                              bg="black",
                              fg="white",
                              activebackground="white")
scale_temperature.grid(row=0, column=1, padx=5)
scale_temperature.set(1.0)

label_instructions = tk.Label(window,
                             text="Instructions:",
                             bg="black",
                             fg="white")
label_instructions.pack(pady=5)

instructions = tk.Text(window,
                 width=43,
                 height=5,
                 bg="black",
                 fg="white",
                 insertbackground="white")
instructions.pack(pady=5)

if os.path.exists("save.txt"):
    with open("save.txt", "r") as file:
        instructions_text = file.read().strip()
        instructions.insert("1.0", instructions_text)
window.mainloop()
