import tkinter as tk
import pyautogui
import datetime
import webbrowser
import os
import csv

def take_bounded_screenshot(x1, y1, x2, y2):
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    image = pyautogui.screenshot(region=(x1, y1, x2, y2))
    file_name = datetime.datetime.now().strftime("%f")
    
    directory = 'snips'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    file_path = os.path.join(directory, file_name + ".png")
    image.save(file_path)
    return file_path

class Application():
    def __init__(self, master):
        self.snip_surface = None
        self.master = master
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None

        root.geometry("700x500")  # set new geometry
        root.title('Screenshot Data')

        self.menu_frame = tk.Frame(master)
        self.menu_frame.pack(fill=tk.BOTH, expand=tk.YES, padx=1, pady=1)

        self.sku_label = tk.Label(self.menu_frame, text="Enter SKU:")
        self.sku_label.pack()

        self.sku_entry = tk.Entry(self.menu_frame)
        self.sku_entry.pack()

        self.url_label = tk.Label(self.menu_frame, text="Enter URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(self.menu_frame)
        self.url_entry.pack()

        self.load_button = tk.Button(self.menu_frame, text="Load Webpage", command=self.load_webpage)
        self.load_button.pack()

        self.buttonBar = tk.Frame(self.menu_frame, bg="")
        self.buttonBar.pack(fill=tk.BOTH, expand=tk.YES)

        self.snipButton = tk.Button(self.buttonBar, width=7, height=3, text='Take Snip', command=self.create_screen_canvas)
        self.snipButton.pack()

        self.save_button = tk.Button(self.menu_frame, text="Save Data", command=self.save_data)
        self.save_button.pack()

        self.master_screen = tk.Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "maroon3")
        self.picture_frame = tk.Frame(self.master_screen, background="maroon3")
        self.picture_frame.pack(fill=tk.BOTH, expand=tk.YES)

        self.screenshot_data = []

    def create_screen_canvas(self):
        self.master_screen.deiconify()
        root.withdraw()

        self.snip_surface = tk.Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.snip_surface.pack(fill=tk.BOTH, expand=tk.YES)

        self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):
        self.display_rectangle_position()

        if self.start_x <= self.current_x and self.start_y <= self.current_y:
            print("right down")
            file_path = take_bounded_screenshot(self.start_x, self.start_y, self.current_x - self.start_x, self.current_y - self.start_y)
            self.screenshot_data.append([self.sku_entry.get(), self.url_entry.get(), file_path])

        self.exit_screenshot_mode()
        return event

    def exit_screenshot_mode(self):
        self.snip_surface.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.snip_surface.canvasx(event.x)
        self.start_y = self.snip_surface.canvasy(event.y)
        self.snip_surface.create_rectangle(0, 0, 1, 1, outline='red', width=3, fill="maroon3")

    def on_snip_drag(self, event):
        self.current_x, self.current_y = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.snip_surface.coords(1, self.start_x, self.start_y, self.current_x, self.current_y)

    def display_rectangle_position(self):
        print(self.start_x)
        print(self.start_y)
        print(self.current_x)
        print(self.current_y)

    def load_webpage(self):
        url = self.url_entry.get()
        webbrowser.open(url)
        self.create_screen_canvas()  # Create snipping canvas after loading webpage

    def save_data(self):
        filename = "screenshot_data.csv"
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["SKU", "URL", "Screenshot_Path"])
            writer.writerows(self.screenshot_data)

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()