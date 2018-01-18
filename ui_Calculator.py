#!/usr/bin/python
# -*- coding:utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from fractions import Fraction
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer
import os
import pandas as pd
import sys
import numpy as np
import random
import time
import datetime

# 生成指定数量的随机运算符
def produce_operators(op_num=3):
    op = []                        # 记录生成的op_num个四则运算操作数
    for i in xrange(op_num):
        temp = random.choice(['＋','－','×','÷'])
        op.append(temp)
    return op

# 生成指定数量的随机整数和随机真分数
def produce_numbers(int_num=2,pro_frac_num=2):
    num = []                      # 记录生成的op_num+1个数（包括整数和真分数）
    for i in xrange(int_num):
        int_number = random.randint(0,99)
        temp = Fraction(int_number, 1)  # 生成随机整数
        num.append(temp)
    for i in xrange(pro_frac_num):
        denominator = random.randint(1,99)  # 分母（分母不为0）
        numerator = random.randint(0,denominator-1) # 分子
        proper_fraction = Fraction(numerator,denominator) # 生成随机真分数
        num.append(proper_fraction)
    return num

# 生成题目
def produce_problem(op_num,num,op):
    problem = []
    for i in xrange(op_num):
        number = random.choice(num)
        problem.append(number)
        num.remove(number)
        operator = random.choice(op)
        problem.append(operator)
        op.remove(operator)
        if i == op_num - 1:
            problem.append(num[0])
    return problem

# 打印题目
def display_problem(problem):
    record_problem = ''
    for i in problem:
        temp = str(i)
        record_problem = record_problem +temp
    record_problem = record_problem + '='
    # print record_problem,
    #print unicode(record_problem, 'utf-8').encode('gbk'),
    return record_problem

# 计算题目正确结果
def calculate_result(problem):
    result = ''
    for i in problem:
        if type(i) == type(Fraction(2,3)):
            numerator_temp = i.numerator
            denominator_temp = i.denominator
            temp = 'Fraction(%d,%d)'%(numerator_temp,denominator_temp)
        else:
            if i == '＋':
                temp = '+'
            elif i == '－':
                temp = '-'
            elif i == '×':
                temp = '*'
            else:
                temp = '/'
        result = result + temp
    final_result = str(eval(result))
    # print result
    # print final_result
    return final_result

# 记录测试信息
def record_test(show_problem, result, answer, judge_result):
    message = []
    message.append(str(show_problem) + '    ')
    message.append(str(result) + '    ')
    message.append(str(answer) + '    ')
    message.append(str(judge_result) + '    \n')
    return np.array(message)

# 判断答题者答案是否正确
def judge(answer,result):
    if answer.strip() == result.strip():  # 判断正误
        return 1
    else:
        return 0

# 判断题目是否有可能重复（设置异常）
def isrepetition(problem,choose):
    global test_data
    global examination_data
    if choose == 'test':
        if problem in test_data[:,0]:
            raise NameError
    elif choose == 'examination':
        if problem in examination_data[:,0]:
            raise NameError
    return None

# 打印测试试题等信息
def output_testdata(name,control=0,accuracy=''):
    global test_data
    global examination_data
    test_data_path = '%s'%(name)
    f = open(test_data_path,'a')
    time_stamp = datetime.datetime.now()
    if control == 0:
        f.write('日期：' + time_stamp.strftime('%Y.%m.%d') + '\n\n')
        f.write('序号  题目  正确答案  答题者答案  是否正确（0错误 1正确）\n')
        for i in xrange(test_data.shape[0]):
            f.write('（%d） '%(i+1))
            f.writelines(test_data[i])
            f.write('\n')
        f.write('本次考试最终得分：%s   ----------------------------------------------------------------------'
                '-------------------------------------' % (accuracy) + '\n\n\n')
        f.close()
    elif control == 1:
        f.write('日期：' + time_stamp.strftime('%Y.%m.%d') + '\n\n')
        f.write('序号  题目  加号数  减号数  乘号数  除号数  正确答案分子  '
                '正确答案分母  正确答案  答题者回答（0错误 1正确）\n\n')
        for i in xrange(examination_data.shape[0]):
            f.write('（%d） '%(i+1))
            f.writelines(examination_data[i])
            f.write('\n')
        f.write('本次考试最终得分：%s   ----------------------------------------------------------------------'
                    '-------------------------------------'%(accuracy) + '\n\n\n')
        f.close()

def calculate_accuracy():
    global test_data
    correct_question_num = 0
    total_question_num = test_data.shape[0]
    for i in xrange(total_question_num):
        correct_question_num = correct_question_num + int(test_data[i, 3])
    if total_question_num == 0:
        accuracy = "{:%}".format(0)
    else:
        accuracy = "{:%}".format(1.0 * correct_question_num / total_question_num)
    return accuracy

