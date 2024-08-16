import pandas as pd
import scipy.stats as ss

"""                                          Making the data frame                                                    """
"""                               this area can be ommitted because most people use excell sheet                         """


number_of_column = int(input("Enter the number of column:"))
number_of_row = int(input("Enter the number of row:"))
alpha = int(input("Enter the alpha value in percentage:"))

row_name = {}
dyna_lis = []
stat_lis = []
stat_data = pd.DataFrame()

for i in range(0,number_of_column):
    stat_lis.append(f"X{i+1}")
dyna_lis.append(stat_lis)
stat_lis = []

for i in range (0,number_of_column):
    for j in range (0,number_of_row):
        stat_lis.append(int(input(f"Enter the {i,j} value :")))
    stat_lis.append(sum(stat_lis))
    dyna_lis.append(stat_lis)
    stat_lis = []

for i in range(0,number_of_column):
    stat_data.insert(i,dyna_lis[0][i],dyna_lis[i+1],True)

temp=0
for i in range (0,number_of_row+1):
    for j in range (0,number_of_column):
        temp+=stat_data.iat[i,j]    
    stat_lis.append(temp)
    temp = 0
stat_data.insert(number_of_column,"Total",stat_lis,True)
stat_lis = []

for i in range(0,number_of_row+1):
    if (i!=number_of_row):
        row_name[i] = f"Y{i+1}"
    else:
        row_name[i] = "Total"

for i in range(0,number_of_column):
    for j in range(0,number_of_row):
        stat_lis.append(stat_data.iat[j,i] ** 2)
    stat_lis.append(sum(stat_lis))
    stat_data.insert(i+number_of_column+1,f"X{i+1}^2",stat_lis,True)
    stat_lis= []

stat_data = stat_data.rename(index=row_name)
print(stat_data)

"""                                               Calculating on the data                                             """

T = stat_data.iat[number_of_row,number_of_column]
N = 0
TSS = 0
SSC = 0
SSE = 0

for i in range(0,number_of_column):
    for j in range(0,number_of_row):
        if stat_data.iat[j,i] != 0:
            N+=1 

correctionFactor = (T**2)/N

for i in range(0,number_of_column):
    TSS += stat_data.iat[number_of_row,i+number_of_column+1]
TSS -= correctionFactor

N1=0
for i in range(0,number_of_column):
    for j in range(0,number_of_row):
        if stat_data.iat[j,i] != 0:
            N1+=1
    SSC += (stat_data.iat[number_of_row,i]**2)/N1
    N1=0
SSC -= correctionFactor

SSE = TSS-SSC

"""                                                       ANOVA TABLE                                                  """

anova = pd.DataFrame({"SS":[SSC,SSE],"DF":[number_of_column-1,N-number_of_column]})
anova = anova.rename(index={0:"BC",1:"Error"})

div=[anova.iat[0,0]/anova.iat[0,1],anova.iat[1,0]/anova.iat[1,1]]
anova.insert(2,"MS",div,True)

tableNumerator = 0
tableDenominator = 0
f = []
if anova.iat[0,2] > anova.iat[1,2]:
    f.extend([anova.iat[0,2]/anova.iat[1,2],0])
    tableNumerator = anova.iat[0,1]
    tableDenominator = anova.iat[1,1]
else:
    f.extend([anova.iat[1,2]/anova.iat[0,2],0])
    tableNumerator = anova.iat[1,1]
    tableDenominator = anova.iat[0,1]

anova.insert(3,"calcf",f,True)
f=[ss.f.ppf(q=(1-(alpha/100)),dfn=tableDenominator,dfd=tableDenominator),0.0]
anova.insert(4,f"table f {alpha}%",f,True)

print(anova)
if anova.iat[0,3]>anova.iat[0,4]:
    print("There is significant difference between the sample")
else:
    print("There is no significant difference between the sample")