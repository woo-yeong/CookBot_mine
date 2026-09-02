import numpy as np
import mujoco
import time
import cv2
from pathlib import Path
from mujoco.glfw import glfw

# 모델 로드
model_path = Path(__file__).with_name("dual_open_manipulator_x.xml")
model = mujoco.MjModel.from_xml_path(str(model_path))
data = mujoco.MjData(model)

# 카메라 ID
left_cam_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, "left_wrist_cam")

# 시각화 설정
scene = mujoco.MjvScene(model, maxgeom=2000)
opt = mujoco.MjvOption()
cam = mujoco.MjvCamera()
cam.azimuth = 90
cam.elevation = -20
cam.distance = 1.5
cam.lookat = np.array([0, 0, 0.3])

# GLFW 윈도우 생성
glfw.init()
window = glfw.create_window(1200, 900, "Dual Robot Arm Simulation", None, None)
glfw.make_context_current(window)
context = mujoco.MjrContext(model, mujoco.mjtFontScale.mjFONTSCALE_150.value)

# 마우스 상태 변수
button_left = False
button_middle = False
button_right = False
lastx, lasty = 0, 0

# 마우스 콜백
def mouse_button(window, button, action, mods):
    global button_left, button_middle, button_right, lastx, lasty
    if button == glfw.MOUSE_BUTTON_LEFT:
        button_left = (action == glfw.PRESS)
    elif button == glfw.MOUSE_BUTTON_MIDDLE:
        button_middle = (action == glfw.PRESS)
    elif button == glfw.MOUSE_BUTTON_RIGHT:
        button_right = (action == glfw.PRESS)
    lastx, lasty = glfw.get_cursor_pos(window)

def mouse_move(window, xpos, ypos):
    global lastx, lasty, cam
    dx, dy = xpos - lastx, ypos - lasty
    if button_left:
        cam.azimuth += dx * 0.5
        cam.elevation -= dy * 0.5
    elif button_middle:
        cam.lookat[0] -= dx * 0.005
        cam.lookat[1] += dy * 0.005
    elif button_right:
        cam.distance *= 1.0 + dy * 0.01
    lastx, lasty = xpos, ypos

def scroll(window, xoffset, yoffset):
    cam.distance *= 1.0 - 0.05 * yoffset

# actuator 이름으로부터 id 매핑
joint_names = [
    "robot1_actuator_joint1", "robot1_actuator_joint2", "robot1_actuator_joint3", "robot1_actuator_joint4", "robot1_actuator_gripper_joint",
    "robot2_actuator_joint1", "robot2_actuator_joint2", "robot2_actuator_joint3", "robot2_actuator_joint4", "robot2_actuator_gripper_joint"
]
joint_ids = {name: mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, name) for name in joint_names}

# 위치 초기화
def reset_position():
    ctrl = data.ctrl
    ctrl[joint_ids["robot1_actuator_joint1"]] = 0.0
    ctrl[joint_ids["robot1_actuator_joint2"]] = -0.8
    ctrl[joint_ids["robot1_actuator_joint3"]] = 1.0
    ctrl[joint_ids["robot1_actuator_joint4"]] = 0.3
    ctrl[joint_ids["robot1_actuator_gripper_joint"]] = 0.0
    ctrl[joint_ids["robot2_actuator_joint1"]] = 0.0
    ctrl[joint_ids["robot2_actuator_joint2"]] = -0.8
    ctrl[joint_ids["robot2_actuator_joint3"]] = 1.0
    ctrl[joint_ids["robot2_actuator_joint4"]] = 0.3
    ctrl[joint_ids["robot2_actuator_gripper_joint"]] = 0.0

# 키보드 콜백
def keyboard(window, key, scancode, act, mods):
    if act != glfw.PRESS:
        return
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    elif key == glfw.KEY_R:
        reset_position()
    elif key == glfw.KEY_SPACE:
        perform_task()
    elif key == glfw.KEY_W:
        data.ctrl[joint_ids["robot1_actuator_joint2"]] += 0.1
    elif key == glfw.KEY_S:
        data.ctrl[joint_ids["robot1_actuator_joint2"]] -= 0.1
    elif key == glfw.KEY_A:
        data.ctrl[joint_ids["robot1_actuator_joint1"]] += 0.1
    elif key == glfw.KEY_D:
        data.ctrl[joint_ids["robot1_actuator_joint1"]] -= 0.1
    elif key == glfw.KEY_I:
        data.ctrl[joint_ids["robot2_actuator_joint2"]] += 0.1
    elif key == glfw.KEY_K:
        data.ctrl[joint_ids["robot2_actuator_joint2"]] -= 0.1
    elif key == glfw.KEY_J:
        data.ctrl[joint_ids["robot2_actuator_joint1"]] += 0.1
    elif key == glfw.KEY_L:
        data.ctrl[joint_ids["robot2_actuator_joint1"]] -= 0.1

