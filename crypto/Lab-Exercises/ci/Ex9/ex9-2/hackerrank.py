def gcd(x,y):
    if y==0: 
        return x
    return gcd(y,x%y)
    
x_white = int(input("Enter number of white balls in X: "))
x_black = int(input("Enter number of black balls in X: "))

y_white = int(input("Enter number of white balls in Y: "))
y_black = int(input("Enter number of black balls in Y: "))

# considering the transfer was white

y_white_new = y_white+1
prob1_num = y_black*5
prob1_den = (y_black+y_white_new)*9

#considering the transwer was black

y_black_new = y_black+1
prob2_num = y_black_new*4
prob2_den = (y_black_new+y_white)*9


tot_num = prob2_den * prob1_num + prob1_den*prob2_num
tot_den = prob1_den * prob2_den
g = gcd(tot_den,tot_num)
print(str(int(tot_num/g))+"/"+str(int(tot_den/g)))
