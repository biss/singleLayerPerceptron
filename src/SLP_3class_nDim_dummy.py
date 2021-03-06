__author__ = 'biswajeet'

""" class 1 vs class 2 vs class 3 distinguished by mean1, mean2 and mean3 respectively"""

import numpy as np
import sklearn.metrics as cma
import matplotlib.pyplot as plt


class SLP(object):
    def __init__(self):
        self.dim = 3
        self.eta = .1
        self.u_weights = np.zeros(shape=(3, self.dim + 1))
        self.mean1 = [0.0, 10.0, 5.0]  # class 1
        self.mean2 = [20.0, 5.0, -5.0]  # class 2
        self.mean3 = [-5.0, -5.0, -5.0]  # class 3

        self.cov1 = [[6.0, 3.0, 0.0],
                     [3.0, 3.0, 1.0],
                     [0.0, 1.0, 2.0]]  # diagonal covariance, points lie on x or y-axis
        self.cov2 = [[5.0, -10.0, 0.0],
                     [-10.0, 15.0, 3.0],
                     [0.0, 3.0, 4.0]]
        self.cov3 = [[8.0, 0.0, 1.0],
                     [0.0, 5.0, -1.0],
                     [1.0, -1.0, 6.0]]

        self.data_train = np.zeros(shape=(300, 5))
        self.test_data = np.zeros(shape=(150, 4))
        self.u_weights = np.array([[-1.0, 5.0, 3.0, 4.0], [-2.0, 4.0, 1.0, 1.0], [-4.0, 2.0, 1.0, 3.0]])
        self.l_weights = np.full((3, 4), 0.0)
        self.labels_test = np.zeros(shape=150)
        self.prediction = np.zeros(shape=150)

    """def show_plot(self):
        plt.plot(self.data_train[1], self.data_train[2], 'x', color = 'Green')
        plt.plot(x1, y1, 'x', color = 'Blue')
        y_range = eval(formula)
        plt.plot(x_range, y_range, color = 'Red')
        plt.axis('equal')
        plt.show()"""

    def generate_data(self):
        __doc__ = """ this is the generate method """

        x, y, z = np.random.multivariate_normal(self.mean1, self.cov1, 100).T
        x1, y1, z1 = np.random.multivariate_normal(self.mean2, self.cov2, 100).T
        x2, y2, z2 = np.random.multivariate_normal(self.mean3, self.cov3, 100).T

        x_data = np.concatenate((x, x1, x2), axis=0)
        y_data = np.concatenate((y, y1, y2), axis=0)
        z_data = np.concatenate((z, z1, z2), axis=0)

        label1 = np.ones(100)
        label2 = label1 + 1
        label3 = label2 + 1

        labels = np.concatenate((label1, label2, label3), axis=0)

        for i, x, y, z, l in zip(range(300), x_data, y_data, z_data, labels):
            self.data_train[i] = [1, x, y, z, l]

        #print self.data_train[:10]

    def generate_test_data(self):
        __doc__ = """generating test data"""

        x_test, y_test, z_test = np.random.multivariate_normal(self.mean1, self.cov1, 50).T
        x1_test, y1_test, z1_test = np.random.multivariate_normal(self.mean2, self.cov2, 50).T
        x2_test, y2_test, z2_test = np.random.multivariate_normal(self.mean2, self.cov2, 50).T

        x_data_test = np.concatenate((x_test, x1_test, x2_test), axis=0)
        y_data_test = np.concatenate((y_test, y1_test, y2_test), axis=0)
        z_data_test = np.concatenate((z_test, z1_test, z2_test), axis=0)

        label1_test = np.ones(50)
        label2_test = label1_test + 1
        label3_test = label2_test + 1

        self.labels_test = np.concatenate((label1_test, label2_test, label3_test), axis=0)
        # print label1_test.shape

        # preparing training and testing data sets
        for i, x, y, z in zip(range(150), x_data_test, y_data_test, z_data_test):
            self.test_data[i] = [1, x, y, z]


    def predict_model(self):

        t_pdt_1 = 0
        t_pdt_2 = 0
        t_pdt_3 = 0
        count = 0
        count_1 = 0
        count_2 = 0
        count_3 = 0
        count_0 = 0
        max = 0
        print self.test_data
        for i in self.test_data:
            t_pdt_1 = np.dot(i[:], np.transpose(self.u_weights[0]))
            t_pdt_2 = np.dot(i[:], np.transpose(self.u_weights[1]))
            t_pdt_3 = np.dot(i[:], np.transpose(self.u_weights[2]))

            #finding max
            if(t_pdt_1>=t_pdt_2 and t_pdt_1>=t_pdt_3):
                max = t_pdt_1
            if(t_pdt_2>=t_pdt_1 and t_pdt_2>=t_pdt_3):
                max = t_pdt_2
            if(t_pdt_3>=t_pdt_1 and t_pdt_3>=t_pdt_2):
                max = t_pdt_3

            if max == t_pdt_1:
                self.prediction[count] = 1
                count_1 += 1
            elif max ==t_pdt_2:
                self.prediction[count] = 2
                count_2 += 1
            elif max == t_pdt_3:
                self.prediction[count] = 3
                count_3 += 1
            else:
                self.prediction[count] = 0
                count_0 += 1
            count += 1
        prediction1 = np.ones(shape = 150)
        for i in range(50):
            prediction1[i] = 1
        for i in range(51,100):
            prediction1[i] = 2
        for i in range(101, 150):
            prediction1[i] = 3
        #print self.prediction
        cm = cma.confusion_matrix(self.labels_test, prediction1)
        print 'confusion matrix for the model is', cm
        #print 'counts are', count_1, count_2,count_3,count_0

    # preparing training and testing data sets
    def train_model(self, label):
        print 'for class : ', label
        pdt = 0
        count = 0
        #self.l_weights = np.full((3, 4), 0.0)
        print 'l_weights are', self.l_weights[label - 1]
        print 'u_weights are', self.u_weights[label - 1]
        # class label >= 0 vs class non-label < 0 - online learning
        while (abs(self.l_weights[label - 1] - self.u_weights[label - 1]).any() > .0001):
            count += 1
            self.l_weights[label - 1] = self.u_weights[label - 1]

            # show_plot(formula, x_range)
            print 'training data and weight vector and pdt is :', self.data_train[0][:-1], self.u_weights[label - 1]\
                , np.dot(self.data_train[0][:-1], np.transpose(self.u_weights[label - 1]))

            for i in self.data_train:
                # print (u_weights, i[:-1])
                pdt = np.dot(i[:-1], np.transpose(self.u_weights[label - 1]))
                print 'class and product is ',i[-1], pdt
                if (i[-1] != label and pdt >= 0):
                    print 'printing weights and n*x before',(self.u_weights[label-1], self.eta*i[:-1])
                    self.u_weights[label - 1] = self.u_weights[label - 1] - self.eta * i[:-1]
                    print 'printing weights and n*x',(self.u_weights[label-1], self.eta*i[:-1])

                if (i[-1] == label and pdt < 0):
                    print 'weights and n*x before',(self.u_weights[label-1], self.eta*i[:-1])
                    self.u_weights[label - 1] = self.u_weights[label - 1] + self.eta * i[:-1]
                    print 'weights and n*x',(self.u_weights[label-1], self.eta*i[:-1])
            print 'abs diff ', abs(self.l_weights[label - 1] - self.u_weights[label - 1])
        print count


obj = SLP()
obj.generate_data()
#print obj.data_train
obj.train_model(1.0)
obj.train_model(2.0)
obj.train_model(3.0)

obj.generate_test_data()
print 'here are the 3 weight vectors', obj.u_weights

obj.predict_model()
