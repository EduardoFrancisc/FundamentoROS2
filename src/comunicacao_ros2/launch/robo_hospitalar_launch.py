from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    limite_arg = DeclareLaunchArgument(
        'temperatura_limite',
        default_value='28.0',
        description='Limiar de alerta (°C)',
    )
    controlador_node = Node(
        package='comunicacao_ros2',
        executable='controlador',
        name='controlador',
        output='screen',
    )

    estado_robo_node = Node(
        package='comunicacao_ros2',
        executable='estado_robo',
        name='estado_robo',
        output='screen',
    )

    monitor_node = Node(
        package='comunicacao_ros2',
        executable='monitor_transporte',
        name='monitor_transporte',
        output='screen',
        parameters=[{
            'temperatura_limite':
                LaunchConfiguration('temperatura_limite'),
        }],
    )
    return LaunchDescription([
        limite_arg,
        controlador_node,
        estado_robo_node,
        monitor_node,
    ])