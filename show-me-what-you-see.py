import anki_vector
from anki_vector.util import degrees


def main():
    args = anki_vector.util.parse_command_args()

    with anki_vector.Robot(args.serial) as robot:
        # If necessary, move Vector's Head and Lift to make it easy to see his face
        robot.behavior.set_head_angle(degrees(35.0))
        robot.behavior.set_lift_height(0.0)

        # Activate the camera display on Vector's face
        robot.vision.enable_display_camera_feed_on_face()
        print("Display Vector camera on its face, press ctrl+c to exit")

        while True:
            infinite_loop = True


if __name__ == "__main__":
    main()
