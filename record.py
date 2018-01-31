#coding:utf-8

from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PIL import Image
import sys
import train2
import matplotlib.pyplot as plt
import numpy as np
import v

def predict_time(difficult):          # 输入难度系数，返回做题消耗时间
    n = 5
    x = [difficult]
    time = np.dot(train2.pow_train_linx(x, n), train2.theta)
    return time

def savePic1(filename = 'liuwei_history.txt'):       # 此函数输入txt记录文件，输出256*192的柱状图（柱状图记录答题正确与错误）
    d = []
    e = []
    with open(filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()
            if not lines:
                break
            _, _ ,_, d_tmp,e_tmp,_, _,_= [str(i) for i in lines.split('||')]
            d.append(d_tmp)
            e.append(e_tmp)

    true = 0
    false = 0
    y_true = []
    y_false = []
    x = []
    for i in xrange(len(d)):
        if i == 0:
            if int(d[i]) == 0:
                false = false + 1
            else:
                true = true + 1
        else:
            if e[i].strip() == e[i - 1].strip():
                if int(d[i]) == 0:
                    false = false + 1
                else:
                    true = true + 1
                if i == len(d) - 1:
                    y_true.append(true)
                    y_false.append(false)
                    x.append(e[i])
            else:
                y_true.append(true)
                y_false.append(false)
                x.append(e[i-1])
                true = 0
                false = 0
                if int(d[i]) == 0:
                    false = false + 1
                else:
                    true = true + 1
                if i == len(d) - 1:
                    y_true.append(true)
                    y_false.append(false)
                    x.append(e[i])
    total_width, n = 0.4, 2
    width = total_width / n
    x1 = np.arange(len(x))
    x1 = x1 - (total_width - width) / 2
    plt.figure()
    plt.bar(x1, y_true, width=width, label=u'错误做题数')
    plt.bar(x1 + width, y_false, width=width, label=u'正确做题数')
    plt.xticks(x1 + width / 2, x)
    plt.xlabel(u"日期")
    plt.ylabel( u"做题情况")
    plt.title("每日做题概览")
    plt.legend()
    plt.savefig('bar.jpg')
    im = Image.open('bar.jpg')
    out = im.resize((400, 260), Image.ANTIALIAS)
    out.save('\ui_Calculator\wx\\bar.jpg', type='jpg')
    # plt.show()

def savePic2( filename = 'liuwei_history.txt'):    # 此函数输入txt记录文件，保存256*192的折线图（折线图记录日期与答题次数）
    global index
    e = []
    with open(filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()
            if not lines:
                break
            _, _ ,_, _, e_tmp,_, _,_= [str(i) for i in lines.split('||')]
            e.append(e_tmp)

    sum = 0
    y = []
    x = []
    for i in xrange(len(e)):
        if i == 0:
            sum = sum +1
        else:
            if e[i].strip() == e[i-1].strip():
                sum = sum + 1
                if i == len(e)-1:
                    y.append(sum)
                    x.append(e[i])
            else:
                y.append(sum)
                x.append(e[i - 1])
                sum = 1
                if i == len(e)-1:
                    y.append(sum)
                    x.append(e[i])
    if len(x) > 1:
        index = 1
        plt.figure()
        plt.plot(range(0,len(y)), y)
        plt.xticks(range(0,len(y)),x)
        plt.title('每日做题次数')
        plt.xlabel(u'日期', labelpad=5)
        plt.ylabel(u'做题数')
        plt.savefig('line.jpg')
        im1 = Image.open('line.jpg')
        out = im1.resize((400, 260), Image.ANTIALIAS)
        out.save('\ui_Calculator\wx\line.jpg', type='jpg')
    else:
        index = 0

def savePic3(filename = 'liuwei_history.txt'):      # 此函数输入txt记录文件，保存256*192的饼状图
    h = []
    with open(filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()
            if not lines:
                break
            _, _, _, _, _, _, _, h_tmp = [str(i) for i in lines.split('||')]
            h.append(h_tmp)

    true = 0
    false = 0
    for i in h:
        if int(i) == 0:
            false = false + 1
        else:
            true = true + 1

    labels = u'题目不会做', u'题目会做，但做题错误'
    fracs = [false, true] # 这里是需要更改的数字（错误类型所占的百分比）
    explode = [0, 0.1]  # 0.1 凸出这部分，
    plt.axes(aspect=1)
    plt.pie(x=fracs, labels=labels, explode=explode, autopct='%0.1f%%',
            shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6)
    plt.title("错误类型分析")
    plt.savefig('pie.jpg')
    im1 = Image.open('pie.jpg')
    out = im1.resize((400, 260), Image.ANTIALIAS)
    out.save('\ui_Calculator\wx\pie.jpg', type='jpg')

class Ui_RecordForm(QWidget):
    global index
    def __init__(self):
        super(Ui_RecordForm, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon \
        ('E:\ui_Calculator\myapp.ico'))

    def setupUi(self, RecordForm):
        RecordForm.setObjectName("RecordForm")
        RecordForm.resize(1424, 404)
        self.openImageBtn = QtWidgets.QPushButton(RecordForm)
        self.openImageBtn.setGeometry(QtCore.QRect(400, 350, 101, 23))
        self.closeBtn = QtWidgets.QPushButton(RecordForm)
        self.closeBtn.setGeometry(QtCore.QRect(900, 350, 101, 23))
        self.openImageBtn.setObjectName("openImageBtn")
        self.graphicsView = QtWidgets.QGraphicsView(RecordForm)
        self.graphicsView.setGeometry(QtCore.QRect(50, 50, 400, 260))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView_2 = QtWidgets.QGraphicsView(RecordForm)
        self.graphicsView_2.setGeometry(QtCore.QRect(520, 50, 400, 260))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.graphicsView_3 = QtWidgets.QGraphicsView(RecordForm)
        self.graphicsView_3.setGeometry(QtCore.QRect(980, 50, 400, 260))
        self.graphicsView_3.setObjectName("graphicsView_3")

        self.retranslateUi(RecordForm)
        QtCore.QMetaObject.connectSlotsByName(RecordForm)

    def retranslateUi(self, RecordForm):
        _translate = QtCore.QCoreApplication.translate
        RecordForm.setWindowTitle(_translate("RecordForm", "Form"))
        self.openImageBtn.setText(_translate("RecordForm", "显示做题记录"))
        self.openImageBtn.clicked.connect(self.displayPic1)
        self.openImageBtn.clicked.connect(self.displayPic2)
        self.openImageBtn.clicked.connect(self.displayPic3)
        self.closeBtn.setText(_translate("RecordForm", "退出"))
        self.closeBtn.clicked.connect(self.quit)

    def quit(self):
        self.hide()


    def displayPic1(self):
        savePic1(v.username+'_history.txt')
        image1 = QImage()
        image1.load('bar.jpg')
        self.scene = QGraphicsScene()
        self.scene.addPixmap(QPixmap.fromImage(image1))
        self.graphicsView.setScene(self.scene)
        self.graphicsView.resize(image1.width() + 10,image1.height() + 10)
        self.graphicsView.show()


    def displayPic2(self):
        savePic2(v.username+'_history.txt')
        if index == 1:
            image = QImage()
            image.load('line.jpg')
            self.scene = QGraphicsScene()
            self.scene.addPixmap(QPixmap.fromImage(image))
            self.graphicsView_2.setScene(self.scene)
            self.graphicsView_2.resize(image.width() + 10,image.height() + 10)
            self.graphicsView_2.show()
        else:
            image2 = QImage()
            image2.load('warn.jpg')
            self.scene = QGraphicsScene()
            self.scene.addPixmap(QPixmap.fromImage(image2))
            self.graphicsView_2.setScene(self.scene)
            self.graphicsView_2.resize(image2.width() + 10, image2.height() + 10)
            self.graphicsView_2.show()

    def displayPic3(self):
        savePic3(v.username+'_history.txt')
        image3 = QImage()
        image3.load('pie.jpg')
        self.scene = QGraphicsScene()
        self.scene.addPixmap(QPixmap.fromImage(image3))
        self.graphicsView_3.setScene(self.scene)
        self.graphicsView_3.resize(image3.width() + 10, image3.height() + 10)
        self.graphicsView_3.show()


index = 1
if __name__ == "__main__":
    App = QApplication(sys.argv)
    userloginForm = Ui_RecordForm()
    userloginForm.show()
    sys.exit(App.exec_())