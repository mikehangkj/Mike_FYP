import time
import pyaudio
import threading
import robomaster
from robomaster import robot
import wave

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    # 依次播放两个本地文件
    # ep_robot.play_audio(filename="output6.wav").wait_for_completed()
    ep_robot.play_audio(filename="gtts2.wav").wait_for_completed()
    # ep_robot.play_audio(filename="output10.wav").wait_for_completed()
    ep_robot.close()