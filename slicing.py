import image_slicer
import os
import cv2

paths = []  # list of all the paths contained in imagesQuery
products = ['avocado','beans','butter','carrots','cheese', 'corn','couscous','cumin','eggplants','eggs','fish','flour','green salad','lemon juice','marakkof','mayonnaise', 'milk', 'mushrooms','muttard','oignon','oil','olive oil','paprika','pasta', 'peas','pepper', 'potatoes', 'rice','salt', 'sauces','shamenet','soup','suggar','tehina','tomatoes', 'tuna','vegetable peppers','vinegar','yogurt',
            'zucchini']  # all types of ingredients in our dataset
list_of_ingredients = ['avocado','beans','butter','carrots','cheese classic','cheese emental','cheese gooda','cheese noam','cheese shamenet','cheese white', 'corn','couscous','couscous middle','couscous middle bag','cumin','eggplant','eggs 12','fish salmon','fish tuna','fish white','flour','green salad','lemon juice','marakkof','marakkof green','mayonnaise', 'milk','milk bottle', 'mushrooms brown','mushrooms white','muttard','muttard dijon','muttard grains','oignon','oil','oil canola', 'oil sesame','olive oil','olive oil spray','paprika','pasta','pasta barilla','pasta barilla penne','pasta noodle','pasta osem','pasta spaghetti','pasta tortilla', 'peas','pepper', 'pepper bag','potatoes red','potatoes sweet','potatoes yellow', 'rice thai','salt','salt big','salt ram levi', 'sauce garlic','sauce thai','shamenet','soup oignon','suggar','suggar bag','suggar brown','tehina','tomatoes cherry', 'tuna','peppers','vinegar yahin','danona yogurt',
            'milki yogurt','zucchini']  # all types of ingredients in our dataset
for product in products:
    paths.append('ImagesQuery/' + product)
print(paths)

nb_images = 4
path_slice='SliceTest'
image_slicer.slice('SliceTest\slice_image_4µ.jpeg',nb_images)
orb = cv2.ORB_create(nfeatures=1000)

images_train = []
classNames_train = []
myList_train = []
myList_train=os.listdir(path_slice)
print(myList_train)
print('Total Classes Detected', len(myList_train))

for cl in myList_train[1:]:
    imgCur = cv2.imread(f'{path_slice}/{cl}', 0)
    images_train.append(imgCur)
    classNames_train.append(os.path.splitext(cl)[0])


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


def findDes(images):
    desList = []
    for img in images:
        kp, des = orb.detectAndCompute(img, None)
        desList.append(des)
    return desList

desList = findDes(images)
print(len(desList))

print(classNames_train)
path=path_slice+'/'+classNames_train[0]+'.png'
print(path)
#img2 = cv2.imread('SliceTest/slice_image_4µ.jpeg')
while True:
    img2 = cv2.imread('ImagesTrain/salt_train.jpeg')
    img = img2.copy()
    id = findID(img2, desList)
    if id != -1:
        cv2.putText(img, classNames[id], (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (100, 145, 100), 1)
    cv2.imshow('img2', img)
    cv2.waitKey(1)
