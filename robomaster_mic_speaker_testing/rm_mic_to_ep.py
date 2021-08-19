import time
import pyaudio
import threading
import robomaster
from robomaster import robot
import time

x=0

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")
    ep_camera = ep_robot.camera

# def play_audio():
#     ep_robot.play_audio(filename="output7.wav").wait_for_completed()

def turn_on_rm_mic():
    global x,start,stop
    audio_player = pyaudio.PyAudio()
    playing_stream = audio_player.open(format=pyaudio.paInt16,channels=1,rate=48000,output=True)
    ep_camera.start_audio_stream()
    # print("main 1")
    # playing_task = threading.Thread(target=audio_playing_task, args=(ep_robot,))
    start=time.time()
    while x<200: #1000 counts is 20 seconds
        try:
            frame = ep_camera.read_audio_frame()
            # print("task 2")
            # print(frame)
        except Exception as e:
            print("LiveView: playing_task, video_frame_queue is empty.")
            continue
        # print("task 3")
        playing_stream.write(frame)
        x+=1
        # print("writing frame")
    x=0
    playing_stream.stop_stream()
    playing_stream.close()
    # ep_camera.stop_audio_stream()
    stop=time.time()


# play_audio()
turn_on_rm_mic()
print("total time taken 1:" + str(stop-start) + "seconds")
# time.sleep(2)
# turn_on_rm_mic()
# print("total time taken 2:" + str(stop-start) + "seconds")

# time.sleep(20)
# print("main 2")
# print("total time taken:" + str(stop-start) + "seconds")

ep_robot.close()
ep_camera.stop_audio_stream()