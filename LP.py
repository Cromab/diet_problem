from pulp import *
import pandas as pd
import numpy as np

df = pd.read_excel("diet.xls").iloc[0:64,:]

#--- Populate quantitative values ---#
#Create Minimization Problem
prob = LpProblem("dietProblem", LpMinimize)

#Define variables
number_foods = 64
number_nutrients = 11
xs = [LpVariable(f"x{i}", 0) for i in range(number_foods)]

#Define Coefficients (notice these are row-wise lists, not columns)
a = {}
for i in range(len(df)):
    a[i] = df.iloc[i, 3:].to_list()

#Define Constants
cs = df['Price/ Serving'].to_list()
maxs = pd.read_excel("diet.xls", sheet_name="Intakes").loc[1, :].values.tolist()[1:]
mins = pd.read_excel("diet.xls", sheet_name="Intakes").loc[0, :].values.tolist()[1:]


#--- Populate LP for Basic Constraints ---#
#objective function
prob += lpSum(cs[i]*xs[i] for i in range(number_foods))

#constraints
for j in range(number_nutrients):
    prob += lpSum(a[i][j]*xs[i] for i in range(number_foods)) >= mins[j]
    prob += lpSum(a[i][j]*xs[i] for i in range(number_foods)) <= maxs[j]


#--- Additional Constraints ---#
#Binary selection variables
bs = [LpVariable(f"b{i}", cat="Binary") for i in range(number_foods)]

#Linking constraint (arbitrarily large serving size) and Minimum serving constraint
for i in range(number_foods):
    prob +=  xs[i] <= 10000 * bs[i] #Linking
    prob += xs[i] >= bs[i] #Min Serving

#Broccoli OR Celery constraint
prob += bs[0] + bs[2] <= 1

#Meat/Poultry/Fish/Eggs constraint
prob += bs[8]+bs[27]+bs[28]+bs[29]+bs[30]+bs[31]+bs[32]+bs[41]+bs[42]+bs[43]+bs[44]+bs[49]+bs[50]+bs[51]+bs[56]+bs[58]+bs[59]+bs[61]+bs[63] >= 3


#--- Solve LP ---#
#Check if optimal
status = prob.solve()
LpStatus[status]

#Show values
for i in xs:
    if value(i) > 0:
        print(i, value(i))