def perform_task():
    data.ctrl[joint_ids["robot1_actuator_joint2"]] = 1.5
    data.ctrl[joint_ids["robot1_actuator_joint3"]] = 0.3
    data.ctrl[joint_ids["robot2_actuator_joint2"]] = 1.5
    data.ctrl[joint_ids["robot2_actuator_joint3"]] = 0.3
    time.sleep(1.0)
    data.ctrl[joint_ids["robot1_actuator_gripper_joint"]] = -0.05
    data.ctrl[joint_ids["robot2_actuator_gripper_joint"]] = -0.05
    time.sleep(0.5)
    data.ctrl[joint_ids["robot1_actuator_joint2"]] = -0.8
    data.ctrl[joint_ids["robot1_actuator_joint3"]] = 1.0
    data.ctrl[joint_ids["robot2_actuator_joint2"]] = -0.8
    data.ctrl[joint_ids["robot2_actuator_joint3"]] = 1.0
    time.sleep(1.0)
    data.ctrl[joint_ids["robot1_actuator_gripper_joint"]] = 0.0
    data.ctrl[joint_ids["robot2_actuator_gripper_joint"]] = 0.0
    time.sleep(0.5)

# 콜백 등록
glfw.set_key_callback(window, keyboard)
glfw.set_mouse_button_callback(window, mouse_button)
glfw.set_cursor_pos_callback(window, mouse_move)
glfw.set_scroll_callback(window, scroll)

# 초기화
reset_position()

# 시각화용 카메라 선언
left_mjv_cam = mujoco.MjvCamera()

# OpenCV용 이미지 버퍼
w, h = 640, 480
viewport = mujoco.MjrRect(0, 0, w, h)
img = np.empty((h, w, 3), dtype=np.uint8)  # C-contiguous, uint8 형식

# 메인 루프
while not glfw.window_should_close(window):
    mujoco.mj_step(model, data)

        # 📸 왼쪽 로봇팔 카메라 시점 OpenCV로 렌더링
    cam_pos = data.cam_xpos[left_cam_id]
    cam_mat = data.cam_xmat[left_cam_id].reshape(3, 3)

    # forward (z축 방향): 카메라가 바라보는 방향
    cam_forward = cam_mat[:, 2]
    cam_up = cam_mat[:, 1]

    # 정확히 카메라 위치에서 바라보는 시점 구성
    left_mjv_cam.lookat[:] = cam_pos + 0.05 * cam_forward  # 약간 앞쪽을 보도록
    left_mjv_cam.distance = 0.05                            # 너무 작으면 clipping 생김
    left_mjv_cam.azimuth = 0
    left_mjv_cam.elevation = 0
    left_mjv_cam.trackbodyid = -1

    mujoco.mjv_updateScene(model, data, opt, None, left_mjv_cam, mujoco.mjtCatBit.mjCAT_ALL.value, scene)
    mujoco.mjr_render(viewport, scene, context)
    mujoco.mjr_readPixels(img, None, viewport, context)

    img_flipped = np.flipud(img).copy()
    cv2.imshow("Left Wrist Cam", cv2.cvtColor(img_flipped, cv2.COLOR_RGB2BGR))


    # 🌐 기본 시뮬레이션 뷰 (cam 유지)
    mujoco.mjv_updateScene(model, data, opt, None, cam, mujoco.mjtCatBit.mjCAT_ALL.value, scene)
    framebuffer_size = glfw.get_framebuffer_size(window)
    mujoco.mjr_render(mujoco.MjrRect(0, 0, *framebuffer_size), scene, context)

    glfw.swap_buffers(window)
    glfw.poll_events()

    if cv2.waitKey(1) & 0xFF == 27:
        break

# 종료 처리
cv2.destroyAllWindows()
glfw.terminate()

