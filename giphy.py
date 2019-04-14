"""Display a GIF on Vector's face
"""

import io
import random
import sys
import time
import requests
import json

try:
    from PIL import Image, ImageSequence, ImageDraw
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

import anki_vector
from anki_vector.util import degrees

keywords = 'up dog dug'

giphy_url = 'http://api.giphy.com/v1/gifs/search'
giphy_api_key = 'ksnIMNa2GiFEWysK3tTcM0hCbPyrbkln'
giphy_limit = 5


def main():
    args = anki_vector.util.parse_command_args()

    # Get GIFs list from Giphy
    request = requests.get(giphy_url, {'q': keywords, 'api_key': giphy_api_key, 'limit': giphy_limit})
    # print(request.url)
    data = json.loads(request.content)
    # print(json.dumps(data, sort_keys=True, indent=2))

    if data and data['data'] and len(data['data']) > 0:
        # Load a random GIF
        selected_gif_index = random.randrange(len(data['data']))
        gif_url = data['data'][selected_gif_index]['images']['original']['url']
        gif = Image.open(io.BytesIO(requests.get(gif_url).content))

        with anki_vector.Robot(args.serial) as robot:
            # Get vector'screen dimension (height, width)
            vector_screen_width, vector_screen_height = anki_vector.screen.dimensions()

            background = Image.new('RGB', (vector_screen_width, vector_screen_height), (0, 0, 0))
            background_w, background_h = background.size

            # Build the vector'sscreen-compliant gif
            images = list()
            for frame in ImageSequence.Iterator(gif):
                frame = frame.convert('RGB')

                # Resize the frame image
                frame.thumbnail((vector_screen_width, vector_screen_height), Image.ANTIALIAS)
                frame_w, frame_h = frame.size

                # Define the black background
                image = background.copy()

                # Paste the frame image on the black background
                offset = (background_w - frame_w) // 2, (background_h - frame_h) // 2
                image.paste(frame, offset)
                images.append(image)

            # If necessary, move Vector's Head and Lift to make it easy to see his face
            robot.behavior.set_head_angle(degrees(45.0))
            robot.behavior.set_lift_height(0.0)

            for image in images:
                # Convert the image to the format used by the Screen
                screen_data = anki_vector.screen.convert_image_to_screen_data(image)

                # Display image on Vector's face
                robot.screen.set_screen_with_image_data(screen_data, 1.0 / 24)
                time.sleep(1.0 / 24)


if __name__ == "__main__":
    main()
