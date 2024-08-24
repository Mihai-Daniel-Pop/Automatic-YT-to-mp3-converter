from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from tkinter import *

# Function to handle placeholder text
def on_entry_click(event):
    if query.get() == placeholder:
        query.delete(0, END)  
        query.config(fg='black')  
    query.bind("<FocusOut>", on_focus_out)

def on_focus_out(event):
    if query.get() == '':
        query.insert(0, placeholder)
        query.config(fg='grey')
    query.unbind("<FocusOut>")

def submit():
    global yt_query
    yt_query = query.get()  
    root.destroy()  

# Tkinter GUI setup
root = Tk()
root.title("YouTube to MP3 Automatic Converter")
root.geometry("400x200")

mesg = Label(root, text="Welcome to YouTube to MP3 Automatic Converter")
mesg.pack(pady=20)

placeholder = "Song name and band"
query = Entry(root, fg='grey')
query.insert(0, placeholder)  # set placeholder text
query.bind("<FocusIn>", on_entry_click)
query.pack()

submit_button = Button(root, text="Submit", command=submit)
submit_button.pack(pady=10)

root.mainloop()

###

#Goin to the YT homepage
driver = webdriver.Firefox()
driver.get("http://www.youtube.com")
driver.implicitly_wait(10)

#Declining cookies
element = driver.find_element(By.CSS_SELECTOR, "div.eom-button-row:nth-child(1) > ytd-button-renderer:nth-child(1) > yt-button-shape:nth-child(1) > button:nth-child(1) > yt-touch-feedback-shape:nth-child(2) > div:nth-child(1) > div:nth-child(2)")
element.click()

#Manipulating the link as if we seached using the search bar
search="https://www.youtube.com/results?search_query="
driver.get(search+yt_query)

#getting the link of the first video which is probably the desired one
try:
    # Locate the first video element (XPath can be adjusted as needed)
    first_video = driver.find_element(By.XPATH, '//*[@id="video-title"]')
    video_link = first_video.get_attribute('href')

    print("First video link:", video_link)

except Exception as e:
    print("Error occurred:", e)

#going to the online converter and converting the video
driver.get("https://yt2mp3.site/en/")
yt_mp3_conversion=driver.find_element(By.XPATH, '//*[@id="videoURL"]')
yt_mp3_conversion.send_keys(video_link)
conversion=driver.find_element(By.CSS_SELECTOR, "#btn-submit")
conversion.click()
sleep(10)
download_link = driver.find_element(By.CSS_SELECTOR,".right > div:nth-child(1)")
download_link.click()
sleep(10)
download_file = driver.find_element(By.CSS_SELECTOR,"#mp3link320")
download_file.click()
sleep(10)
driver.quit()
