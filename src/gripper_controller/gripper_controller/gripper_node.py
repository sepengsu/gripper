import rclpy
from rclpy.node import Node

# 인터페이스 패키지에서 import
from gripper_interface.srv import GripperInit, GripperGrasp, GripperRelease
from gripper_interface.msg import GripperStatus

# 로컬 함수 import (gripper_control 폴더 아래에 있어야 함)
from gripper_control.gripper_function.init import safe_initialize, is_initialized
from gripper_control.gripper_function.grasp import safe_grasp, ungrasp
from connect.connection import find_gripper

class GripperNode(Node):
    def __init__(self):
        super().__init__('gripper_node')

        # 그리퍼 연결 
        self.cilent = find_gripper() # 연결된 그리퍼 찾기
        if not self.cilent:
            self.get_logger().error('Gripper not found. Please check the connection.')
            raise RuntimeError('Gripper not found.')
        self.get_logger().info('Gripper connected successfully.')

        # 서비스 등록
        self.srv_init = self.create_service(GripperInit, 'gripper_init', self.init_callback)
        self.srv_grasp = self.create_service(GripperGrasp, 'gripper_grasp', self.grasp_callback)
        self.srv_release = self.create_service(GripperRelease, 'gripper_release', self.release_callback)

        # 상태 퍼블리셔
        self.status_pub = self.create_publisher(GripperStatus, 'gripper_status', 10)
        self.timer = self.create_timer(1.0, self.publish_status)

        self._is_initialized = False
        self.get_logger().info('GripperNode started.')

    def init_callback(self, request, response):
        try:
            safe_initialize(self.cilent)
            self._is_initialized = True
            response.success = True
            response.message = 'Gripper initialized successfully.'
        except Exception as e:
            response.success = False
            response.message = str(e)
        return response

    def grasp_callback(self, request, response):
        try:
            if not self._is_initialized:
                response.success = False
                response.message = 'Gripper not initialized.'
                return response

            # safe_grasp(request.force, request.position)
            safe_grasp(self.cilent)
            response.success = True
            response.message = f'Gripper grasped at {request.position}%, force {request.force}%.'
        except Exception as e:
            response.success = False
            response.message = str(e)
        return response

    def release_callback(self, request, response):
        try:
            if not self._is_initialized:
                response.success = False
                response.message = 'Gripper not initialized.'
                return response

            ungrasp(self.cilent)
            response.success = True
            response.message = 'Gripper released.'
        except Exception as e:
            response.success = False
            response.message = str(e)
        return response

    def publish_status(self):
        msg = GripperStatus()
        msg.position = 0      # TODO: 실제 위치 읽기 함수가 있다면 반영
        msg.force = 0         # TODO: 실제 힘 읽기 함수가 있다면 반영
        msg.status = "OK" if self._is_initialized else "NOT_INITIALIZED"
        msg.is_initialized = self._is_initialized
        self.status_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = GripperNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
