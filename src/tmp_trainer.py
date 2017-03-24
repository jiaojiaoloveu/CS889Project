import cv2
import sklearn as sk
from sklearn.datasets import fetch_olivetti_faces
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score, KFold
from scipy.stats import sem
from scipy.ndimage import zoom

class Trainer:
    def __init__(self):
        self.faces = fetch_olivetti_faces()
        self.clf = SVC(kernel = 'linear')
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.faces.data, self.faces.target, test_size = 0.25, random_state = 0)
        self.evaluate(self.X_train, self.y_train, 5)
        self.train(self.X_train, self.X_test, self.y_train, self.y_test)

    def evaluate(self, X, y, K):
        self.cv = KFold(len(y), K, shuffle = True, random_state = 0)
        scores = cross_val_score(self.clf, X, y, cv = self.cv)

    def train(self, X_train, X_test, y_train, y_test):
        self.clf.fit(X_train, y_train)
        print("Accuracy on training set:")
        print(self.clf.score(X_train, y_train))
        print("Accuracy on testing set:")
        print(self.clf.score(X_test, y_test))
        y_pred = self.clf.predict(X_test)
        size = len(y_pred)
        for i in range(0, size):
            print(str(y_pred[i]) + ' ' + str(y_test[i]))
    
    def predict(self, image, rec):
        if len(rec) == 0:
            return
        (x, y, w, h) = rec
        xoffset = 0.15 * w
        yoffset = 0.2 * h
        face = image[y + yoffset : y + h, x + xoffset : x - xoffset + w]
        (w, h) = face.shape
        new_face = zoom(face, (64. / w, 64. / h))
        new_face = new_face.astype('float32')
        new_face = new_face / float(new_face.max())
        cv2.imshow('new face', new_face)     
        y_pred = self.clf.predict([new_face.ravel()])
        print(y_pred[0])