class Ui_UserLoginForm(QWidget):
    def __init__(self):
        super(Ui_UserLoginForm, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon \
        ('E:\ui_Calculator\myapp.ico'))

        self.path = 'E:\ui_Calculator\userdata.csv'
        self.filename = 'userdata.csv'

    def setupUi(self, calculatorForm):
        calculatorForm.setObjectName("calculatorForm")
        calculatorForm.resize(250, 200)
        self.gridLayout = QtWidgets.QGridLayout(calculatorForm)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(0, 0, -1, 0)
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.userLabel = QtWidgets.QLabel(calculatorForm)
        self.userLabel.setObjectName("userLabel")
        self.horizontalLayout.addWidget(self.userLabel)
        self.userLineEdit = QtWidgets.QLineEdit(calculatorForm)
        self.userLineEdit.setObjectName("userLineEdit")
        self.horizontalLayout.addWidget(self.userLineEdit)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(7, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pwdBtn = QtWidgets.QLabel(calculatorForm)
        self.pwdBtn.setObjectName("pwdBtn")
        self.horizontalLayout_2.addWidget(self.pwdBtn)
        self.pwdLineEdit = QtWidgets.QLineEdit(calculatorForm)
        self.pwdLineEdit.setObjectName("pwdLineEdit")
        self.pwdLineEdit.setEchoMode(2)
        self.horizontalLayout_2.addWidget(self.pwdLineEdit)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(30, -1, 30, -1)
        self.horizontalLayout_3.setSpacing(20)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.loginBtn = QtWidgets.QPushButton(calculatorForm)
        self.loginBtn.setObjectName("loginBtn")
        self.loginBtn.setFocus()
        self.loginBtn.setDefault(True)
        self.horizontalLayout_3.addWidget(self.loginBtn)
        self.regisBtn = QtWidgets.QPushButton(calculatorForm)
        self.regisBtn.setObjectName("regisBtn")
        self.horizontalLayout_3.addWidget(self.regisBtn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.retranslateUi(calculatorForm)
        self.loginBtn.clicked.connect(self.login)
        self.regisBtn.clicked.connect(self.register)
        QtCore.QMetaObject.connectSlotsByName(calculatorForm)

    def retranslateUi(self, calculatorForm):
        _translate = QtCore.QCoreApplication.translate
        calculatorForm.setWindowTitle(_translate("calculatorForm", "Calculator"))
        self.userLabel.setText(_translate("calculatorForm", "用户名："))
        self.pwdBtn.setText(_translate("calculatorForm", "密 码："))
        self.loginBtn.setText(_translate("calculatorForm", "登录"))
        self.regisBtn.setText(_translate("calculatorForm", "注册"))

    def register(self):
        if self.userLineEdit.text() and self.pwdLineEdit.text():
            if os.path.isfile(self.path):
                df = pd.read_csv(self.filename)
                if str(self.userLineEdit.text()) in list((df['username'])):
                    self.informationMessage1()
                else:
                    df1 = pd.DataFrame({'username': [str(self.userLineEdit.text())],
                                        'password': [str(self.pwdLineEdit.text())]})
                    result = df.append(df1)
                    result.to_csv(self.filename, index=False, sep=',')
                    self.informationMessage4()
            else:
                df = pd.DataFrame({'username': [str(self.userLineEdit.text())],
                                   'password': [str(self.pwdLineEdit.text())]})
                df.to_csv(self.filename, index=False, sep=',')
                self.informationMessage4()
        else:
            self.informationMessage()

    def login(self):
        global username
        if os.path.isfile(self.path):
            if self.userLineEdit.text() and self.pwdLineEdit.text():
                df = pd.read_csv(self.filename)
                if str(self.userLineEdit.text()) in list(df['username']):
                    index = list(df['username']).index(str(self.userLineEdit.text()))
                    if str(self.pwdLineEdit.text()) == list(df['password'])[index]:
                        username = str(self.userLineEdit.text())
                        self.close()
                        self.modeselect = Ui_ModeSelectMainWindow()
                        self.modeselect.show()
                    else:
                        self.informationMessage2()
                else:
                    self.informationMessage3()
            else:
                self.informationMessage()
        else:
            self.informationMessage3()

    def informationMessage(self):
        MESSAGE = "请输入用户名和密码"
        reply = QMessageBox.information(self,
                "登录失败", MESSAGE)

    def informationMessage1(self):
        MESSAGE = "用户名已被注册"
        reply = QMessageBox.information(self,
                "登录失败", MESSAGE)

    def informationMessage2(self):
        MESSAGE = "密码错误"
        reply = QMessageBox.information(self,
                "登录失败", MESSAGE)

    def informationMessage3(self):
        MESSAGE = "用户名不存在，请注册！"
        reply = QMessageBox.information(self,
                "登录失败", MESSAGE)

    def informationMessage4(self):
        MESSAGE = "注册成功！"
        reply = QMessageBox.information(self,
                "登录失败", MESSAGE)

class Ui_ModeSelectMainWindow(QMainWindow):
    def __init__(self):
        super(Ui_ModeSelectMainWindow,self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon \
        ('E:\ui_Calculator\myapp.ico'))

    def setupUi(self, calculatorMainWindow):
        calculatorMainWindow.setObjectName("calculatorMainWindow")
        calculatorMainWindow.resize(201, 281)
        self.centralwidget = QtWidgets.QWidget(calculatorMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.practiceBtn = QtWidgets.QPushButton(self.centralwidget)
        self.practiceBtn.setGeometry(QtCore.QRect(60, 30, 81, 31))
        self.practiceBtn.setObjectName("practiceBtn")
        self.testBtn = QtWidgets.QPushButton(self.centralwidget)
        self.testBtn.setGeometry(QtCore.QRect(60, 110, 81, 31))
        self.testBtn.setObjectName("testBtn")
        self.examinationBtn = QtWidgets.QPushButton(self.centralwidget)
        self.examinationBtn.setGeometry(QtCore.QRect(60, 190, 81, 31))
        self.examinationBtn.setObjectName("examinationBtn")
        calculatorMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(calculatorMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 201, 23))
        self.menubar.setObjectName("menubar")
        calculatorMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(calculatorMainWindow)
        self.statusbar.setObjectName("statusbar")
        calculatorMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(calculatorMainWindow)
        self.practiceBtn.clicked.connect(self.showpractice)
        self.testBtn.clicked.connect(self.showtest)
        self.examinationBtn.clicked.connect(self.showexamination)
        QtCore.QMetaObject.connectSlotsByName(calculatorMainWindow)

    def retranslateUi(self, calculatorMainWindow):
        _translate = QtCore.QCoreApplication.translate
        calculatorMainWindow.setWindowTitle(_translate("calculatorMainWindow", "Calculator"))
        self.practiceBtn.setText(_translate("calculatorMainWindow", "练习模式"))
        self.testBtn.setText(_translate("calculatorMainWindow", "测试模式"))
        self.examinationBtn.setText(_translate("calculatorMainWindow", "考试模式"))

    def showpractice(self):
        self.pronumForm = Ui_ProNumForm()
        self.pronumForm.show()

    def showtest(self):
        self.protimeForm = Ui_ProTimeForm()
        self.protimeForm.show()

    def showexamination(self):
        self.pronumtimeForm = Ui_ProNumTimeForm()
        self.pronumtimeForm.show()

class Ui_ProNumForm(QWidget):
    def __init__(self):
        super(Ui_ProNumForm,self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon \
        ('E:\ui_Calculator\myapp.ico'))

    def setupUi(self, ProNumForm):
        ProNumForm.setObjectName("ProNumForm")
        ProNumForm.resize(210, 92)
        self.pronumLabel = QtWidgets.QLabel(ProNumForm)
        self.pronumLabel.setGeometry(QtCore.QRect(-20, 30, 141, 16))
        self.pronumLabel.setObjectName("pronumLabel")
        self.pronumLineEdit = QtWidgets.QLineEdit(ProNumForm)
        self.pronumLineEdit.setGeometry(QtCore.QRect(110, 30, 81, 20))
        self.pronumLineEdit.setObjectName("pronumLineEdit")
        self.pushBtn = QtWidgets.QPushButton(ProNumForm)
        self.pushBtn.setGeometry(QtCore.QRect(110, 60, 51, 23))
        self.pushBtn.setObjectName("pushBtn")

        self.retranslateUi(ProNumForm)
        self.pushBtn.clicked.connect(self.showpracticeForm)
        QtCore.QMetaObject.connectSlotsByName(ProNumForm)

    def retranslateUi(self, ProNumForm):
        _translate = QtCore.QCoreApplication.translate
        ProNumForm.setWindowTitle(_translate("ProNumForm", "Calculator"))
        self.pronumLabel.setText(_translate("ProNumForm", "　　　请输入题目数量："))
        self.pushBtn.setText(_translate("ProNumForm", "确定"))

    def showpracticeForm(self):
        global num
        try:
            if int(self.pronumLineEdit.text()) > 0:
                num = int(self.pronumLineEdit.text())
                self.close()
                self.practiceForm = Ui_PracticeForm()
                self.practiceForm.show()
            else:
                self.informationMessage()
        except:
            self.informationMessage()

    def informationMessage(self):
        MESSAGE = "请输入一个大于0的数字"
        reply = QMessageBox.information(self,
                                        "输入失败", MESSAGE)

class Ui_ProTimeForm(QWidget):
    def __init__(self):
        super(Ui_ProTimeForm,self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon \
        ('E:\ui_Calculator\myapp.ico'))

    def setupUi(self, ProTimeForm):
        ProTimeForm.setObjectName("ProTimeForm")
        ProTimeForm.resize(245, 92)
        self.protimeLabel = QtWidgets.QLabel(ProTimeForm)
        self.protimeLabel.setGeometry(QtCore.QRect(10, 30, 141, 16))
        self.protimeLabel.setObjectName("protimeLabel")
        self.protimeLineEdit = QtWidgets.QLineEdit(ProTimeForm)
        self.protimeLineEdit.setGeometry(QtCore.QRect(135, 30, 81, 20))
        self.protimeLineEdit.setObjectName("protimeLineEdit")
        self.pushBtn = QtWidgets.QPushButton(ProTimeForm)
        self.pushBtn.setGeometry(QtCore.QRect(135, 60, 51, 23))
        self.pushBtn.setObjectName("pushBtn")

        self.retranslateUi(ProTimeForm)
        self.pushBtn.clicked.connect(self.showtestForm)
        QtCore.QMetaObject.connectSlotsByName(ProTimeForm)

    def retranslateUi(self, ProTimeForm):
        _translate = QtCore.QCoreApplication.translate
        ProTimeForm.setWindowTitle(_translate("ProTimeForm", "Calculator"))
        self.protimeLabel.setText(_translate("ProTimeForm", "请输入测试时间(min)："))
        self.pushBtn.setText(_translate("ProTimeForm", "确定"))

    def showtestForm(self):
        global time
        try:
            if int(self.protimeLineEdit.text()) > 0:
                time = int(self.protimeLineEdit.text())
                self.close()
                self.testForm = Ui_TestForm()
                self.testForm.show()
            else:
                self.informationMessage()
        except:
            self.informationMessage()

    def informationMessage(self):
        MESSAGE = "请输入一个大于0的数字"
        reply = QMessageBox.information(self,
                                        "输入失败", MESSAGE)

class Ui_ProNumTimeForm(QWidget):
    def __init__(self):
        super(Ui_ProNumTimeForm, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon \
        ('E:\ui_Calculator\myapp.ico'))

    def setupUi(self, ProNumTimeForm):
        ProNumTimeForm.setObjectName("ProNumTimeForm")
        ProNumTimeForm.resize(232, 121)
        self.pronumLabel = QtWidgets.QLabel(ProNumTimeForm)
        self.pronumLabel.setGeometry(QtCore.QRect(10, 20, 141, 16))
        self.pronumLabel.setObjectName("pronumLabel")
        self.pronumLineEdit = QtWidgets.QLineEdit(ProNumTimeForm)
        self.pronumLineEdit.setGeometry(QtCore.QRect(132, 20, 81, 20))
        self.pronumLineEdit.setObjectName("pronumLineEdit")
        self.pushBtn = QtWidgets.QPushButton(ProNumTimeForm)
        self.pushBtn.setGeometry(QtCore.QRect(132, 80, 51, 23))
        self.pushBtn.setObjectName("pushBtn")
        self.protimeLabel = QtWidgets.QLabel(ProNumTimeForm)
        self.protimeLabel.setGeometry(QtCore.QRect(10, 50, 141, 16))
        self.protimeLabel.setObjectName("protimeLabel")
        self.protimeLineEdit = QtWidgets.QLineEdit(ProNumTimeForm)
        self.protimeLineEdit.setGeometry(QtCore.QRect(132, 50, 81, 20))
        self.protimeLineEdit.setObjectName("protimeLineEdit")

        self.retranslateUi(ProNumTimeForm)
        self.pushBtn.clicked.connect(self.showexaminationForm)
        QtCore.QMetaObject.connectSlotsByName(ProNumTimeForm)

    def retranslateUi(self, ProNumTimeForm):
        _translate = QtCore.QCoreApplication.translate
        ProNumTimeForm.setWindowTitle(_translate("ProNumTimeForm", "Calculator"))
        self.pronumLabel.setText(_translate("ProNumTimeForm", "请输入题目数量："))
        self.pushBtn.setText(_translate("ProNumTimeForm", "确定"))
        self.protimeLabel.setText(_translate("ProNumTimeForm", "请输入测试时间(min)："))

    def showexaminationForm(self):
        global num, time
        try:
            if int(self.pronumLineEdit.text()) > 0 and int(self.protimeLineEdit.text()) > 0:
                num = int(self.pronumLineEdit.text())
                time = int(self.protimeLineEdit.text())
                self.close()
                self.examinationForm = Ui_ExaminationForm()
                self.examinationForm.show()
            else:
                self.informationMessage()
        except:
            self.informationMessage()

    def informationMessage(self):
        MESSAGE = "请输入一个大于0的数字"
        reply = QMessageBox.information(self,
                                        "输入失败", MESSAGE)

class Ui_PracticeForm(QWidget):
    def __init__(self):
        super(Ui_PracticeForm,self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon \
        ('E:\ui_Calculator\myapp.ico'))
        self.practiceflag = 0
        self.practiceflag1 = 0

    def setupUi(self, PracticeForm):
        global num
        PracticeForm.setObjectName("PracticeForm")
        PracticeForm.resize(471, 333)
        self.propractLabel = QtWidgets.QLabel(PracticeForm)
        self.propractLabel.setGeometry(QtCore.QRect(30, 20, 111, 16))
        self.propractLabel.setObjectName("propractLabel")
        self.propracEdit = QtWidgets.QTextEdit(PracticeForm)
        self.propracEdit.setGeometry(QtCore.QRect(30, 40, 231, 201))
        self.propracEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.propracEdit.setObjectName("propracEdit")
        self.useranswerLabel = QtWidgets.QLabel(PracticeForm)
        self.useranswerLabel.setGeometry(QtCore.QRect(30, 260, 111, 16))
        self.useranswerLabel.setObjectName("useranswerLabel")
        self.useranswerLineEdit = QtWidgets.QLineEdit(PracticeForm)
        self.useranswerLineEdit.setGeometry(QtCore.QRect(130, 260, 131, 20))
        self.useranswerLineEdit.setObjectName("useranswerLineEdit")
        self.proresidueLabel = QtWidgets.QLabel(PracticeForm)
        self.proresidueLabel.setGeometry(QtCore.QRect(320, 30, 111, 16))
        self.proresidueLabel.setObjectName("proresidueLabel")
        self.answerLabel = QtWidgets.QLabel(PracticeForm)
        self.answerLabel.setGeometry(QtCore.QRect(320, 110, 111, 16))
        self.answerLabel.setObjectName("answerLabel")
        self.answerTextEdit = QtWidgets.QTextEdit(PracticeForm)
        self.answerTextEdit.setGeometry(QtCore.QRect(320, 130, 121, 171))
        self.answerTextEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.answerTextEdit.setObjectName("answerTextEdit")
        self.useranswerBtn = QtWidgets.QPushButton(PracticeForm)
        self.useranswerBtn.setGeometry(QtCore.QRect(130, 290, 71, 23))
        self.useranswerBtn.setObjectName("useranswerBtn")
        self.saveBtn = QtWidgets.QPushButton(PracticeForm)
        self.saveBtn.setGeometry(QtCore.QRect(210, 290, 91, 23))
        self.saveBtn.setObjectName("saveBtn")
        self.beginBtn = QtWidgets.QPushButton(PracticeForm)
        self.beginBtn.setGeometry(QtCore.QRect(10, 290, 111, 23))
        self.beginBtn.setObjectName("beginBtn")
        self.proresidueLineEdit = QtWidgets.QTextEdit(PracticeForm)
        self.proresidueLineEdit.setEnabled(True)
        self.proresidueLineEdit.setGeometry(QtCore.QRect(320, 50, 121, 24))
        self.proresidueLineEdit.setUndoRedoEnabled(True)
        self.proresidueLineEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.proresidueLineEdit.setObjectName("proresidueLineEdit")

        self.retranslateUi(PracticeForm)
        self.proresidueLineEdit.setText(str(num))
        self.beginBtn.clicked.connect(self.runpractice)
        self.useranswerBtn.clicked.connect(self.getanswer)
        self.saveBtn.clicked.connect(self.save)
        QtCore.QMetaObject.connectSlotsByName(PracticeForm)

    def retranslateUi(self, PracticeForm):
        _translate = QtCore.QCoreApplication.translate
        PracticeForm.setWindowTitle(_translate("PracticeForm", "Calculator"))
        self.propractLabel.setText(_translate("PracticeForm", "练习题目："))
        self.useranswerLabel.setText(_translate("PracticeForm", "请输入你的回答："))
        self.proresidueLabel.setText(_translate("PracticeForm", "剩余题目数量："))
        self.answerLabel.setText(_translate("PracticeForm", "作答结果："))
        self.useranswerBtn.setText(_translate("PracticeForm", "提交答案"))
        self.saveBtn.setText(_translate("PracticeForm", "保存本次练习"))
        self.beginBtn.setText(_translate("PracticeForm", "开始答题/下一题"))

    def runpractice(self):
        global num, test_data
        try:
            if num > 0:
                self.test()
                num = num - 1
                self.practiceflag1 = 1
                self.proresidueLineEdit.setText(str(num))
            elif num == 0:
                self.informationMessage4()
            else:
                self.informationMessage1()
        except:
            pass

    # 对答题者进行测试
    def test(self):
        global test_data
        self.op_num = random.randint(1, 4)  # 随机生成的运算符个数
        self.pro_frac_num = random.randint(0, self.op_num)  # 随机生成的真分数个数
        self.int_num = self.op_num + 1 - self.pro_frac_num  # 生成整数个数
        self.op = produce_operators(self.op_num)  # 随机生成指定数量的运算符
        self.num = produce_numbers(self.int_num, self.pro_frac_num)  # 生成指定数量的随机整数和随机真分数
        self.problem = produce_problem(self.op_num, self.num, self.op)  # 生成题目
        self.result = calculate_result(self.problem)  # 计算题目正确结果
        self.show_problem = display_problem(self.problem)
        isrepetition(self.show_problem + '    ', 'test')
        self.propracEdit.append(self.show_problem)
        test_data = np.row_stack([test_data, record_test
        (self.show_problem, self.result, '该题未作答', '0')])

    def getanswer(self):
        global test_data, num
        try:
            if num >= 0:
                self.answer = str(self.useranswerLineEdit.text())
                self.judge_result = judge(self.answer, self.result)  # 判断答题者答案
                if self.judge_result == 0:
                    self.answerTextEdit.setText('回答错误，正确答案是%s'%(self.result))
                else:
                    self.answerTextEdit.setText('回答正确')
                if self.answer == '':
                    pass
                else:
                    if test_data.shape[0] == 1:
                        test_data[0,2] = str(self.answer) + '    '
                        test_data[0,3] = str(self.judge_result) + '    \n'
                    else:
                        test_data[-1][2] = str(self.answer) + '    '
                        test_data[-1][3] = str(self.judge_result) + '    \n'
                if num == 0:
                    num = num - 1
                    self.practiceflag = 1
                    self.propracEdit.append('\n\n\n练习已结束!')
                    self.propracEdit.append('\n本次测试的正确率为：%s' % (str(calculate_accuracy())))
            else:
                self.informationMessage1()
        except:
            if self.practiceflag1 == 1:
                self.answerTextEdit.setText('回答错误！')
            else:
                self.informationMessage()

    def informationMessage(self):
        MESSAGE = "请单击开始答题根据题目作答！"
        reply = QMessageBox.information(self,
                                        "输入失败", MESSAGE)

    def informationMessage1(self):
        MESSAGE = "练习已结束！"
        reply = QMessageBox.information(self,
                                        "输入失败", MESSAGE)

    def informationMessage2(self):
        MESSAGE = "文件已保存完毕！"
        reply = QMessageBox.information(self,
                                        "输入失败", MESSAGE)

    def informationMessage3(self):
        MESSAGE = "请先作答完毕！"
        reply = QMessageBox.information(self,
                                        "输入失败", MESSAGE)

    def informationMessage4(self):
        MESSAGE = "请提交最后一题的答案！"
        reply = QMessageBox.information(self,
                                        "输入失败", MESSAGE)

    def save(self):
        global username, num
        if self.practiceflag == 1:
            output_testdata('E:\ui_Calculator\userdata\%s'%(username + '_practice_data.txt'),
                            control=0,accuracy=str(calculate_accuracy()))
            self.informationMessage2()
            self.practiceflag = 2
        elif self.practiceflag == 2:
            self.informationMessage2()
        else:
            if num >= 0:
                self.informationMessage3()

class Ui_TestForm(QWidget):
    def __init__(self):
        global time
        super(Ui_TestForm,self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon \
        ('E:\ui_Calculator\myapp.ico'))
        self.timer = QTimer(self)
        self.second = 60
        self.testflag = 1
        self.minute = time
        self.timer.timeout.connect(self.showNum)

    def setupUi(self, TestForm):
        global time
        TestForm.setObjectName("TestForm")
        TestForm.resize(471, 333)
        self.protesttLabel = QtWidgets.QLabel(TestForm)
        self.protesttLabel.setGeometry(QtCore.QRect(30, 20, 111, 16))
        self.protesttLabel.setObjectName("protesttLabel")
        self.protestEdit = QtWidgets.QTextEdit(TestForm)
        self.protestEdit.setEnabled(True)
        self.protestEdit.setGeometry(QtCore.QRect(30, 40, 231, 201))
        self.protestEdit.setUndoRedoEnabled(True)
        self.protestEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.protestEdit.setObjectName("protestEdit")
        self.useranswerLabel = QtWidgets.QLabel(TestForm)
        self.useranswerLabel.setGeometry(QtCore.QRect(30, 260, 111, 16))
        self.useranswerLabel.setObjectName("useranswerLabel")
        self.useranswerLineEdit = QtWidgets.QLineEdit(TestForm)
        self.useranswerLineEdit.setGeometry(QtCore.QRect(130, 260, 131, 20))
        self.useranswerLineEdit.setObjectName("useranswerLineEdit")
        self.timeresidueLabel = QtWidgets.QLabel(TestForm)
        self.timeresidueLabel.setGeometry(QtCore.QRect(320, 30, 111, 16))
        self.timeresidueLabel.setObjectName("timeresidueLabel")
        self.answerLabel = QtWidgets.QLabel(TestForm)
        self.answerLabel.setGeometry(QtCore.QRect(320, 110, 111, 16))
        self.answerLabel.setObjectName("answerLabel")
        self.answerTextEdit = QtWidgets.QTextEdit(TestForm)
        self.answerTextEdit.setGeometry(QtCore.QRect(320, 130, 121, 171))
        self.answerTextEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.answerTextEdit.setObjectName("answerTextEdit")
        self.useranswerBtn = QtWidgets.QPushButton(TestForm)
        self.useranswerBtn.setGeometry(QtCore.QRect(130, 290, 71, 23))
        self.useranswerBtn.setObjectName("useranswerBtn")
        self.saveBtn = QtWidgets.QPushButton(TestForm)
        self.saveBtn.setGeometry(QtCore.QRect(210, 290, 91, 23))
        self.saveBtn.setObjectName("saveBtn")
        self.beginBtn = QtWidgets.QPushButton(TestForm)
        self.beginBtn.setGeometry(QtCore.QRect(30, 290, 71, 23))
        self.beginBtn.setObjectName("beginBtn")
        self.timeresidueTextEdit = QtWidgets.QTextEdit(TestForm)
        self.timeresidueTextEdit.setGeometry(QtCore.QRect(320, 50, 104, 24))
        self.timeresidueTextEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.timeresidueTextEdit.setObjectName("timeresidueTextEdit")

        self.retranslateUi(TestForm)
        if time < 10:
            self.timeresidueTextEdit.setText('0' + str(time) + ':00')
        else:
            self.timeresidueTextEdit.setText(str(time) + ':00')
        self.beginBtn.clicked.connect(self.startCount)
        self.beginBtn.clicked.connect(self.runtest)
        self.useranswerBtn.clicked.connect(self.getanswer)
        self.saveBtn.clicked.connect(self.save)
        QtCore.QMetaObject.connectSlotsByName(TestForm)

    def retranslateUi(self, TestForm):
        _translate = QtCore.QCoreApplication.translate
        TestForm.setWindowTitle(_translate("TestForm", "Calculator"))
        self.protesttLabel.setText(_translate("TestForm", "测试题目："))
        self.useranswerLabel.setText(_translate("TestForm", "请输入你的回答："))
        self.timeresidueLabel.setText(_translate("TestForm", "剩余时间："))
        self.answerLabel.setText(_translate("TestForm", "作答结果："))
        self.useranswerBtn.setText(_translate("TestForm", "提交答案"))
        self.saveBtn.setText(_translate("TestForm", "保存本次测试"))
        self.beginBtn.setText(_translate("TestForm", "开始答题"))

    def runtest(self):
        global time, test_data, message_flag0
        try:
            if message_flag0 == 1:
                self.test()
        except:
            pass

    # 对答题者进行测试
    def test(self):
        global test_data
        if self.testflag == 0:
            self.op_num = random.randint(1, 4)  # 随机生成的运算符个数
            self.pro_frac_num = random.randint(0, self.op_num)  # 随机生成的真分数个数
            self.int_num = self.op_num + 1 - self.pro_frac_num  # 生成整数个数
            self.op = produce_operators(self.op_num)  # 随机生成指定数量的运算符
            self.num = produce_numbers(self.int_num, self.pro_frac_num)  # 生成指定数量的随机整数和随机真分数
            self.problem = produce_problem(self.op_num, self.num, self.op)  # 生成题目
            self.result = calculate_result(self.problem)  # 计算题目正确结果
            self.show_problem = display_problem(self.problem)
            isrepetition(self.show_problem + '    ', 'test')
            self.protestEdit.append(self.show_problem)
            test_data = np.row_stack([test_data, record_test
            (self.show_problem, self.result, '该题未作答', '0')])

    def getanswer(self):
        global test_data, message_flag0
        try:
            if message_flag0 == 1:
                self.answer = str(self.useranswerLineEdit.text())
                self.judge_result = judge(self.answer, self.result)  # 判断答题者答案
                if self.judge_result == 0:
                    self.answerTextEdit.setText('回答错误，正确答案是%s' % (self.result))
                else:
                    self.answerTextEdit.setText('回答正确')
                if self.answer == '':
                    pass
                else:
                    if test_data.shape[0] == 1:
                        test_data[0,2] = str(self.answer) + '    '
                        test_data[0,3] = str(self.judge_result) + '    \n'
                    else:
                        test_data[-1][2] = str(self.answer) + '    '
                        test_data[-1][3] = str(self.judge_result) + '    \n'
            else:
                self.informationMessage1()
        except:
            if self.testflag == 0:
                self.answerTextEdit.setText('回答错误！')
            else:
                self.informationMessage()

    def informationMessage(self):
        MESSAGE = "请单击开始答题根据题目作答！"
        reply = QMessageBox.information(self,
                                        "输入失败", MESSAGE)

    def informationMessage1(self):
        MESSAGE = "测试时间到！"
        reply = QMessageBox.information(self,
                                        "输入失败", MESSAGE)

    def informationMessage2(self):
        MESSAGE = "文件已保存完毕！"
        reply = QMessageBox.information(self,
                                        "输入失败", MESSAGE)

    def informationMessage3(self):
        MESSAGE = "请先测试完毕！"
        reply = QMessageBox.information(self,
                                        "输入失败", MESSAGE)

    def informationMessage4(self):
        MESSAGE = "请提交最后一题的答案！"
        reply = QMessageBox.information(self,
                                        "输入失败", MESSAGE)

    def save(self):
        global username
        if self.testflag == -1:
            output_testdata('E:\ui_Calculator\userdata\%s'%(username + '_test_data.txt'),
                            control=0,accuracy=str(calculate_accuracy()))
            self.informationMessage2()
            self.testflag = 2
        elif self.testflag == 2:
            self.informationMessage2()
        else:
            if self.minute > 0 and self.second > 0:
                self.informationMessage3()

    def startCount(self):
        if self.testflag == 1:
            self.timer.start(1000)
            self.testflag = 0

    def showNum(self):
        global message_flag0
        if self.second > 0:
            self.second = self.second - 1
            if self.second > 10 and self.minute > 10:
                self.timeresidueTextEdit.setText('%d:' % (self.minute - 1) + '%d' % (self.second))
            elif self.minute < 10 and self.second >= 10:
                self.timeresidueTextEdit.setText('0' + '%d:' % (self.minute - 1) + '%d' % (self.second))
            elif self.minute >= 10 and self.second < 10:
                self.timeresidueTextEdit.setText('%d:' % (self.minute - 1) + '0' + '%d' % (self.second))
            else:
                self.timeresidueTextEdit.setText('0' + '%d:' % (self.minute - 1) + '0' + '%d' % (self.second))

        elif self.second == 0:
            if self.minute - 1 == 0 and self.testflag == 0:
                message_flag0 = 0
                self.testflag = -1
                self.protestEdit.append('\n\n\n测试时间到!')
                self.protestEdit.append('\n本次测试的正确率为：%s'%(str(calculate_accuracy())))
            elif self.minute - 1 > 0 and self.testflag == 0:
                self.minute = self.minute - 1
                self.second = 60

class Ui_ExaminationForm(QWidget):
    def __init__(self):
        super(Ui_ExaminationForm, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon \
        ('E:\ui_Calculator\myapp.ico'))
        self.timer = QTimer(self)
        self.second = 60
        self.examinationflag = 1
        self.examinationflag1 = 1
        self.examinationflag2 = 1
        self.temp = None
        self.minute = time
        self.timer.timeout.connect(self.showNum)

    def setupUi(self, ExaminationForm):
        global num
        ExaminationForm.setObjectName("ExaminationForm")
        ExaminationForm.resize(756, 333)
        self.proexaminationtLabel = QtWidgets.QLabel(ExaminationForm)
        self.proexaminationtLabel.setGeometry(QtCore.QRect(30, 20, 111, 16))
        self.proexaminationtLabel.setObjectName("proexaminationtLabel")
        self.proexaminationEdit = QtWidgets.QTextEdit(ExaminationForm)
        self.proexaminationEdit.setGeometry(QtCore.QRect(30, 40, 541, 201))
        self.proexaminationEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.proexaminationEdit.setObjectName("proexaminationEdit")
        self.useranswerLabel = QtWidgets.QLabel(ExaminationForm)
        self.useranswerLabel.setGeometry(QtCore.QRect(30, 260, 111, 16))
        self.useranswerLabel.setObjectName("useranswerLabel")
        self.useranswerLineEdit = QtWidgets.QLineEdit(ExaminationForm)
        self.useranswerLineEdit.setGeometry(QtCore.QRect(130, 260, 131, 20))
        self.useranswerLineEdit.setObjectName("useranswerLineEdit")
        self.timeresidueLabel = QtWidgets.QLabel(ExaminationForm)
        self.timeresidueLabel.setGeometry(QtCore.QRect(600, 20, 111, 16))
        self.timeresidueLabel.setObjectName("timeresidueLabel")
        self.scoreLabel = QtWidgets.QLabel(ExaminationForm)
        self.scoreLabel.setGeometry(QtCore.QRect(600, 130, 111, 16))
        self.scoreLabel.setObjectName("scoreLabel")
        self.answerTextEdit = QtWidgets.QTextEdit(ExaminationForm)
        self.answerTextEdit.setGeometry(QtCore.QRect(600, 150, 121, 171))
        self.answerTextEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.answerTextEdit.setObjectName("answerTextEdit")
        self.useranswerBtn = QtWidgets.QPushButton(ExaminationForm)
        self.useranswerBtn.setGeometry(QtCore.QRect(130, 290, 71, 23))
        self.useranswerBtn.setObjectName("useranswerBtn")
        self.proresidueLabel = QtWidgets.QLabel(ExaminationForm)
        self.proresidueLabel.setGeometry(QtCore.QRect(600, 70, 111, 16))
        self.proresidueLabel.setObjectName("proresidueLabel")
        self.saveBtn = QtWidgets.QPushButton(ExaminationForm)
        self.saveBtn.setGeometry(QtCore.QRect(210, 290, 91, 23))
        self.saveBtn.setObjectName("saveBtn")
        self.beginBtn = QtWidgets.QPushButton(ExaminationForm)
        self.beginBtn.setGeometry(QtCore.QRect(30, 290, 71, 23))
        self.beginBtn.setObjectName("beginBtn")
        self.timeresidueTextEdit = QtWidgets.QTextEdit(ExaminationForm)
        self.timeresidueTextEdit.setGeometry(QtCore.QRect(600, 40, 104, 24))
        self.timeresidueTextEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.timeresidueTextEdit.setObjectName("timeresidueTextEdit")
        self.proresidueLineEdit = QtWidgets.QTextEdit(ExaminationForm)
        self.proresidueLineEdit.setEnabled(True)
        self.proresidueLineEdit.setGeometry(QtCore.QRect(600, 90, 121, 24))
        self.proresidueLineEdit.setUndoRedoEnabled(True)
        self.proresidueLineEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.proresidueLineEdit.setObjectName("proresidueLineEdit")

        self.retranslateUi(ExaminationForm)
        self.beginBtn.clicked.connect(self.testexplanation)
        self.useranswerBtn.clicked.connect(self.getanswer)
        self.saveBtn.clicked.connect(self.save)
        if time < 10:
            self.timeresidueTextEdit.setText('0%s:00'%(str(time)))
        else:
            self.timeresidueTextEdit.setText('%s:00' % (str(time)))
        self.proresidueLineEdit.setText(str(num))
        QtCore.QMetaObject.connectSlotsByName(ExaminationForm)

    def retranslateUi(self, ExaminationForm):
        _translate = QtCore.QCoreApplication.translate
        ExaminationForm.setWindowTitle(_translate("ExaminationForm", "Calculator"))
        self.proexaminationtLabel.setText(_translate("ExaminationForm", "考试窗口："))
        self.useranswerLabel.setText(_translate("ExaminationForm", "请输入你的回答："))
        self.timeresidueLabel.setText(_translate("ExaminationForm", "剩余时间："))
        self.scoreLabel.setText(_translate("ExaminationForm", "提示栏："))
        self.useranswerBtn.setText(_translate("ExaminationForm", "提交"))
        self.proresidueLabel.setText(_translate("ExaminationForm", "剩余题目数量："))
        self.saveBtn.setText(_translate("ExaminationForm", "保存本次考试"))
        self.beginBtn.setText(_translate("ExaminationForm", "开始考试"))

    def getanswer(self):
        global examination_data, message_flag1
        if message_flag1 == 1:
            if self.examinationflag == 0:
                try:
                    self.answer = str(self.useranswerLineEdit.text().strip())
                    if self.answer == 'ok':
                        if self.examinationflag1 == 1:
                            for i in xrange(examination_data.shape[0]):
                                self.proexaminationEdit.append('(%d) ' % (i) + examination_data[i, 0]+'\n\n')
                            self.startCount()
                            self.examinationflag1 = 0
                        else:
                            self.answerTextEdit.setText('请开始作答！')
                    elif ':' in self.answer:
                        self.index = self.answer.find(':')
                        if self.temp != int(self.answer[:self.index]):
                            self.answerTextEdit.setText('(%d)题回答完毕' % (int(self.answer[:self.index])))
                            self.number = self.number - 1
                            self.proresidueLineEdit.setText(str(self.number))
                            examination_data[int(self.answer[:self.index]), 9] = str(judge(
                                examination_data[int(self.answer[:self.index]), 7].strip(),
                                self.answer[self.index + 1:].strip())) + '    \n'
                            self.temp = int(self.answer[:self.index])
                            examination_data[int(self.answer[:self.index]), 8] = self.answer[self.index + 1:].strip()\
                                                                                 + '    '
                        else:
                            self.answerTextEdit.setText('(%d)题回答完毕' % (int(self.answer[:self.index])))
                            examination_data[int(self.answer[:self.index]), 9] = str(judge(
                                examination_data[int(self.answer[:self.index]), 7].strip(),
                                self.answer[self.index + 1:].strip())) + '    \n'
                            examination_data[int(self.answer[:self.index]), 8] = self.answer[self.index + 1:].strip()\
                                                                                 + '    '
                    else:
                        self.answerTextEdit.setText('请输入正确的格式作答！')
                except:
                    self.answerTextEdit.setText('请输入正确的格式作答！')
            else:
                self.answerTextEdit.setText('请单击开始考试并根据题目作答！\n\n')
        else:
            self.proexaminationEdit.setText('考试时间到！')
            self.answerTextEdit.setText('考试时间到！')
            if str(self.useranswerLineEdit.text().strip()) == 'outputscore':
                a = self.calculate_score()

    def testexplanation(self):
        global examination_data, num, time
        if self.examinationflag == 1:
            self.proexaminationEdit.append('正在出题........\n\n')
            self.number = num
            while num > 0:
                try:
                    examination_data = np.row_stack([examination_data, self.record_examination()])
                    num = num - 1
                except:
                    pass
            self.proexaminationEdit.append('考试前，请仔细阅读本次考试说明，本次考试共有%d道题目，满分100分，'
                                           '能约分的题目必须约分，输入"题号:答案"来作答，比如第0题答案为67/34，'
                                           '要回答第0题，请输入"0:67/34"并单击提交按钮 (注意不用加双引号'
                                           '，冒号为英文字符)，准备完毕输入OK并单击提交开始答题。\n\n\n'%(self.number))
            self.examinationflag = 0

    # 产生考试试题并记录试题有关信息
    def record_examination(self):
        op_num = random.randint(1, 10)  # 随机生成的运算符个数
        pro_frac_num = random.randint(0, op_num)  # 随机生成的真分数个数
        int_num = op_num + 1 - pro_frac_num  # 生成整数个数
        op = produce_operators(op_num)  # 随机生成指定数量的运算符
        num = produce_numbers(int_num, pro_frac_num)  # 生成指定数量的随机整数和随机真分数
        problem = produce_problem(op_num, num, op)  # 生成题目
        result = calculate_result(problem)  # 计算题目正确结果
        show_problem = display_problem(problem)  # 打印题目
        isrepetition(show_problem, 'examination')
        add, sub, mul, div = 0, 0, 0, 0
        for i in problem:
            if i == '＋':
                add += 1
            elif i == '－':
                sub += 1
            elif i == '×':
                mul += 1
            elif i == '÷':
                div += 1
        result = Fraction(result)
        return np.array([str(show_problem) + '    ', str(add) + '    ', str(sub) + '    ', str(mul) + '    ',
                         str(div) + '    ', str(result.numerator) + '    ', str(result.denominator) + '    '
                            , str(result) + '    ', '该题未作答' + '    ', str(0) + '    \n'])

    # 计算套题中每题的分值
    def calculate_score(self):
        global examination_data, username
        self.answerTextEdit.setText('正在计算本次考试成绩......\n\n\n计算完毕！')
        score = np.zeros([examination_data.shape[0], 3])
        temp0 = examination_data[:, 1:5].astype('float')
        sum_temp0 = sum(sum(temp0))
        temp1 = np.log(abs(examination_data[:, 5:7].astype('float')) + 3)
        sum_temp1 = sum(sum(temp1))
        for i in xrange(examination_data.shape[0]):
            score[i, 0] = 50 * (1.0 * sum(temp0[i]) / sum_temp0)
            score[i, 1] = 50 * (1.0 * sum(temp1[i]) / sum_temp1)
            score[i, 2] = examination_data[i, 9]
        self.final_score = 0
        for i in xrange(score.shape[0]):
            self.proexaminationEdit.append('(%d) '%(i) + str(score[i, 0]+score[i, 1]) + '     ' + str(score[i,2]))
            if score[i, 2] == 1:
                self.final_score = self.final_score + score[i, 0] + score[i, 1]
        self.proexaminationEdit.append('\n\n')
        self.proexaminationEdit.append('%s,你的最终得分是： '%(username) + str(self.final_score))
        return self.final_score

    def save(self):
        global username, message_flag1
        if message_flag1 == 0:
            if self.examinationflag == -1:
                output_testdata('E:\ui_Calculator\userdata\%s'%(username + '_examination_data.txt'),
                                control=1, accuracy=str(self.calculate_score()))
                self.proexaminationEdit.setText('文件已保存完毕！')
                self.examinationflag = 2
            else:
                self.answerTextEdit.append('文件已保存完毕！')
        else:
            self.answerTextEdit.setText('请先完成作答！')

    def startCount(self):
        self.timer.start(1000)

    def showNum(self):
        global message_flag1
        if self.second > 0:
            self.second = self.second - 1
            if self.second > 10 and self.minute > 10:
                self.timeresidueTextEdit.setText('%d:' % (self.minute - 1) + '%d' % (self.second))
            elif self.minute < 10 and self.second >= 10:
                self.timeresidueTextEdit.setText('0' + '%d:' % (self.minute - 1) + '%d' % (self.second))
            elif self.minute >= 10 and self.second < 10:
                self.timeresidueTextEdit.setText('%d:' % (self.minute - 1) + '0' + '%d' % (self.second))
            else:
                self.timeresidueTextEdit.setText('0' + '%d:' % (self.minute - 1) + '0' + '%d' % (self.second))

        elif self.second == 0:
            if self.minute - 1 == 0:
                message_flag1 = 0
                self.examinationflag = -1
                if self.examinationflag2 == 1:
                    self.proexaminationEdit.setText('考试时间到！')
                    self.examinationflag2 = 0
            else:
                self.minute = self.minute - 1
                self.second = 60


examination_data = np.zeros([0, 10])
test_data = np.zeros([0, 4])  # 记录题目、正确答案、答题者答案、是否正确
message_flag0 = 1
message_flag1 = 1
num = 0
time = 0
username = ''
if __name__ == "__main__":
    App = QApplication(sys.argv)
    userloginForm = Ui_UserLoginForm()
    userloginForm.show()
    sys.exit(App.exec_())

