import serial
import serial.rs485
import cv2
import time
import threading

# Configure RS485 serial communication
ser = serial.Serial('COM3', 9600)
ser.rs485_mode = serial.rs485.RS485Settings(
    rts_level_for_tx=True, 
    rts_level_for_rx=False, 
    loopback=False,
    delay_before_tx=None, 
    delay_before_rx=None,
)

print(f"Serial port open: {ser.isOpen()}")

# PTZ control commands (Pelco-D protocol)
# cmd_left = bytearray.fromhex('FF 01 00 04 3F FF 74')
# cmd_right = bytearray.fromhex('FF 01 00 02 20 3F 62')
# cmd_stop = bytearray.fromhex('FF 01 00 00 00 00 01')

cmd_pan_left = bytearray.fromhex('FF 01 00 04 3F 00 3A')
cmd_pan_right = bytearray.fromhex('FF 01 00 02 20 00 23')
cmd_tilt_up = bytearray.fromhex('FF 01 00 08 00 10 19')
cmd_tilt_down = bytearray.fromhex('FF 01 00 10 00 3F 50')
cmd_zoom_in = bytearray.fromhex('FF 01 00 20 00 00 21')
cmd_zoom_out = bytearray.fromhex('FF 01 00 40 00 00 41')
#cmd_focus_near = bytearray.fromhex('FF 01 00 80 00 00 62') 
#cmd_focus_far =  bytearray.fromhex('FF 01 01 00 00 00 62')
cmd_stop = bytearray.fromhex('FF 01 00 00 00 00 01')

# Function to send PTZ commands
def send_command(command):
    ser.write(command)
    print(f"Command sent: {command.hex()}")

# Function to control PTZ with timed actions
def ptz_control():
    # Move right for 3 seconds
    send_command(cmd_pan_left)
    time.sleep(10)
    send_command(cmd_stop)
    time.sleep(1)

    send_command(cmd_pan_right)
    time.sleep(10)
    send_command(cmd_stop)
    time.sleep(1)
    
    send_command(cmd_tilt_up)
    time.sleep(5)
    send_command(cmd_stop)
    time.sleep(1)
    
    send_command(cmd_tilt_down)
    time.sleep(5)
    send_command(cmd_stop)
    time.sleep(1)
    
    send_command(cmd_zoom_in)
    time.sleep(5)
    send_command(cmd_stop)
    time.sleep(1)

    send_command(cmd_zoom_out)
    time.sleep(5)
    send_command(cmd_stop)
    time.sleep(1)

# Live stream function
def camera_stream():
    # Replace 'rtsp://...' with your camera's RTSP or HTTP URL
    stream_url = 'rtsp://username:password@camera_ip:554/stream'
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Unable to open camera stream.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame.")
            break

        # Display the live stream
        cv2.imshow("Camera Stream", frame)

        # Exit stream on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run PTZ control and live streaming in parallel
if __name__ == "__main__":
    # Start PTZ control in a separate thread
    ptz_thread = threading.Thread(target=ptz_control)
    ptz_thread.start()

    # Start camera live streaming
    camera_stream()

    # Wait for PTZ thread to finish
    ptz_thread.join()

    # Close the serial connection
    ser.close()
    print("Serial port closed.")
