import sys

import ui.camera as camera

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5 import QtCore, QtGui, uic
import cv2


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.ui = uic.loadUi('./ui/camera.ui') # 里面的exec不用管，已经有的close管用，也不用管
        self.ui.camera.clicked.connect(self.runCamera)# 相当于重置？

        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.cap = cv2.VideoCapture()  # 视频流
        self.CAM_NUM = 0

    def runCamera(self):
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self.cap.open(self.CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                msg = QMessageBox.warning(self, 'warning', "请检查相机于电脑是否连接正确",
                                          buttons=QMessageBox.Ok)
            else:
                self.timer_camera.start(10)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.timer_camera.timeout.connect(self.show_camera)
                self.ui.camera.setText('关闭相机')
        else:
            self.timer_camera.stop()  # 关闭定时器
            self.cap.release()  # 释放视频流
            self.ui.master.clear()  # 清空视频显示区域
            self.ui.camera.setText('打开相机')
            self.ui.master.setText('主相机')
            self.ui.sub1.setText('从相机1')
            self.ui.sub2.setText('从相机2')
            self.ui.BP.setText('算法估计')
        pass

    def show_camera(self):
        flag, self.image = self.cap.read()  # 从视频流中读取
        # todo 根据ak的代码改变一下showImage部分ok了
        show = cv2.resize(self.image, (640, 480))  # 把读到的帧的大小重新设置为 640x480
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                 QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.ui.master.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage


if __name__ == '__main__':
    app = QApplication(sys.argv)
    DL = MainWindow()
    DL.ui.show()
    sys.exit(app.exec_())
