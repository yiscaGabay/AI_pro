import os
import sys
import time
import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QGridLayout
from PyQt5 import QtWidgets


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Home Page")
        self.layout2 = QVBoxLayout()

        # enable auto fill background
        self.setAutoFillBackground(True)

        # set the background color to brown
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor("#964B00"))
        self.setPalette(p)

        # create the background image
        pixmap = QPixmap('background_gui.png')
        label = QLabel()
        label.setPixmap(pixmap)
        label.setScaledContents(True)

        # create the main vertical layout
        layout1 = QVBoxLayout()

        # add the background image to the main layout
        layout1.addWidget(label)

        title1 = QLabel("Click & Cook")
        title1.setStyleSheet("QLabel { font-size: 25pt ;font-family: Times New Roman}")
        title1.setAlignment(Qt.AlignCenter)
        layout1.addWidget(title1)

        title2 = QLabel("Welcome to our gui application!")
        font = QFont("Times New Roman", 25, italic=True)
        title2.setAlignment(Qt.AlignCenter)
        title2.setFont(font)
        layout1.addWidget(title2)

        button_start = QPushButton("START")
        button_start.setFixedSize(900, 50)
        button_start.setStyleSheet(
            "QPushButton { background-color: rgba(255, 255, 255, 255);font-family: Times New Roman;font-size: 15pt }")
        layout1.addWidget(button_start)

        # set the layout to the window
        self.setLayout(layout1)

        button_start.clicked.connect(self.on_button_start_clicked)
        self.window2 = None
        self.picture_counter = 0
        self.path = 'ImagesTrain'

    def on_button_start_clicked(self):
        self.window2 = QWidget()
        self.window2.setGeometry(100, 100, 800, 600)
        self.window2.setWindowTitle("Window 2")

        # set the background color to beige
        p = self.window2.palette()
        p.setColor(self.backgroundRole(), QColor("#964B00"))
        self.window2.setPalette(p)

        # create the scan button
        scan_button = QPushButton("SCAN")
        scan_button.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        scan_button.setFixedSize(300,200)
        scan_button.setStyleSheet("QPushButton { background-color: rgba(255, 255, 255, 255);font-family: Times New Roman;font-size: 50pt }")

        # create the continue button
        continue_button = QPushButton("Continue to Scan")
        continue_button.setStyleSheet(
            "QPushButton { background-color: rgba(255, 255, 255, 255);font-family: Times New Roman;font-size: 15pt }")
        try_again_button = QPushButton("Try Again")
        try_again_button.setStyleSheet(
            "QPushButton { background-color: rgba(255, 255, 255, 255);font-family: Times New Roman;font-size: 15pt }")

        # create the close button
        #close_button = QPushButton("Close")

        # create the bottom row layout
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(try_again_button)
        bottom_layout.addWidget(continue_button)

        # create the top-right corner layout
        top_right_layout = QVBoxLayout()
        #top_right_layout.addWidget(close_button)

        # create the done button
        done_button = QPushButton("Done")
        done_button.setStyleSheet(
            "QPushButton { background-color: rgba(255, 255, 255, 255);font-family: Times New Roman;font-size: 15pt }")



        # create the main layout
        main_layout = QGridLayout()
        main_layout.addWidget(scan_button, 0, 1, alignment=Qt.AlignCenter)
        main_layout.addLayout(bottom_layout, 1, 1)
        # add the done button to the main layout
        main_layout.addWidget(done_button, 1, 1, alignment=Qt.AlignCenter)
        #main_layout.addLayout(top_right_layout, 0, 0)

        self.window2.setLayout(main_layout)

        scan_button.clicked.connect(self.on_button_scan_clicked)
        done_button.clicked.connect(self.on_button_done_clicked)
        continue_button.clicked.connect(self.on_button_scan_clicked)
        #close_button.clicked.connect(self.window2.close)

        self.window2.show()




    def on_button_scan_clicked(self):
        self.picture_counter+=1
        self.camera = cv2.VideoCapture(0)
        ret, frame = self.camera.read()
        cv2.imshow("Preview", frame)
        countdown = 100
        while countdown > 0:
            print("Taking picture in: ", countdown)
            time.sleep(1)
            countdown -= 1
            ret, frame = self.camera.read()
            cv2.imshow("Preview", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                filename = os.path.join(self.path, f"captured_frame_{self.picture_counter}.jpg")
                cv2.imwrite(filename, frame)
                self.picture_counter += 1
                self.camera.release()
                cv2.destroyAllWindows()
                break
        if countdown == 0:
            filename = os.path.join(self.path, f"captured_frame_{self.picture_counter}.jpg")
            cv2.imwrite(filename, frame)
            self.picture_counter += 1
            cv2.destroyAllWindows()

    def on_button_done_clicked(self):
        import os
        import cv2

        paths = []  # list of all the paths contained in imagesQuery
        products = ['avocado', 'beans', 'butter', 'carrots', 'cheese', 'corn', 'couscous', 'cumin', 'eggplants', 'eggs',
                    'fish', 'flour', 'green salad', 'lemon juice', 'marakkof', 'mayonnaise', 'milk', 'mushrooms',
                    'muttard', 'oignon', 'oil', 'olive oil', 'paprika', 'pasta', 'peas', 'pepper', 'potatoes', 'rice',
                    'salt', 'sauces', 'shamenet', 'soup', 'suggar', 'tehina', 'tomatoes', 'tuna', 'vegetable peppers',
                    'vinegar', 'yogurt',
                    'zucchini']  # all types of ingredients in our dataset
        list_of_ingredients = ['avocado', 'beans', 'butter', 'carrots', 'cheese classic', 'cheese emental',
                               'cheese gooda', 'cheese noam', 'cheese shamenet', 'cheese white', 'corn', 'couscous',
                               'couscous middle', 'couscous middle bag', 'cumin', 'eggplant', 'eggs 12', 'fish salmon',
                               'fish tuna', 'fish white', 'flour', 'green salad', 'lemon juice', 'marakkof',
                               'marakkof green', 'mayonnaise', 'milk', 'milk bottle', 'mushrooms brown',
                               'mushrooms white', 'muttard', 'muttard dijon', 'muttard grains', 'oignon', 'oil',
                               'oil canola', 'oil sesame', 'olive oil', 'olive oil spray', 'paprika', 'pasta',
                               'pasta barilla', 'pasta barilla penne', 'pasta noodle', 'pasta osem', 'pasta spaghetti',
                               'pasta tortilla', 'peas', 'pepper', 'pepper bag', 'potatoes red', 'potatoes sweet',
                               'potatoes yellow', 'rice thai', 'salt', 'salt big', 'salt ram levi', 'sauce garlic',
                               'sauce thai', 'shamenet', 'soup oignon', 'suggar', 'suggar bag', 'suggar brown',
                               'tehina', 'tomatoes cherry', 'tuna', 'peppers', 'vinegar yahin', 'danona yogurt',
                               'milki yogurt', 'zucchini']  # all types of ingredients in our dataset
        for product in products:
            paths.append('ImagesQuery/' + product)
        print(paths)

        orb = cv2.ORB_create(nfeatures=1000)

        images = []
        classNames = []
        myList = []
        for path in paths:
            myList.append(os.listdir(path))
        print(myList)
        print('Total Classes Detected', len(myList))

        i = 0
        for path in myList:
            for cl in path:
                imgCur = cv2.imread(f'{paths[i]}/{cl}', 0)
                images.append(imgCur)
                classNames.append(os.path.splitext(cl)[0])
            i += 1
        print(classNames)

        def findDes(images):
            desList = []
            for img in images:
                kp, des = orb.detectAndCompute(img, None)
                desList.append(des)
            return desList

        def findID(img, desList, thres=6):
            kp2, des2 = orb.detectAndCompute(img, None)
            bf = cv2.BFMatcher()
            matchList = []
            finalVal = -1
            try:
                for des in desList:
                    matches = bf.knnMatch(des, des2, k=2)
                    good = []
                    for m, n in matches:
                        if m.distance < 0.75 * n.distance:
                            good.append([m])
                    matchList.append(len(good))

                print(matchList)

            except:
                pass
            if len(matchList) != 0:
                if max(matchList) > thres:
                    finalVal = matchList.index(max(matchList))

            return finalVal

        desList = findDes(images)
        print(len(desList))

        '''
        train images from slicing

        '''

        nb_images = 4
        path_slice = 'ImagesTrain'
        images_train = []
        classNames_train = []
        myList_train = []
        myList_train = os.listdir(path_slice)
        print(myList_train)
        print('Total Classes Detected', len(myList_train))

        for cl in myList_train:
            imgCur = cv2.imread(f'{path_slice}/{cl}', 0)
            images_train.append(imgCur)
            classNames_train.append(os.path.splitext(cl)[0])

        print(classNames_train)

        # List of ingredients
        ingredients = []

        for path in classNames_train:
            path_img2 = 'ImagesTrain/' + path + '.jpg'
            print(path_img2)
            img2 = cv2.imread(path_img2)
            imgOriginal = img2.copy()
            id = findID(img2, desList)
            if id != -1:
                cv2.putText(imgOriginal, classNames[id], (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (153, 75, 0), 1)
            if classNames[id] not in ingredients:
                ingredients.append(classNames[id])

            #cv2.imshow('img2', imgOriginal)
            cv2.waitKey(1)

        print(ingredients)

        def find_recipes(ingredients, recipe_data):
            # Initialize a list to store the matching recipes
            matching_recipes = []

            # Iterate over the recipes in the recipe dataset
            for recipe in recipe_data:
                # Initialize a flag to store whether all ingredients are present
                all_ingredients_present = True

                # Iterate over the ingredients in the recipe
                for recipe_ingredient in recipe['ingredients']:
                    # If the ingredient is not in the list of available ingredients, set the flag to False
                    if recipe_ingredient not in ingredients:
                        all_ingredients_present = False
                        break

                # If the flag is still True, the recipe can be made with the given ingredients, so append it to the list
                if all_ingredients_present:
                    matching_recipes.append(recipe)

            # Return the list of matching recipes
            return matching_recipes

        # Recipe dataset
        recipe_data = [
            {'name': 'Cake', 'ingredients': ['eggs', 'flour', 'sugar', 'milk']},
            {'name': 'Cookies', 'ingredients': ['eggs', 'flour', 'sugar']},
            {'name': 'Scrambled Eggs', 'ingredients': ['eggs', 'milk']},
            {'name': 'Omelette', 'ingredients': ['eggs', 'milk', 'cheese']},

        ]

        # Find recipes that can be made with the given ingredients
        matching_recipes = find_recipes(ingredients, recipe_data)

        # Print the names of the matching recipes
        for recipe in matching_recipes:
            print(recipe['name'])

        self.window3 = QWidget()
        self.window3.setGeometry(100, 100, 800, 600)
        self.window3.setWindowTitle("Window 3")
        # set the background color to beige
        p = self.window3.palette()
        p.setColor(self.backgroundRole(), QColor("#964B00"))
        self.window3.setPalette(p)


        title1 = QLabel("Here is the list of your ingredients:")
        title1.setAlignment(Qt.AlignCenter)
        title1.setFont(QFont("Times New Roman", 25, QFont.Bold))
        title1.setStyleSheet("color: white;")
        str_ingredients = ', '.join(ingredients)
        title2 = QLabel(str_ingredients)
        title2.setAlignment(Qt.AlignCenter)
        title2.setFont(QFont("Times New Roman", 15))
        title2.setStyleSheet("color: white;")

        # create the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(title1)
        main_layout.addWidget(title2)

        self.window3.setLayout(main_layout)
        self.window3.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

