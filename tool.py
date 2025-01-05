import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import pyautogui
import os
import time
import keyboard

# Configuration
options = uc.ChromeOptions()
options.add_argument('--start-maximized')
driver = uc.Chrome(options=options)

# Screenshots directory
screenshots_dir = 'screenshots'
os.makedirs(screenshots_dir, exist_ok=True)

# Open the website
driver.get('https://learn.blackspectacles.com/')
print("Please log in and navigate to the first question.")
print("Press 'Ctrl + B' to start taking screenshots and navigating pages. Press 'q' to quit at any time.")

# Function to take a screenshot of the entire screen
def take_screenshot(page_num):
    screenshot_path = os.path.join(screenshots_dir, f'question_{page_num}.png')
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    print(f"Captured screenshot for question {page_num}: {screenshot_path}")
    return screenshot_path

# Function to click at the current mouse cursor location
def click_at_cursor():
    x, y = pyautogui.position()
    pyautogui.click(x, y)
    print(f"Clicked at position ({x}, {y}).")

# Start the process after the first hotkey
page_num = 1
max_questions = 21  # Set a limit for safety (can be adjusted)
started = False

try:
    while True:
        # Check for quit hotkey
        if keyboard.is_pressed('q'):
            print("Quitting the process.")
            break

        # Wait for the first 'Ctrl + B' hotkey to start the process
        if not started:
            if keyboard.is_pressed('ctrl') and keyboard.is_pressed('b'):
                print("Starting the screenshot and click process...")
                started = True

        # After the first hotkey, automatically perform actions
        if started:
            # Wait for the specified time
   
            print(f"Taking screenshot for question {page_num}...")
            take_screenshot(page_num)

            # Simulate a click at the current mouse cursor position
            print("Clicking at the current mouse cursor position...")
            click_at_cursor()

            # Increment page number and wait briefly for the next page to load
            page_num += 1
            time.sleep(2)  # Adjust the delay based on application load times

            # Optional: Stop after a certain number of pages for safety
            if page_num > max_questions:
                print("Reached the maximum number of questions. Stopping.")
                break

except Exception as e:
    print(f"Error encountered: {e}")

# Close the browser
driver.quit()

# Combine screenshots into a PDF and remove images after creating the PDF
if page_num > 1:
    pdf_path = "questions.pdf"
    
    # Sort files in numerical order
    image_files = sorted(
        [f for f in os.listdir(screenshots_dir) if f.endswith('.png')],
        key=lambda x: int(x.split('_')[1].split('.')[0])  # Extract numerical part for sorting
    )
    
    images = [Image.open(os.path.join(screenshots_dir, f)) for f in image_files]
    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    
    print(f"Generated PDF: {pdf_path}")
    
    # Remove all images after PDF creation
    for f in image_files:
        os.remove(os.path.join(screenshots_dir, f))
    print("All images have been deleted.")
else:
    print("No screenshots taken. Exiting.")
