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
path_slice= 'ImagesTrain'
images_train = []
classNames_train = []
myList_train = []
myList_train=os.listdir(path_slice)
print(myList_train)
print('Total Classes Detected', len(myList_train))

for cl in myList_train:
    imgCur = cv2.imread(f'{path_slice}/{cl}', 0)
    images_train.append(imgCur)
    classNames_train.append(os.path.splitext(cl)[0])


print(classNames_train)


# List of ingredients
ingredients=[]

for path in classNames_train:
    path_img2 = 'ImagesTrain/' + path + '.jpeg'
    print(path_img2)
    img2 = cv2.imread(path_img2)
    imgOriginal = img2.copy()
    id = findID(img2, desList)
    if id != -1:
        cv2.putText(imgOriginal, classNames[id], (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (100, 145, 100), 1)
    if classNames[id] not in ingredients:
        ingredients.append(classNames[id])

    cv2.imshow('img2', imgOriginal)
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




