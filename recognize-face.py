import threading

import anki_vector
from anki_vector.events import Events
from anki_vector.util import degrees

faces = []


def main():
    def on_robot_observed_face(_robot, _event_type, _event, _done):
        global faces

        face_id = _event.face_id
        name = _event.name
        if not any(face["face_id"] == face_id for face in faces):
            print(f"Vector sees a face: {{face_id: {face_id}, name :{name}}}")

            if face_id > 0 and name:
                faces.append({"face_id": face_id, "name": name})
                _robot.behavior.say_text("I see a face!")
                _robot.behavior.say_text("Hello " + name)
                _done.set()

    args = anki_vector.util.parse_command_args()

    with anki_vector.Robot(args.serial, enable_face_detection=True) as robot:
        # robot.behavior.drive_off_charger()

        # If necessary, move Vector's Head and Lift to make it easy to see his face
        robot.behavior.set_head_angle(degrees(45.0))
        robot.behavior.set_lift_height(0.0)

        # Activate the camera display on Vector's face
        robot.vision.enable_display_camera_feed_on_face()

        done = threading.Event()

        # Create a subscription to 'robot_observed_face' event
        # which will execute the def 'on_robot_observed_face'
        robot.events.subscribe(on_robot_observed_face, Events.robot_observed_face, done)

        print("Waiting for face events...")

        try:
            if not done.wait(timeout=10):
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
