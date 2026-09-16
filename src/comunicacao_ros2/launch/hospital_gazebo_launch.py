import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_comunicacao = get_package_share_directory('comunicacao_ros2')
    
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        )
    )

    urdf_path = os.path.join(
        pkg_comunicacao, 'urdf', 'robo_hospitalar.urdf')
    with open(urdf_path, 'r') as f:
        robot_description = f.read()

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
        }],
    )

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'robo_hospitalar',
        ],
        output='screen',
    )

    monitor_node = Node(
        package='comunicacao_ros2',
        executable='monitor_transporte',
        name='monitor_transporte',
        output='screen',
        parameters=[{'temperatura_limite': 27.0}],
    )

    echo_alertas = ExecuteProcess(
        cmd=['ros2', 'topic', 'echo', '/alertas', 'std_msgs/msg/String' ],
        output='screen',
    )
    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_entity,
        monitor_node,
        echo_alertas,
    ])
