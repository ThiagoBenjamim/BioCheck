import cv2
import time
import serial.tools.list_ports


"""ports = serial.tools.list_ports.comports()
serial_inst = serial.Serial()

ports_list = []

for port in ports:
    ports_list.append(str(port))
    print(str(port))

val: str = input('Select Port: COM')

for i in range(len(ports_list)):
    if ports_list[i].startswith(f'COM{val}'):
        port_var = f'COM{val}'
        print(port_var)

serial_inst.baudrate = 9600
serial_inst.port = port_var
serial_inst.open()"""


COLORS =[(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

class_names= []
with open("coco.names", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

cap = cv2.VideoCapture(0)

net = cv2.dnn.readNet("yolov7-tiny.weights", "yolov7-tiny.cfg")

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255)

while True:

    _, frame = cap.read()

    start = time.time()

    classes, scores, boxes = model.detect(frame, 0.1, 0.2)

    end = time.time()

    for(classid, score, box) in zip(classes, scores, boxes):

        color = COLORS[int(classid) % len(COLORS)]

        label = f"{class_names[classid]} : {score}"

        cv2.rectangle(frame, box, color, 2)

        cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, color, 2)
    
    fps_label = f"FPS: {round(1.0/(end - start)),2}"

    cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 5)
    cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

    cv2.imshow("detections", frame)

    if cv2.waitKey(20) and 0xFF==ord('d'):
        break

cap.release()
cv2.destroyAllWindows()
