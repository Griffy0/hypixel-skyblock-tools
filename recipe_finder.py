import requests
import json
recipes = requests.get('https://raw.githubusercontent.com/kr45732/skyblock-plus-data/main/InternalNameMappings.json').json()

def get_recipe(to_craft, amount, subtract):
    #print(to_craft, amount)
    list_of_mats = {}
    #if 'recipe' in recipes[to_craft].keys():
        #print(to_craft, 'in keys')

    for recipe in recipes[to_craft]['recipe'].keys():
        #print(recipes[to_craft]['recipe'])
        if recipes[to_craft]['recipe'][recipe]:
            ingredient = recipes[to_craft]['recipe'][recipe].split(':')
            ingredient[1] = int(ingredient[1])
            if ingredient[0] in list_of_mats.keys():
                list_of_mats[ingredient[0]][1] += ingredient[1] * amount
            else:
                list_of_mats[ingredient[0]] = [ingredient[0], ingredient[1] * amount]
    for i in list_of_mats.keys():
        if i in recipes.keys():
            if 'recipe' in recipes[i].keys():
                list_of_mats[i] = get_recipe(i, list_of_mats[i][1], subtract)
    return list_of_mats

def extract_array(obj):
    if type(obj) is dict:
        for value in obj.values():
            yield from extract_array(value)
    elif type(obj) in {list, tuple}:
        yield obj


def recipe_wrapper(to_craft, amount, subtract):
    recipe_dict = get_recipe(to_craft, amount, subtract)
    reconstructed = []
    for i in recipe_dict:
        reconstructed.extend(list(extract_array(recipe_dict[i])))
    return reconstructed

def format_item_name(name):
    name = name.replace('_', ' ')
    name = name.lower()
    name = name.title()
    return name

def format_recipe(to_craft, amount, subtract=''):
    if not to_craft in recipes.keys():
        print(f'{format_item_name(to_craft)} has no recipe')
        return [[to_craft, amount]]
    reconstructed = recipe_wrapper(to_craft, amount, subtract)
    for i in reconstructed:
        if i[0] in text_replacements.keys():
            i[0] = text_replacements[i[0]]

    for i in reconstructed:
        if 'ENCHANTED_'+i[0] in recipes:
            conv_int = recipe_wrapper('ENCHANTED_'+i[0], i[1], subtract)[0][1]
            i[0] = 'ENCHANTED_'+i[0]
            i[1] = i[1] / (conv_int / i[1])
            i[1] = round(i[1])

    for i in reconstructed:
        i[0] = format_item_name(i[0])

    return reconstructed

def print_recipe(arr):
    for i in arr:
        print(str(i[0]) + ': ' + str(i[1]))


#https://github.com/maxbachmann/Levenshtein
to_craft = ''
while to_craft == '':
    to_craft = input('what do you want to craft?\n')
print('\n')
to_craft = to_craft.upper()
subtract_craft = ''
if '-' in to_craft:
    to_craft = to_craft.split('-')
    to_craft[0] = to_craft[0].rstrip()
    to_craft[1] = to_craft[1].lstrip()
    subtract_craft = to_craft[1]
    to_craft = to_craft[0]
to_craft = to_craft.replace(' ', '_')



print(to_craft, subtract_craft)

text_replacements = {
    'INK_SACK-4': 'LAPIS_LAZULI',
}

print(recipes['GOLDEN_PLATE'])
#print_recipe(format_recipe(to_craft, 1))
