```
gripper_control_ros2/
├── gripper_control/                # 기존 모듈 복붙
│   ├── base_function/
│   ├── function_to_bytes/
│   ├── gripper_function/
│   ├── __init__.py
│   └── main.py ...
│
├── gripper_node/                  # ROS2 노드 파일
│   └── gripper_node.py
│
├── srv/
│   └── GripperCommand.srv
├── msg/
│   └── GripperStatus.msg
├── launch/
│   └── gripper_launch.py
├── setup.py
├── package.xml
```