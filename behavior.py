import cv2
from aip import AipBodyAnalysis

def detectSmoking():
    # 百度AIP的配置信息
    APP_ID = '32891123'
    API_KEY = 'rYQN28Dmv8zRusPxn4LQfuO8'
    SECRET_KEY = 'admRPxzMPYxRuHWOvt81zeDQCjtqUFNq'

    # 初始化百度AIP客户端
    client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)

    # 调用摄像头
    cap = cv2.VideoCapture(0)

    # 加载人脸检测器
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        # 读取摄像头画面
        ret, frame = cap.read()

        # 转换为灰度图像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 人脸检测
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # 遍历检测到的人脸
        for (x, y, w, h) in faces:
            # 提取人脸区域
            face_img = frame[y:y+h, x:x+w]

            # 将人脸区域转换为二进制格式
            _, img_encoded = cv2.imencode('.jpg', face_img)
            image = img_encoded.tobytes()

            # 调用百度AIP的人体分析接口
            result = client.bodyAttr(image)

            # 解析分析结果
            if 'person_info' in result:
                person_info = result['person_info']
                for person in person_info:
                    # 获取抽烟动作的置信度
                    smoking_score = person['attributes']['smoke']['score']

                    # 判断是否在抽烟
                    if smoking_score > 0.5:
                        label = 'Smoking'
                        color = (0, 0, 255)  # 红色
                    else:
                        label = 'Not Smoking'
                        color = (0, 255, 0)  # 绿色

                    # 在人脸上绘制矩形框和标签
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        # 显示摄像头画面
        cv2.imshow('Camera', frame)

        # 按下ESC键退出循环
        if cv2.waitKey(1) == 27:
            break

    # 释放摄像头资源
    cap.release()

    # 关闭窗口
    cv2.destroyAllWindows()
