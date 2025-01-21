import cv2
import DateTime
import serial.tools.list_ports
import time

packet = ["", "", "", "", "", ""]
ports = serial.tools.list_ports.comports()
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
serial_inst.open()


COLORS =[(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

class_names= []
with open("coco.names", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

cap = cv2.VideoCapture(1)

net = cv2.dnn.readNet("yolov7-tiny.weights", "yolov7-tiny.cfg")

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255)

while True:
    if serial_inst.in_waiting:
        packet = []
        packet = serial_inst.readline()
        packet = packet.decode("utf").strip()
        packet = packet.split()
    if len(packet) < 5:
        packet = ["", "", "", "", "", ""]
    print(packet)

    _, frame = cap.read()

    start = time.time()

    classes, scores, boxes = model.detect(frame, 0.1, 0.2)

    end = time.time()

    for(classid, score, box) in zip(classes, scores, boxes):

        color = COLORS[int(classid) % len(COLORS)]

        label = f"{class_names[classid]} : {score}"

        cv2.rectangle(frame, box, color, 2)

        cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, color, 1)
    
    fps_label = f"FPS: {round(1.0/(end - start)), 2}"

    '''cv2.putText(frame, time, (0, 25), cv2.FONT_HERSHEY_TRIPLEX, 1, (170, 213, 118), 2)'''
    cv2.putText(frame, (f"Luminosidade: {packet[0]}"), (0, 25), cv2.FONT_HERSHEY_TRIPLEX, 1, (115, 169, 66), 2)
    cv2.putText(frame, (f"Umidade do ar: {packet[1]}"), (0, 55), cv2.FONT_HERSHEY_TRIPLEX, 1, (83, 141, 34), 2)
    cv2.putText(frame, (f"Umidade do solo: {packet[2]}"), (0, 85), cv2.FONT_HERSHEY_TRIPLEX, 1, (36, 85, 1), 2)
    cv2.putText(frame, (f"Nivel de agua: {packet[3]}"), (0, 115), cv2.FONT_HERSHEY_TRIPLEX, 1, (26, 67, 1), 2)
    cv2.putText(frame, (f"Temperatura(Celcius): {packet[4]}"), (0, 145), cv2.FONT_HERSHEY_TRIPLEX, 1, (20, 54, 1), 2)

    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow("window", frame)

    if cv2.waitKey(20) and 0xFF==ord('d'):
        break

cap.release()
cv2.destroyAllWindows()