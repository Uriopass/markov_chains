import csv
from collections import defaultdict
import re
import random

random.seed(1)

v = csv.reader(open("all_drinks.csv", "r"))

cols = dict((a, b) for (b, a) in enumerate(next(v)))

cocktails = {}
doses = defaultdict(set)

parseRegexes = [
    (re.compile(r"^(\d+)\s?oz$"), lambda res: int(res.group(1)) * 3),
    (re.compile(r"^(\d+)\s?shot$"), lambda res: int(res.group(1)) * 4),
    (re.compile(r"^(\d+)\s?1/2\s?oz$"), lambda res: 1.5 + int(res.group(1)) * 3),
    (re.compile(r"1/2\s?oz$"), lambda res: 1.5),
    (re.compile(r"1\.5\s?oz$"), lambda res: 4.5),
    (re.compile(r"3/4\s?oz$"), lambda res: 2.25),
    (re.compile(r"1/4\s?oz$"), lambda res: 0.75),
    (re.compile(r"2/3\s?oz$"), lambda res: 2),
    (re.compile(r"1/3\s?oz$"), lambda res: 1),
    (re.compile(r"0\.75\s?oz$"), lambda res: 2.25),
    (re.compile(r"0\.5\s?oz$"), lambda res: 1.5),
    (re.compile(r"0\.25\s?oz$"), lambda res: 0.75),
]

def parseQty(dosage):
    for reg, f in parseRegexes:
        m = reg.match(dosage)
        if m:
            return f(m)
    return None

trads = {
        "tomato juice": "Jus de tomate",
        "lemon juice": "Jus de citron",
        "celery salt": "Sel de celeri",
        "lemon": "Citron",
        "ice": "Glaçons",
        "dark rum": "Rhum brun",
        "malibu rum": "Rhum Malibu",
        "151 proof rum": "Rhum ambré 151 Proof",
        "spiced rum": "Rhum épicé",
        "white rum": "Rhum blanc",
        "añejo rum": "Rhum Añejo",
        "port": "Porto",
        "cinnamon": "Cannelle",
        "pineapple": "Ananas",
        "irish cream": "Crème de whisky",
        "lemon-lime soda": "Soda citron-citron vert",
        "beer": "Bière",
        "light rum": "Rhum léger",
        "red wine": "Vin rouge",
        "white wine": "Vin blanc",
        "wine": "Vin",
        "sugar": "Sucre",
        "apricot": "Abricot",
        "rum": "Rhum",
        "coffee": "Café",
        "cream": "Crème",
        "carbonated water": "Eau pétillante",
        "club soda": "Eau pétillante",
        "soda water": "Eau pétillante",
        "lemon peel": "Zeste de citron",
        "salt": "Sel",
        "powdered sugar": "Sucre en poudre",
        "water": "Eau",
        "light cream": "Crème légère",
        "heavy cream": "Crème épaisse",
        "egg": "Oeuf",
        "egg yolk": "Jaune d'oeuf",
        "egg white": "Blanc d'oeuf",
        "cherry": "Cerise",
        "egg yolk": "Jaune d'oeuf",
        "orange juice": "Jus d'orange",
        "apple juice": "Jus de pomme",
        "fruit juice": "Jus de fruit",
        "lime juice cordial": "Jus de citron+citron vert+sucre",
        "cranberry juice": "Jus de cranberry",
        "grapefruit juice": "Jus de pamplemousse",
        "pineapple juice": "Jus d'ananas",
        "lime juice": "Jus de citron vert",
        "lime": "Citron vert",
        "orange peel": "Zeste d'orange",
        "nutmeg": "Noix de muscade",
        "mint": "Menthe",
}

data = []
for row in v:
    if row[cols["strAlcoholic"]] != "Alcoholic":
        continue
    
    ingredients = []
    for ingrIdx in range(1,14):
        ingr = row[cols["strIngredient"+str(ingrIdx)]].strip()
        if ingr == "":
            break
        dosage = row[cols["strMeasure"+str(ingrIdx)]].strip()
        if dosage != "":
            qty = parseQty(dosage)
            if qty is not None:
                dosage = str(qty) + " cl"
            doses[ingr].add(dosage)
        ingredients.append(trads.get(ingr.lower(), ingr))
    data.append(tuple(ingredients))
    #print(ingredients)

from gen_name import genword

for i,v in enumerate(genword(data, 2000, 1.5, noexisting=False)):
    #if not any("Rhum" in x or "rum" in x or "Rum" in x for x in v):
    #    continue
    print("# Cocktail #"+str(i))
    for ingr in v:
        #dose = ", ".join(sorted(doses[ingr], key=lambda x: list(reversed(x))))
        print(f"{ingr}")
    print()
