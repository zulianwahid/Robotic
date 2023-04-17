import rclpy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from webots_ros2_core.utils import ctrl_c_handler

class MyRobot:
    def __init__(self):
        # Initialize ROS2 node
        rclpy.init()
        self.node = rclpy.create_node('my_robot_node')

        # Subscribe to Joy topic
        self.joy_subscriber = self.node.create_subscription(Joy, 'joy', self.joy_callback, 10)

        # Publish to Twist topic
        self.twist_publisher = self.node.create_publisher(Twist, 'cmd_vel', 10)

        # Initialize Twist message
        self.twist = Twist()

        # Set loop rate
        self.rate = self.node.create_rate(10)

    def joy_callback(self, data):
        # Get joystick data
        left_stick_x = data.axes[0]
        left_stick_y = data.axes[1]
        right_stick_x = data.axes[2]
        right_stick_y = data.axes[3]

        # Convert joystick data to Twist message
        self.twist.linear.x = -left_stick_y
        self.twist.linear.y = left_stick_x
        self.twist.angular.z = right_stick_x

        # Publish Twist message
        self.twist_publisher.publish(self.twist)

    def run(self):
        while rclpy.ok():
            # Spin once per loop iteration
            rclpy.spin_once(self.node)

            # Sleep to maintain loop rate
            self.rate.sleep()

if __name__ == '__main__':
    my_robot = MyRobot()
    signal.signal(signal.SIGINT, ctrl_c_handler)
    my_robot.run()
