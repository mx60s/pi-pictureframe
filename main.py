import sys
import os

font_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font')

# Search lib folder for display driver modules
sys.path.append('lib')
from waveshare_epd import epd7in5_V2
epd = epd7in5_V2.EPD()

from datetime import datetime
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import requests, json
from io import BytesIO
import csv

# Define funciton for writing image and sleeping for a number of min.
def write_to_screen(image, sleep_seconds):
    print('Writing to screen.')
    # Write to screen
    h_image = Image.new('1', (epd.width, epd.height), 255)
    # Open the template
    screen_output_file = Image.open(os.path.join(pic_dir, image))
    # Initialize the drawing context with template as background
    h_image.paste(screen_output_file, (0, 0))
    epd.display(epd.getbuffer(h_image))
    
    print('Sleeping for ' + str(sleep_seconds) +'.')
    time.sleep(sleep_seconds)

# Define function for displaying error
def display_error(error_source):
    print('Error in the', error_source, 'request.')
    
    error_image = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(error_image)
    draw.text((100, 150), error_source +' ERROR', font=font50, fill=black)
    draw.text((100, 300), 'Retrying in 30 seconds', font=font22, fill=black)
    
    current_time = datetime.now().strftime('%H:%M')
    draw.text((300, 365), 'Last Refresh: ' + str(current_time), font = font50, fill=black)

    # Save the error image
    error_image_file = 'error.png'
    error_image.save(os.path.join(pic_dir, error_image_file))
    error_image.close()

    write_to_screen(error_image_file, 30)


# Set the fonts
# font22 = ImageFont.truetype(os.path.join(font_dir, 'Font.ttc'), 22)
# font30 = ImageFont.truetype(os.path.join(font_dir, 'Font.ttc'), 30)

# Set the colors
# may need to define more for these pictures 
black = 'rgb(0,0,0)'
white = 'rgb(255,255,255)'
grey = 'rgb(235,235,235)'

print('Initializing and clearing screen.')
epd.init()
epd.Clear()


URL = '?' 

while True:
    error_connect = True
    while error_connect == True:
        try:
            print('Attempting to connect to source.')
            response = requests.get(URL)
            print('Connection to source successful.')
            error_connect = None
        except:
            print('Connection error.')
            display_error('CONNECTION') 
    
    error = None
    while error == None:
        if response.status_code == 200:
            print('Connection to source successful.')
            data = response.json()
            
            # optional function to determine what type of picture to get for today
            # maybe it could correspond with the weather/time/whatever?

            # get picture from website
            picture = '' # stand-in, the function should return a png
  
        else:
            display_error('HTTP')


    template = 'template.png'
    draw = ImageDraw.Draw(template)
    
    
    template.paste(picture, (0, 0)) # will need to sub in correct indices when you know what the template will look like
    # Place a black rectangle outline
    draw.rectangle((0, 0, 0, 0), outline=black)

    # maybe do this again to add the time and/or additional information that should appear here

    # Add a reminder to take out trash on Mon and Thurs
    '''weekday = datetime.today().weekday()
    if weekday == 0 or weekday == 3:
        draw.rectangle((345, 13, 705, 55), fill =black)
        draw.text((355, 15), 'TAKE OUT TRASH TODAY!', font=font30, fill=white)
    '''
    # this could be a fun thing to put in
        
    screen_output_file = 'screen_output.png'
    template.save(screen_output_file)
    template.close()
    
    # Refresh clear screen to avoid burn-in at 3:00 AM
    if datetime.now().strftime('%H') == '03':
    	print('Clearning screen to avoid burn-in.')
    	epd.Clear()

    write_to_screen(screen_output_file, 600)