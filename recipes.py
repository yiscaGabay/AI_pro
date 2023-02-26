TRESHOLD = float(1)

def read_dataset():
    '''
    Creates the data set in this way:
    a list of lists: every inner list is per one recipe:
    [the recipe name, the ingredients with amounts, directions, a list of ingredients]
    '''
    # there are 959107 recipes in the file
    f = open("RecipeNLG_dataset.csv", "r")
    l = f.readline()  # read the titles line
    ds = []
    for i in range(50000):
        l = f.readline()
        name = l.split(',')[1]
        ingredients_with_amounts = l.split('[')[1].split(']')[0]
        ingredients_with_amounts = ingredients_with_amounts.replace('\"',"").split(', ')
        directions = l.split('[')[2].split(']')[0].split('""')[1::2]
        # go to the ingredients list(the 6th column)
        ingredients_list = l.split("[")[3].replace('\"',"")
        ingredients_list = ingredients_list.split(']')[0].split(', ')    #.replace(']', "")
        # print(name)
        # print(ingredients_with_amounts)
        # print(directions)
        # print(ingredients_list)
        recipe = [name, ingredients_with_amounts, directions, ingredients_list]
        ds += [recipe]

    f.close()
    return ds


def find_recipes(user_ingredients):
    ds = read_dataset()
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
        #if 'water' in recipe_ingredients:
            #exist_ings += ['water']
        recipe_ings_amount = len(recipe_ingredients)
        exist_ings_amount = len(exist_ings)
        ratio = float(exist_ings_amount/recipe_ings_amount)
        if recipe[0] == 'Oven Fried Chicken' and ratio >= TRESHOLD:
            print(recipe[3])
            print(exist_ings)
            print(missing_ings)
            print(ratio)
            print(TRESHOLD)
            print(ratio >= TRESHOLD)
            print(recipe[1], recipe[2])

        # if it's bigger than TRESHOLD, add this recipe o the list
        if ratio >= TRESHOLD:

            recipe_data = recipe[:-1]
            recipe_data += [exist_ings, missing_ings]
            suitable_recipes += [recipe_data]
            # for every suitable recipe, return a list with 5 items:
            # [the recipe name, ingredients with amounts, directions,
            # the list of exist ingredients, the list of missing ingredients]


    print(len(suitable_recipes))  # print the amount of suitable_recipes were found
    return suitable_recipes


ingredients = ['sugar', 'avocado', 'tomatoes', 'salt', 'pepper']  # an example
rec = find_recipes(ingredients)
# print the recipes names for checking
for r in rec:
    print(r)
