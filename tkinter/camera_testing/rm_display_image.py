import time
from robomaster import robot
from robomaster import camera


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_camera = ep_robot.camera

    # 显示十秒图传
    ep_camera.start_video_stream(display=True, resolution=camera.STREAM_360P)
    time.sleep(10)
    ep_camera.stop_video_stream()

    ep_robot.close()