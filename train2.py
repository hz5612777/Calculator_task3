import matplotlib.pyplot as plt
import numpy as np
import math
import v


filename = 'xunlianmuban.txt'
train_linx = []
train_liny = []
x_tmp = []
y_tmp = []
with open(filename, 'r') as file_to_read:
    while True:
        lines = file_to_read.readline()
        if not lines:
            break
        _, _, _, _, _, x_tmp, y_tmp,_= [str(i) for i in lines.split('||')]
        train_linx.append(x_tmp)
        train_liny.append(y_tmp)

train_linx = np.asarray(train_linx)
train_liny = np.asarray(train_liny)
train_linx = train_linx.reshape(-1,1)
train_liny = train_liny.reshape(-1,1)
train_linx = train_linx.astype('float64')
train_liny = train_liny.astype('float64')

train_linx1 = train_linx
a = int(100*max(train_linx))
steps = [i / 100.0 for i in range(a)]
steps = np.asmatrix(steps)

train_liny = train_liny.astype('float')

m = train_linx.shape[0]
n = 5
lamda = 5


def pow_matrix(x, n):
    q = np.zeros([1, 0])
    for i in range(n + 1):
        q = np.column_stack((q, math.pow(x, i)))
    return q


def pow_train_linx(train_linx, n):
    p = np.zeros([0, n + 1])
    for data in train_linx:
        p = np.row_stack((p, pow_matrix(data, n)))
    return p

train_linx = pow_train_linx(train_linx, n)

def E(n):
    a = np.ones([1, n + 1])
    a = np.diag(a[0])
    a[0, 0] = 0
    return a

theta = np.asmatrix(np.dot(train_linx.T, train_linx) + lamda * E(n)).I * train_linx.T * train_liny

# number = [7.2]
# print np.dot(pow_train_linx(number,n),theta)
#
# steps1 = pow_train_linx(steps.T, n)
# plt.plot(train_linx1, train_liny, '.')
# plt.plot(steps.T, np.dot(steps1, theta))
# plt.show()

