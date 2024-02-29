import tkinter as tk
from tkinter import Toplevel, Checkbutton, Button, IntVar, Entry, Label
from selenium import webdriver

def show_popup():
    def proceed():
        selected_values = [value for value, var in zip(checkbox_values, checkbox_vars) if var.get() == 1]
        user_input = entry.get()

        with open("selected_data.txt", "w") as file:
            file.write("User Input: {}\n".format(user_input))
            file.write("Selected Values:\n")
            for selected_value in selected_values:
                file.write(f"- {selected_value}\n")

        popup.destroy()

    popup = Toplevel(root)
    popup.title("Overlaying Popup Window")
    popup.geometry("400x250")

    label = Label(popup, text="Enter some data:")
    label.pack(pady=10)

    entry = Entry(popup)
    entry.pack(pady=10)

    checkbox_values = ["Brand", "Speed (max)", "Shipping Weight"]
    checkbox_vars = [IntVar() for _ in range(len(checkbox_values))]
    checkboxes = [Checkbutton(popup, text=value, variable=var) for value, var in zip(checkbox_values, checkbox_vars)]
    for checkbox in checkboxes:
        checkbox.pack()

    proceed_button = Button(popup, text="Proceed", command=proceed)
    proceed_button.pack(pady=10)

def open_overlay(url):
    driver = webdriver.Chrome()  # Change to webdriver.Firefox() for Firefox
    driver.get(url)

    # Execute JavaScript to create an overlay on the page
    driver.execute_script('''
        var div = document.createElement('div');
        div.setAttribute('id', 'overlayDiv');
        div.style.position = 'fixed';
        div.style.top = '0';
        div.style.left = '0';
        div.style.width = '100%';
        div.style.height = '100%';
        div.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
        document.body.appendChild(div);
    ''')

    show_popup()

def get_url():
    url = url_entry.get()
    open_overlay(url)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Window")
    root.geometry("400x300")

    url_label = Label(root, text="Enter URL:")
    url_label.pack(pady=10)

    url_entry = Entry(root)
    url_entry.pack(pady=10)

    submit_button = Button(root, text="Submit", command=get_url)
    submit_button.pack(pady=20)

    root.mainloop()
