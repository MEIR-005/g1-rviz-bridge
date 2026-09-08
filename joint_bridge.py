import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import JointState
from unitree_hg.msg import LowState

JOINT_NAMES = [
    'left_hip_pitch_joint', 'left_hip_roll_joint', 'left_hip_yaw_joint',
    'left_knee_joint', 'left_ankle_pitch_joint', 'left_ankle_roll_joint',
    'right_hip_pitch_joint', 'right_hip_roll_joint', 'right_hip_yaw_joint',
    'right_knee_joint', 'right_ankle_pitch_joint', 'right_ankle_roll_joint',
    'waist_yaw_joint', 'waist_roll_joint', 'waist_pitch_joint',
    'left_shoulder_pitch_joint', 'left_shoulder_roll_joint',
    'left_shoulder_yaw_joint', 'left_elbow_joint', 'left_wrist_roll_joint',
    'left_wrist_pitch_joint', 'left_wrist_yaw_joint',
    'right_shoulder_pitch_joint', 'right_shoulder_roll_joint',
    'right_shoulder_yaw_joint', 'right_elbow_joint', 'right_wrist_roll_joint',
    'right_wrist_pitch_joint', 'right_wrist_yaw_joint',
]


class JointBridge(Node):
    def __init__(self):
        super().__init__('g1_joint_bridge')

        qos = QoSProfile(depth=10)
        qos.reliability = ReliabilityPolicy.BEST_EFFORT

        self.pub = self.create_publisher(JointState, 'joint_states', 10)
        self.create_subscription(LowState, 'lowstate', self.on_lowstate, qos)

        self.count = 0
        self.get_logger().info('waiting for /lowstate')

    def on_lowstate(self, msg):
        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        js.name = JOINT_NAMES
        js.position = [float(msg.motor_state[i].q) for i in range(len(JOINT_NAMES))]
        self.pub.publish(js)

        self.count += 1
        if self.count % 2000 == 0:
            self.get_logger().info(f'{self.count} messages published')


def main():
    rclpy.init()
    node = JointBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
