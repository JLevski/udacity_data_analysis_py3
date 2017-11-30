import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

titanic = pd.read_csv('titanic_data.csv')

relatives = titanic['SibSp'] + titanic['Parch']
titanic['relatives'] = relatives

pclass = titanic.groupby('Pclass')
survived_by_class = pclass.sum()['Survived'] / pclass.count()['Survived']

sib_spouse = titanic.groupby('SibSp')
survived_by_sibsp = (sib_spouse.sum()['Survived'] /
                     sib_spouse.count()['Survived'])

par_child = titanic.groupby('Parch')
survived_by_parch = par_child.sum()['Survived'] / par_child.count()['Survived']

relative = titanic.groupby('relatives')
survived_by_relat = relative.sum()['Survived'] / relative.count()['Survived']

age_groups = [0, 18, 40, 60, 150]
age_group_labels = ['0 - 18', '19 - 40', '41 - 60', '61+']
titanic['age_range'] = pd.cut(titanic['Age'], bins=age_groups,
                              labels=age_group_labels)
age_range = titanic.groupby('age_range')
survived_by_age = age_range.sum()['Survived'] / age_range.count()['Survived']

print('Survived by class: \n', survived_by_class)
print('Survived by sibling or spouse: \n', survived_by_sibsp)
print('Survived by parent or child: \n', survived_by_parch)
print('Survived by relative: \n', survived_by_relat)
print('Survived by age range: \n', survived_by_age)
# print('Survived by class: \n', survived_by_class)

# fig, axes = plt.subplots(nrows=3, ncols=3)
