import os
import sys
import time
import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QColor, QPalette, QBrush
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QGridLayout, \
    QListWidget, QMessageBox, QSpacerItem, QSizePolicy, QFrame
from PyQt5 import QtWidgets

TRESHOLD = 0.75


def read_dataset():
    '''
    Creates the data set in this way:
    a list of lists: every inner list is per one recipe:
    [the recipe name, the ingredients with amounts, directions, a list of ingredients]
    '''
    # there are 50000 recipes in the file
    f = open("RecipeNLG_dataset.csv", "r")
    l = f.readline()  # read the titles line
    ds = []
    for i in range(100000):
        l = f.readline()
        name = l.split(',')[1]
        ingredients_with_amounts = l.split('[')[1].split(']')[0]
        ingredients_with_amounts = ingredients_with_amounts.replace('\"', "").split(', ')
        directions = l.split('[')[2].split(']')[0].split('""')[1::2]
        # go to the ingredients list(the 6th column)
        ingredients_list = l.split("[")[3].replace('\"', "")
        ingredients_list = ingredients_list.split(']')[0].split(', ')  # .replace(']', "")
        # print(name)
        # print(ingredients_with_amounts)
        # print(directions)
        # print(ingredients_list)
        recipe = [name, ingredients_with_amounts, directions, ingredients_list]
        ds += [recipe]

    f.close()
    return ds


