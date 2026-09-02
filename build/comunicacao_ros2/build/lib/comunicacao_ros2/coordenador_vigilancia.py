import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from sensor_msgs.msg import Range
from std_msgs.msg import String
from std_srvs.srv import SetBool
class CoordenadorVigilancia(Node):
    def __init__(self):
        super().__init__('coordenador_vigilancia')
        self.alarme_ativo = False
        self.sub_dist = self.create_subscription(
            Range, '/distancia_frontal', self.distancia_callback, 10)
        self.sub_status = self.create_subscription(
            String, '/status_patrulha', self.status_callback, 10)
        self.srv_alarme = self.create_service(
            SetBool, '/ligar_alarme', self.ligar_alarme_callback)
        self.pub_alertas = self.create_publisher(
            String, '/alertas', 10)
        self.get_logger().info('nó iniciado')

    def ligar_alarme_callback(self, request, response):
        self.alarme_ativo = request.data
        response.success = True
        estado = 'ativado' if self.alarme_ativo else 'desativado'
        response.message = f'Alarme {estado}'
        return response

    def distancia_callback(self, msg):
        if msg.range < 0.5 and self.alarme_ativo:
            alerta = String()
            alerta.data = 'INTRUSO DETECTADO'
            self.pub_alertas.publish(alerta)
            self.get_logger().warn('INTRUSO DETECTADO')

    def status_callback(self, msg):
        self.get_logger().info(f'status_patrulha: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = CoordenadorVigilancia()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()