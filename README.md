# g1-rviz-bridge

Unitree G1 в RViz2: модель повторяет позу робота, вокруг облако точек с Livox Mid-360.

<img width="591" height="1280" alt="rviz_2" src="https://github.com/user-attachments/assets/21de1369-017a-4b64-aa96-67140bfa25fb" />
<img width="591" height="1280" alt="rviz_2" src="https://github.com/user-attachments/assets/4a4bcd63-a0a1-40c0-a4d8-c288e2ae183d" />
<img width="591" height="1280" alt="rviz_2" src="https://github.com/user-attachments/assets/e96538e3-57e8-495c-a2a0-8f6b5dddd05c" />
<img width="591" height="1280" alt="rviz_2" src="https://github.com/user-attachments/assets/c5f08aa9-408e-4b46-95b5-3ff05856c5d9" />
<img width="591" height="1280" alt="rviz_2" src="https://github.com/user-attachments/assets/57eefe27-f225-4edc-a1bc-2c19277c77c3" />
<img width="591" height="1280" alt="rviz_3" src="https://github.com/user-attachments/assets/c92a3d0d-cc71-4b28-bbe3-9a26cbaa631e" />


Робот отдаёт состояние в `unitree_hg/LowState`, а `robot_state_publisher` его не понимает. Мост переводит одно в другое.

## Запуск

```bash
unset CYCLONEDDS_URI
ros2 launch g1_rviz_bridge g1_rviz.launch.py
```

Поднимает мост, `robot_state_publisher`, трансформ до лидара и RViz.


<img width="591" height="1280" alt="rviz_2" src="https://github.com/user-attachments/assets/c01b4b15-bf26-4e59-926e-cd16ae549fa5" /><img width="591" height="1280" alt="rviz_1" src="https://github.com/user-attachments/assets/bbc774c2-f3b5-44e2-8e3f-a18b86ffd42d" />
<img width="591" height="1280" alt="rviz_1" src="https://github.com/user-attachments/assets/2b52f79e-725b-4e7d-9a0f-5a0288cc7d6b" />
<img width="591" height="1280" alt="rviz_1" src="https://github.com/user-attachments/assets/958def97-4db7-4531-96a4-5e55d94b8421" />
<img width="591" height="1280" alt="rviz_1" src="https://github.com/user-attachments/assets/2be19494-29bc-4931-a9ee-6acf87aec1b1" />


## Что нужно

ROS 2 (у меня Foxy на Jetson внутри робота), `unitree_hg` из [unitree_ros2](https://github.com/unitreerobotics/unitree_ros2), URDF и меши из [unitree_ros](https://github.com/unitreerobotics/unitree_ros).

## Сборка

```bash
cd ~/ros2_ws/src
git clone https://github.com/MEIR-005/g1-rviz-bridge.git
cd ~/ros2_ws
colcon build --packages-select g1_rviz_bridge
source install/setup.bash
```

## Топики

Читает `/lowstate` и `/utlidar/cloud_livox_mid360`, публикует `/joint_states` и `/robot_description`.



## Грабли

**Меши не находятся.** В URDF пути относительные, RViz ищет их относительно своей папки. Или запускать из `g1_description/`, или переписать:

```bash
sed 's|filename="meshes/|filename="file:///путь/meshes/|g' g1_29dof.urdf > g1_29dof_abs.urdf
```

**Смещение лидара на глаз** — 0.1 вперёд, 0.5 вверх. По креплению не мерил.

**rclpy и unitree_sdk2py в одном процессе не живут.** Оба создают домен CycloneDDS, второй падает. Поэтому мост подписан на ROS-топик, а не лезет в SDK.

**RViz на другой машине.** Если multicast не проходит, указать адрес робота явно через `CYCLONEDDS_URI` с `<Peers>`. Конфиг нужен на обеих машинах.

## Лицензия

MIT
