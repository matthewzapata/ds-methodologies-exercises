import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, chi2_contingency
from sklearn.model_selection import train_test_split

# Write a function that will take, as input, a dataframe and a list containing the column names of 
# all ordered numeric variables. It will output, through subplots, a pairplot, a heatmap, and 1 other 
# type of plot that will loop through and plot each combination of numeric variables 
# (an x and a y, combination order doesn't matter here!).
def pair_heat_(df):
    plt.figure(figsize=(20,20))
    sns.pairplot(df)
    plt.show()

    plt.figure(figsize=(20,20))
    sns.heatmap(df.corr(), annot=True)
    
    plt.show()

# Write a function that will use seaborn's relplot to plot 2 numeric (ordered) variables and 1 categorical variable. 
# It will take, as input, a dataframe, column name indicated for each of the following: x, y, & hue.
def relplot_TwoNum_OneCat(df, x, y, hue):
    """Creates a sns.relplot with two ordered numeric variables and 1 categorical variable."""
    sns.relplot(data=df, x=x, y=y, hue=hue)


# Write a function that will take, as input, a dataframe, a categorical column name, and a list of numeric column names. 
# It will return a series of subplots: a swarmplot for each numeric column. X will be the categorical variable.
def swarm_subs(df, cat, list_of_num_columns):
    n = len(list_of_num_columns)
    for i, column in enumerate(list_of_num_columns):
        plt.figure(figsize=(15, 15))
        plt.subplot(n, 1, i+1)
        sns.swarmplot(data=df, x=cat, y=column)
        


# Write a function that will take a dataframe and a list of categorical columns to plot each combination of 
# variables in the chart type of your choice.
def cat_distributions(df, list_of_cat_columns, num_variable):
    for column in list_of_cat_columns:
        if len(df[column].unique()) > 6:
            binned_column = pd.cut(df[column], bins=5)
            sns.boxplot(data=df, x=num_variable, y=binned_column, orient='h')
            plt.show()
        else:
            sns.boxplot(data=df, x=num_variable, y=column, orient='h')
            plt.show()

# logerror is normally distributed, so it is a great opportunity to use the t-test to test for 
# significant differences in the logerror by creating sample groups based on various variables. 
# e.g. Is logerror significantly different for properties in Los Angeles County vs Orange County (or Ventura County)? 
# Is logerror significantly different for properties that are delinquent on their taxes vs those that are not? 
# Is logerror significantly different for properties built prior to 1960 than those built later than 2000?
def print_ttest_results(group_1, group_2, alpha=0.05):
    ttest = ttest_ind(group_1, group_2)
    print(f'The p-value is : {ttest[1]}')
    if ttest[1] < alpha:
        print('There is a significant difference.')
    else:
        print('Not significant.')




# Because there are many discrete variables, you can the use chi-squared test to test proportions. 
# If you split logerror into quartiles, you can expect the overall probability of falling into a single quartile to be 25%. 
# Now, add another variable, like bedrooms (and you can bin these if you want fewer distinct values) and 
# compare the probabilities of bedrooms with logerror quartiles. 
# See the example in the Classification_Project notebook we reviewed on how to implement chi-squared.
def print_chi_test_results(cat_1, cat_2, alpha=0.05):
    num_unique_1 = len(cat_1.unique())
    num_unique_2 = len(cat_2.unique())
    if num_unique_1 > 8:
        bins_1 = []
        for i in [0, .25, .50, .75, 1]:
            bins_1.append(cat_1.quantile(i))
        cat_1 = pd.cut(cat_1, bins_1, include_lowest=True)
        print(f'Category 1 was binned. Here are the bins {bins_1}')
    if num_unique_2 > 8:
        bins_2 = []
        for i in [0, .25, .50, .75, 1]:
            bins_2.append(cat_2.quantile(i))
        cat_2 = pd.cut(cat_2, bins_2, include_lowest=True)
        print(f'Category 2 was binned. Here are the bins {bins_2}')
    chi = chi2_contingency(pd.crosstab(cat_1, cat_2))
    print(f'The p-value is: {chi[1]}')
    if chi[1] < .05:
        print('There is a relationship between the variables.')
    else:
        print('The variables are independent.')



def split_it(df, training_size=.7, random=123, strat=None):
    """Train test split. Returns train_df and test_df."""
    train, test = train_test_split(df, train_size=training_size, random_state=random, stratify=strat)
    print('Parameters are df, train_size, random_state, and stratify')
    print('Returns train, test')
    return train, test