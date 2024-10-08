import requests
import time

url = "https://apis.elai.io/api/v1/videos/from-presentation"
filepath = "test.pptx"
headers = {
    "Authorization": "ELAI.IO_API_KEY"
}

with open(filepath, 'rb') as file:
    files = {'file': file}
    #creates video from pptx File
    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
      video_id = response.content.decode('utf-8')
      url = "https://apis.elai.io/api/v1/videos/render/" + video_id[1:-1]

      headers = {
          "accept": "application/json",
          "Authorization": "ELAI.IO_API_KEY"
      }
      #Renders the video
      response = requests.post(url, headers=headers)

      if response.status_code == 200:
        url = "https://apis.elai.io/api/v1/videos/" + video_id[1:-1]

        headers = {
            "accept": "application/json",
            "Authorization": "ELAI.IO_API_KEY"
        }
        #Retrieves the video
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
          while(response.status_code == 200 and  response.json().get('url') != None):
            time.sleep(10)
            response = requests.get(url, headers=headers)

          video_data = response.json()  # Assuming the response is in JSON format
          video_url = video_data.get('url')  # Adjust the key based on actual response

          # Download the video
          if video_url:
              video_response = requests.get(video_url)
              with open('downloaded_video.mp4', 'wb') as f:
                  f.write(video_response.content)
              print("Video downloaded successfully!")
          else:
              print("No video URL found in the response")
        else:
            print("Failed to retrieve video:", response.status_code)
      else:
        print("Render failed")