def find_recipes(user_ingredients, ds):
    suitable_recipes = []
    for recipe in ds:
        recipe_ingredients = recipe[3]
        # print(recipe_ingredients)
        exist_ings = []
        missing_ings = []
        for ing in recipe_ingredients:
            if ing in user_ingredients:
                exist_ings += [ing]
            else:
                missing_ings += [ing]
        # if 'water' in recipe_ingredients:
        #     exist_ings += ['water']
        recipe_ings_amount = len(recipe_ingredients)
        exist_ings_amount = len(exist_ings)
        ratio = exist_ings_amount / recipe_ings_amount
        # if it's bigger than TRESHOLD, add this recipe o the list
        if ratio > TRESHOLD:
            # for every suitable recipe, return a list with 5 items:
            # [the recipe name, ingredients with amounts, directions,
            # the list of exist ingredients, the list of missing ingredients]
            recipe_data = recipe[:-1]
            recipe_data += [exist_ings, missing_ings]
            suitable_recipes += [recipe_data]
    print(len(suitable_recipes))  # print the amount of suitable_recipes were found
    return suitable_recipes


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.window5 = None
        self.recipe_window = None
        self.window4 = None
        self.window3 = None
        self.camera = None
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Home Page")
        self.layout2 = QVBoxLayout()

        # enable autofill background
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

        # your existing code
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
        # create window 2
        self.window2 = QWidget()
        self.window2.setGeometry(100, 100, 800, 600)
        self.window2.setWindowTitle("Window 2")

        # set the background color to beige
        p = self.window2.palette()
        p.setColor(self.backgroundRole(), QColor("#964B00"))
        self.window2.setPalette(p)

        # Create a QPixmap with the image file
        pixmap = QPixmap("fond.jpg")

        # Create a QPalette and set the background role to the QPixmap
        p.setBrush(QPalette.Background, QBrush(pixmap))

        self.window2.setPalette(p)

        # description label
        description = QLabel("Please press SCAN to take pictures of your ingredients")
        description.setAlignment(Qt.AlignCenter)
        description.setFont(QFont("Times New Roman", 15, QFont.StyleItalic))
        description.setStyleSheet("color: white;")

        # create the scan button
        scan_button = QPushButton("SCAN")
        scan_button.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        scan_button.setFixedSize(300, 200)
        scan_button.setStyleSheet(
            "QPushButton { background-color: rgba(255, 255, 255, 255);font-family: Times New Roman;font-size: 50pt }")

        # create the continue button
        continue_button = QPushButton("Continue to Scan")
        continue_button.setStyleSheet(
            "QPushButton { background-color: rgba(255, 255, 255, 255);font-family: Times New Roman;font-size: 15pt }")
        try_again_button = QPushButton("Try Again")
        try_again_button.setStyleSheet(
            "QPushButton { background-color: rgba(255, 255, 255, 255);font-family: Times New Roman;font-size: 15pt }")

        # create the done button
        done_button = QPushButton("Done")
        done_button.setStyleSheet(
            "QPushButton { background-color: rgba(255, 255, 255, 255);font-family: Times New Roman;font-size: 15pt }")

        # create the bottom row layout
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(try_again_button)
        bottom_layout.addSpacerItem(QSpacerItem(10, 10))
        bottom_layout.addWidget(continue_button)
        bottom_layout.addSpacerItem(QSpacerItem(10, 10))
        bottom_layout.addWidget(done_button)

        # create the main layout
        main_layout = QGridLayout()
        main_layout.addWidget(scan_button, 0, 1, alignment=Qt.AlignCenter)
        main_layout.addLayout(bottom_layout, 1, 1)
        # add the done button to the main layout
        main_layout.addWidget(done_button, 1, 1, alignment=Qt.AlignCenter)
        # main_layout.addLayout(top_right_layout, 0, 0)
        main_layout.addWidget(description, 0, 1, alignment=Qt.AlignTop)

        self.window2.setLayout(main_layout)

        scan_button.clicked.connect(self.on_button_scan_clicked)
        done_button.clicked.connect(self.on_button_done_clicked)
        continue_button.clicked.connect(self.on_button_scan_clicked)
        try_again_button.clicked.connect(self.try_again_button_click)
        # close_button.clicked.connect(self.window2.close)

        self.window2.show()

    def try_again_button_click(self):
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
                self.camera.release()
                cv2.destroyAllWindows()
                break
        if countdown == 0:
            filename = os.path.join(self.path, f"captured_frame_{self.picture_counter}.jpg")
            cv2.imwrite(filename, frame)
            cv2.destroyAllWindows()

    def on_button_scan_clicked(self):
        self.picture_counter += 1
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
        products = ['milk', 'flour']  # all types of ingredients in our dataset
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

            # cv2.imshow('img2', imgOriginal)
            cv2.waitKey(1)

        print(ingredients)

        ##

        self.window3 = QWidget()
        self.window3.setGeometry(100, 100, 800, 600)
        self.window3.setWindowTitle("Window 3")
        # set the background color to beige
        p = self.window3.palette()
        p.setColor(self.backgroundRole(), QColor("#964B00"))
        # Create a QPixmap with the image file
        pixmap = QPixmap("fond3.jpg")

        # Create a QPalette and set the background role to the QPixmap
        p.setBrush(QPalette.Background, QBrush(pixmap))
        self.window3.setPalette(p)

        # # Create a QPixmap with the image file
        # pixmap = QPixmap("fond.jpeg")
        #
        # # Create a QPalette and set the background role to the QPixmap
        # p.setBrush(QPalette.Background, QBrush(pixmap))
        #
        # self.window3.setPalette(p)

        title1 = QLabel("Here is the list of your ingredients:")
        title1.setAlignment(Qt.AlignCenter)
        title1.setFont(QFont("Times New Roman", 25, QFont.Bold))
        title1.setStyleSheet("color: white;")
        str_ingredients = ', '.join(ingredients)
        title2 = QLabel(str_ingredients)
        title2.setAlignment(Qt.AlignCenter)
        title2.setFont(QFont("Times New Roman", 20))
        title2.setStyleSheet("color: white;")

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setLineWidth(1)
        frame.setMidLineWidth(1)
        frame.setStyleSheet("background-color: black;")

        # Create a layout for the frame
        frame_layout = QVBoxLayout()
        frame_layout.addWidget(title1)
        frame.setLayout(frame_layout)
        layout = QVBoxLayout()
        layout.addWidget(frame)
        layout.addWidget(title2)

        # Create the confirm button
        confirm_button = QPushButton("Confirm")
        confirm_button.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        confirm_button.setFixedSize(400, 100)
        confirm_button.setStyleSheet(
            "QPushButton { background-color: rgba(255, 255, 255, 255);font-family: Times New Roman;font-size: 15pt }")

        # create delete and ReScan button
        reScan_button = QPushButton("Delete & re-Scan")
        reScan_button.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        reScan_button.setFixedSize(400, 100)
        reScan_button.setStyleSheet(
            "QPushButton { background-color: rgba(255, 255, 255, 255);font-family: Times New Roman;font-size: 15pt }")

        # create the main layout
        main_layout = QGridLayout()
        main_layout.addWidget(title1, 0, 0, alignment=Qt.AlignTop)
        main_layout.addWidget(title2, 0, 0, alignment=Qt.AlignCenter)
        main_layout.addWidget(confirm_button, 1, 0, alignment=Qt.AlignLeft)
        main_layout.addWidget(reScan_button, 1, 1, alignment=Qt.AlignLeft)

        # confirm_button.clicked.connect(self.on_confirm_button_click)
        reScan_button.clicked.connect(self.on_button_Rescan_clicked)
        confirm_button.clicked.connect(lambda: self.on_confirm_button_click(ingredients))

        self.window3.setLayout(main_layout)
        self.window3.show()
        # self.on_confirm_button_click(ingredients)

    def on_confirm_button_click(self, ingredients):
        self.window4 = QWidget()
        self.window4.setGeometry(100, 100, 800, 600)
        self.window4.setWindowTitle("Window 4")

        # set the background color to beige
        p = self.window4.palette()
        p.setColor(self.backgroundRole(), QColor("#964B00"))
        self.window4.setPalette(p)

        # create the main layout
        main_layout = QGridLayout()

        title = QLabel("We propose you some of our delicious recipes:")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Times New Roman", 20, QFont.Bold))
        title.setStyleSheet("color: white;")

        # Recipe dataset
        ds = read_dataset()

        # Find recipes that can be made with the given ingredients
        matching_recipes = find_recipes(ingredients, ds)
        l = []
        print(matching_recipes)
        for r in matching_recipes:
            l.append(r[0])

        list_widget = QListWidget()
        list_widget.setGeometry(50, 50, 100, 100)
        list_widget.addItems(l)
        list_widget.setStyleSheet("color: black")
        list_widget.setFont(QFont("Times New Roman", 15, QFont.Bold))
        list_widget.setMinimumSize(600, 400)

        main_layout.setRowStretch(1, 1)
        main_layout.setColumnStretch(0, 1)

        main_layout.addWidget(title, 0, 0, alignment=Qt.AlignCenter)
        main_layout.addWidget(list_widget, 1, 0, alignment=Qt.AlignCenter)
        # connect the function to the itemClicked signal of the list_widget
        list_widget.itemClicked.connect(lambda item: self.open_recipe_window(item, matching_recipes))
        # list_widget.itemClicked.connect(self.open_recipe_window)

        self.window4.setLayout(main_layout)
        self.window4.show()

    def on_button_Rescan_clicked(self):
        folder = 'ImagesTrain'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        confirm = QMessageBox.question(self, 'Confirm',
                                       "Are you sure you want to Rescan?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.window3.hide()
            self.window2.show()

    def open_recipe_window(self, item, matching_recipes):
        self.window5 = QWidget()
        self.window5.setGeometry(100, 100, 800, 600)
        self.window5.setWindowTitle("Window 5")

        # set the background color to beige
        p = self.window5.palette()
        p.setColor(self.backgroundRole(), QColor("#964B00"))
        self.window5.setPalette(p)

        # create the main layout
        main_layout = QGridLayout()

        # Title - recipe name
        recipe_name = item.text()
        title = QLabel(recipe_name)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Times New Roman", 20, QFont.StyleItalic))
        title.setStyleSheet("color: white;")

        # DETAILS OF THE RECIPE
        recipe_details = ""
        for recipe in matching_recipes:
            if recipe[0] == recipe_name:
                recipe_details = recipe[1]
                recipe_details2 = recipe[2]
                recipe_details4 = recipe[4]

        list_widget = QListWidget()
        list_widget.setGeometry(50, 50, 100, 100)
        list_widget.addItems(['Ingredients with amounts:'] + recipe_details + ['\n'] + ['Directions:'] + recipe_details2
                             + ['\n'] + ['List of missing ingredients:'] + recipe_details4)
        list_widget.setStyleSheet("color: black")
        list_widget.setFont(QFont("Time New Roman", 12))
        list_widget.setMinimumSize(600, 400)

        # Set the font of the selected items to bold
        bold_font = QFont()
        bold_font.setBold(True)

        # Select the first item in the list widget - title 1
        list_widget.setCurrentRow(0)
        list_widget.item(0).setFont(bold_font)
        list_widget.item(0).setText(list_widget.item(0).text() + '\n')

        # Select Direction's title in the list widget
        list_widget.setCurrentItem(list_widget.findItems('Directions:', Qt.MatchExactly)[0])
        list_widget.currentItem().setFont(bold_font)
        list_widget.currentItem().setText(list_widget.currentItem().text() + '\n')

        # Select the third item in the list widget
        list_widget.setCurrentItem(list_widget.findItems('List of missing ingredients:', Qt.MatchExactly)[0])
        list_widget.currentItem().setFont(bold_font)
        list_widget.currentItem().setText(list_widget.currentItem().text() + '\n')

        main_layout.addWidget(title, 0, 0, alignment=Qt.AlignTop)
        main_layout.setSpacing(10)
        main_layout.addWidget(list_widget, 1, 0, alignment=Qt.AlignTop)

        self.window5.setLayout(main_layout)
        self.window5.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
