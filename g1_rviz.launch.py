import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory('g1_rviz_bridge')

    urdf = LaunchConfiguration('urdf')
    rviz_config = LaunchConfiguration('rviz_config')
    lidar_z = LaunchConfiguration('lidar_z')
    lidar_x = LaunchConfiguration('lidar_x')

    return LaunchDescription([
        DeclareLaunchArgument(
            'urdf',
            default_value=os.path.join(pkg, 'urdf', 'g1_29dof.urdf'),
            description='Path to the G1 URDF with absolute mesh paths'),

        DeclareLaunchArgument(
            'rviz_config',
            default_value=os.path.join(pkg, 'rviz', 'g1.rviz'),
            description='RViz2 config'),

        DeclareLaunchArgument('lidar_x', default_value='0.1'),
        DeclareLaunchArgument('lidar_z', default_value='0.5'),

        Node(
            package='g1_rviz_bridge',
            executable='joint_bridge',
            name='g1_joint_bridge',
            output='screen',
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            arguments=[urdf],
            output='screen',
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='pelvis_to_livox',
            arguments=[lidar_x, '0', lidar_z, '0', '0', '0', 'pelvis', 'livox_frame'],
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config],
        ),
    ])
