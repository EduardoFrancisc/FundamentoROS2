import random
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from sensor_msgs.msg import Temperature
from std_msgs.msg import Bool, String
from std_srvs.srv import Trigger
class MonitorTransporte(Node):
    def __init__(self):
        super().__init__('monitor_transporte')
        self.declare_parameter('temperatura_limite', 28.0)
        self.ocupado = True
        self.pub_temp = self.create_publisher(
            Temperature, '/temperatura_ambiente', 10)
        self.pub_ocupado = self.create_publisher(
            Bool, '/robo_ocupado', 10)
        self.pub_alertas = self.create_publisher(
            String, '/alertas', 10)
        self.srv_entrega = self.create_service(
            Trigger, '/confirmar_entrega',
            self.confirmar_entrega_callback)
        self.create_timer(1.0, self.tick)
        self.get_logger().info('nó iniciado')

    def confirmar_entrega_callback(self, request, response):
        self.ocupado = False
        alerta = String()
        alerta.data = 'Entrega confirmada'
        self.pub_alertas.publish(alerta)
        response.success = True
        response.message = 'Entrega confirmada'
        return response
    def tick(self):
        temp_msg = Temperature()
        temp_msg.temperature = round(random.uniform(18.0, 30.0),2)
        self.pub_temp.publish(temp_msg)
        ocupado_msg = Bool()
        ocupado_msg.data = self.ocupado
        self.pub_ocupado.publish(ocupado_msg)
        limite = self.get_parameter('temperatura_limite').value
        if temp_msg.temperature > limite:
            alerta = String()
            alerta.data = 'TEMPERATURA FORA DO PADRAO'
            self.pub_alertas.publish(alerta)
def main(args=None):
    rclpy.init(args=args)
    node = MonitorTransporte()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()
