import csv
import cv2
import yt_dlp as youtube_dl
import pytesseract
import numpy as np

rows = [] 
logonames = []
lastids = []
with open('br_videos_ids.csv') as file:
    contents = file.readlines()
contents = [content.replace('"', '').strip() for content in contents]
youtube_ids = contents[1:]
for youtube_id in youtube_ids:
  video_url = 'https://www.youtube.com/watch?v=' + youtube_id
  ydl_opts = {}

  # create youtube-dl object
  ydl = youtube_dl.YoutubeDL(ydl_opts)

  # set video url, extract video information
  info_dict = ydl.extract_info(video_url, download=False)

  # get video formats available
  formats = info_dict.get('formats',None)

  for f in formats:

      # I want the lowest resolution, so I set resolution as 144p
      if f.get('format_note',None) == '360p':
        haslogo = False
        logoname = ""
          #get the video url
        url = f.get('url',None)
        # Open the stream using OpenCV's VideoCapture function
        cap = cv2.VideoCapture(url)
        # Get the total number of frames in the video
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # Set the frame index to the middle frame of the video
        frame_index = int(total_frames / 2)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

        # Read the frame at the current frame index
        ret, frame = cap.read()
        height, width, _ = frame.shape

      # Calculate the size of each sub-image
        sub_img_height = int(height / 6)
        sub_img_width = int(width / 6)
        # Convert the frame to grayscale
        for j in range(5,-1,-1):
          for i in range(5,-1,-1):
            sub_img = frame[i*sub_img_height:(i+1)*sub_img_height, j*sub_img_width:(j+1)*sub_img_width]
            gray = cv2.cvtColor(sub_img, cv2.COLOR_BGR2GRAY)
        # Use Pytesseract to search for a given text in the frame
            text = pytesseract.image_to_string(gray)

        # Print the searched text
            if "SURYA" in text:
              haslogo = True
              logoname = "Surya "
              break
            if "HAUT" in text:
              haslogo = True
              logoname = "Hauteloom "
              break
            if "Bouti" in text:
              haslogo = True
              logoname = "Boutique Rugs"
              break
        cap.release()
        if haslogo:
          logonames[] = logoname 
        else:
          logonames[] = logoname
        lastids[] = youtube_id
        break
with open('youtubelogos.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    for i in range(len(lastids)):
        data = [lastids[i], logonames[i]]
        writer.writerow(data)


    




