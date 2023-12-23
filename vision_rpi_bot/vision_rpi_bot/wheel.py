import rclpy
from rclpy.node import Node
from odrive import find_any
from odrive.enums import AXIS_STATE_CLOSED_LOOP_CONTROL
import time
import fibre


class WheelNode(Node):

    def __init__(self):
        super().__init__('wheel_node')
        self.odrv0 = find_any()
        self.move_forward()

    def move_forward(self):
        self.get_logger().info("Moving forward...")
        self.odrv0.axis0.requested_state = self.odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.odrv0.axis0.controller.input_vel = -0.2
        self.odrv0.axis1.controller.input_vel = 0.2
        self.get_logger().info("Waiting for 10 seconds...")
        time.sleep(10)
        self.get_logger().info("Moving stopped.")
        self.stop_robot()

    def move_backward(self):
        self.get_logger().info("Moving backward...")
        self.odrv0.axis0.requested_state = self.odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.odrv0.axis0.controller.input_vel = 0.2
        self.odrv0.axis1.controller.input_vel = -0.2
        self.get_logger().info("Waiting for 10 seconds...")
        time.sleep(10)
        self.get_logger().info("Moving stopped.")
        self.stop_robot()

    def move_left(self):
        self.get_logger().info("Moving left...")
        self.odrv0.axis0.requested_state = self.odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.odrv0.axis0.controller.input_vel = 0.2
        self.odrv0.axis1.controller.input_vel = 0.2
        time.sleep(6)
        self.get_logger().info("Moving stopped.")
        self.stop_robot()

    def move_right(self):
        self.get_logger().info("Moving right...")
        self.odrv0.axis0.requested_state = self.odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.odrv0.axis0.controller.input_vel = -0.2
        self.odrv0.axis1.controller.input_vel = -0.2
        time.sleep(6)
        self.get_logger().info("Moving stopped.")
        self.stop_robot()

    def stop_robot(self):
        self.get_logger().info("Stopping...")
        self.odrv0.axis0.controller.input_vel = self.odrv0.axis1.controller.input_vel = 0.0

        # Release the USB interface
        #self.odrv0.release_interface()
        #time.sleep(1)  # Allow time for the release
        ## Reconnect to the ODrive
        self.odrv0 = find_any()


def main(args=None):
    rclpy.init(args=args)
    wheel_node = WheelNode()

    try:
        wheel_node.move_forward()
        wheel_node.move_backward()
        wheel_node.move_left()
        wheel_node.move_right()
    except KeyboardInterrupt:
        # Stop the robot if the script is interrupted
        wheel_node.stop_robot()
        print("\nScript interrupted.")
    except Exception as e:
        print(f"An error occurred: {e}")

    wheel_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
