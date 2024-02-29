import pyautogui

def take_screenshot():
    try:
        print("Move the mouse to the top-left corner of the area to capture and click...")
        x1, y1 = pyautogui.position()
        pyautogui.click()

        print("Move the mouse to the bottom-right corner of the area to capture and click...")
        x2, y2 = pyautogui.position()
        pyautogui.click()

        left = min(x1, x2)
        top = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)

        if width > 0 and height > 0:
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            screenshot.show()  # Display the screenshot
            screenshot.save('screenshot.png')  # Save the screenshot as an image file
            print("Screenshot captured and saved as 'screenshot.png'")
        else:
            print("Invalid selection: Please ensure the area selected is not empty.")
    except KeyboardInterrupt:
        print("\nProcess interrupted.")

if __name__ == "__main__":
    take_screenshot()
