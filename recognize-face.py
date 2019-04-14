import functools
import threading

import anki_vector
from anki_vector.events import Events
from anki_vector.util import degrees

faces = []


def main():
    evt = threading.Event()

    def on_robot_observed_face(robot, event_type, event):
        global faces

        face_id = event.face_id
        name = event.name
        if not any(face['face_id'] == face_id for face in faces):
            print(f"Vector sees a face: {{face_id: {face_id}, name :{name}}}")

            if face_id > 0 and name:
                faces.append({'face_id': face_id, 'name': name})
                robot.say_text("I see a face!")
                robot.say_text("Hello " + name)
                # evt.set()

    args = anki_vector.util.parse_command_args()

    with anki_vector.Robot(args.serial, enable_face_detection=True) as robot:
        # robot.behavior.drive_off_charger()

        # If necessary, move Vector's Head and Lift to make it easy to see his face
        robot.behavior.set_head_angle(degrees(45.0))
        robot.behavior.set_lift_height(0.0)

        # Activate the camera display on Vector's face
        robot.vision.enable_display_camera_feed_on_face()

        print("Waiting for face events...")

        # Create a subscription to 'robot_observed_face' event
        # which will execute the def 'on_robot_observed_face'
        on_robot_observed_face = functools.partial(on_robot_observed_face, robot)
        robot.events.subscribe(on_robot_observed_face, Events.robot_observed_face)

        try:
            if not evt.wait(timeout=10):
                if faces:
                    print(f"Vector recognize {len(faces)} face(s): {faces}")
                else:
                    print("Vector never recognize a face")
        except KeyboardInterrupt:
            pass

    # Detach the event subscription
    robot.events.unsubscribe(on_robot_observed_face, Events.robot_observed_face)


if __name__ == "__main__":
    main()
