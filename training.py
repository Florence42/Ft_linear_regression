#!/usr/bin/python

import sys, csv, pickle
#from math import *

''' sort the list ascending order of price'''
def sort_liste(tab):
    imove = 1
    n = len(tab) -1
    while imove:
        imove = 0
        for i in range(0,n):
            if tab[i][0] > tab[i + 1][0]:
                tmpx = tab[i][0]
                tmpy = tab[i][1]
                tab[i][0] = tab[i + 1][0]
                tab[i][1] = tab[i + 1][1]
                tab[i + 1][0] = tmpx
                tab[i + 1][1] = tmpy
                imove = 1


''' save beta0 and beta1 for next use of pricing determination '''
def save_data(outputfile, beta0, beta1):
    with open(outputfile, "w") as f:
        tmp ="beta0=" + str(beta0) +"\nbeta1=" + str(beta1) + "\n"
        f.write(tmp)
        #f.readline   
        # https://docs.python.org/fr/3.6/tutorial/inputoutput.html 
        
'''' print the graph'''
def print_graph(tab, beta1, beta0, beta1_f, beta0_f):
    import matplotlib.pyplot as plt
    plt.title("Training graph")
    a = []
    b = []
    i = 0
    n = len(tab)
    while i < n:
        a.append(tab[i][0])
        b.append(tab[i][1])
        i = i + 1
    plt.plot(a, b, "bo", label="csv data")

    ''' plot the line for the linear regression '''
    ''' only 2 points '''
    c =[]
    c.append(tab[0][0])
    c.append(tab[n-1][0])
    b = []
    tmp = (tab[0][0] * beta1_f) + beta0_f
    b.append(tmp)
    tmp = (tab[n-1][0] * beta1_f) + beta0_f
    b.append(tmp)
    plt.plot(c, b, "g--", label= "linear regression")

    ''' plot for gradient descent '''
    b = []
    i = 0
    while i < n:
        tmp = (tab[i][0] * beta1) + beta0
        b.append(tmp)
        i = i + 1
    plt.plot(a, b, "r-.", label= "machine learning")
    plt.xlabel('Mileage')
    plt.ylabel('Price')
    plt.legend()  
    #plt.interactive(True)  
    plt.show()

''' classical linear regression '''
def make_regression(list_price, list_km):
    top = 0.
    bottom = 0.
    xm = 0.
    ym = 0.
    m = len(list_price)
    for i in range(0, m):
        xm = xm + int(list_km[i])
    xm = xm / m
    for i in range(0, m):
        ym = ym + int(list_price[i])
    ym = ym / m
    for i in range(0, m):
        top = top + (int(list_price[i]) - ym) * (int(list_km[i]) - xm)
        bottom = bottom + ((int(list_km[i]) - xm)**2) 
    beta1 = top / bottom
    beta0 = ym - (beta1 * xm)
    #print("-------------xm = ", xm)
    #print("-------------Ym = ", ym)
    return(beta1, beta0)

''' compute what is call the cost for the gradientdescent '''
def make_cost(list_price, list_km, beta1, beta0):
    cost = 0.
    m = len(list_price)
    for i in range(m) :
        cost = cost + ((beta1 * int(list_km[i])) +beta0 -int(list_price[i] ))**2
    cost = cost/(2 * m)
    #print ("cost ", cost)
    return cost

''' informations for the gap between the reality and the predict '''
def print_cost(tab, beta1, beta0):
    m = len(tab)
    print("\n Mileage -- Price -- Pred. -- Gap")
    for i in range (m):
        tmp = estimated_price(beta1, beta0, tab[i][0])
        gap = tab[i][1] - tmp
        print( "%8d"% (int(tab[i][0])), "--", "%5d"% tab[i][1], "--", "%5d"% (int(tmp)), "--", "%5d"% (int(gap))  )

def moyenne(tableau):
    m = 0.
    for x in tableau:
        m = m + x
    print("moy = ", m / len(tableau))
    return sum(tableau, 0.0) / len(tableau)

def variance(tableau):
    m = moyenne(tableau)
    return moyenne([(x-m)**2 for x in tableau])

def ecartype(tableau):
    return variance(tableau)**0.5
        
def determine_scaling_km(list_org):
    #we tansform list_km in float
    #we determine the standard deviation 
    list_new1 = list()
    for x in list_org:
        list_new1.append(float(x))
    #we determine the mean and the standard deviation
    mean = moyenne(list_new1)
    ectype = ecartype(list_new1) 
    #we scale the data
    list_new = list()
    for x in list_new1:
        list_new.append((x - mean) / ectype) 
    #print(list_new)      
    return  list_new, ectype, mean

def determine_scaling_price(list_org, scale, mean):
    #we tansform list_price in float
    #we divide by the scale
    list_new = list()
    for x in list_org:
        list_new.append(float(x) / scale )
    return  list_new


def estimated_price(theta1, theta0, mileage):
    return(theta1 * mileage + theta0)

''' gradient descent '''
def make_learning(list_price, list_km, beta1, beta0, iter = 0):
    deriv_beta0 = 0.
    deriv_beta1 = 0.
    #ilearn = 0.1
    ilearn = 0.1
    tmp = 0.
    m = len(list_price)        
    """ feature scaling """
    #list_kms, scale, mean = determine_scaling_km(list_km)
    #list_prices = determine_scaling_price(list_price, scale, mean)
    scale = int(list_km[0])
    list_kms = list()        
    list_prices = list()    
    for i in range(m):
       list_kms.append(float(float(list_km[i])/scale))
       list_prices.append(float(float(list_price[i])/scale))
    #print("ilear = ", ilearn)
    while (True):
        i = 0
        while i < m:
            tmp = estimated_price(beta1, beta0, list_kms[i]) - list_prices[i]
            deriv_beta0 = deriv_beta0 + tmp 
            deriv_beta1 = deriv_beta1 + (tmp * list_kms[i])
            i = i + 1
        
        deriv_beta0 = (deriv_beta0 * ilearn) / m
        deriv_beta1 = (deriv_beta1 * ilearn) / m
        #print("deriv_beta0", deriv_beta0)      
        #print("deriv_beta1", deriv_beta1)
        iter +=1
        
        if abs(deriv_beta0) < float(0.000000001) and abs(deriv_beta1) < float(0.000000001):       
            return (beta1, beta0 * scale, iter)
        #print("beta0", beta0)      
        #print("beta1", beta1)
        beta0 = beta0 - deriv_beta0
        beta1 = beta1 - deriv_beta1
        #cost = make_cost(list_price, list_km, beta1, beta0 * 1000)
        #print("cost ", cost)

def treat_csv_file(inputfile, outputfile):
    with open(inputfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)          
        list_km =  list()
        list_price = list()
        for row in reader:
            list_km.append(row['km'])
            list_price.append(row['price'])
        n = len(list_price)
        tab = [[0] * 2 for i in range(0, n)]
        for i in range (0, n):
            tab[i][0] = int(list_km[i])
            tab[i][1] = int(list_price[i])
        sort_liste(tab)
        print("\n Mileage -- Price")
        for i in range (0, n):
            print("%8d"% ( tab[i][0]), "--", tab[i][1])   

        """ classical linear regression """
        beta1_f, beta0_f = make_regression(list_price, list_km)
        print("\n Linear regression results :")
        print(" beta0_f = ", beta0_f)
        print(" beta1_f = ", beta1_f)
        cost_f = make_cost(list_price, list_km, beta1_f, beta0_f)
        print("  cost_f = ", cost_f)
        
        """ gradient descent """
        print("\nThe machine is learning, be patient please .....")
        beta1, beta0, iter = make_learning(list_price, list_km, beta1=0., beta0= 0., iter = 0)
        print("\nCool, here are the results....")
        print("\n Gradiant descent results : ")
        print(" beta0 = ", beta0)
        print(" beta1 = ", beta1)
        print("  iter = ", iter)
        cost = make_cost(list_price, list_km, beta1, beta0)
        print("  cost = ", cost)
        #print_cost1(list_price, list_km, beta1, beta0)
        print_cost(tab, beta1, beta0)
        save_data(outputfile, beta0, beta1)
        print("\n The graph will be displayed .....")
        print_graph(tab, beta1, beta0, beta1_f, beta0_f)
        print("\n Here  we goo, that's pretty cool")
        print("\n By now ...")

def usage():
	print("Error :")
	print("Usage : training input_file output_file")
	print("Exemple : training data.csv data.save")
	sys.exit()

def main(argv):
    #https://www.solumaths.com/fr/calculatrice-en-ligne/calculer/deriver 
    #https://mrmint.fr/gradient-descent-algorithm
    inputfile = ''
    outputfile = ''
    try:
        if len(sys.argv) != 3:
            usage()
        inputfile = sys.argv[1]
        outputfile = sys.argv[2]
        print("\nMachine learning will start with :")
        print("    the data in the file : ", inputfile)
        print("    the parameters computed will be saved in the file : ", outputfile)
        print("\nLets' start the fun ....")		
        treat_csv_file(inputfile, outputfile)
    except Exception:
        print ('An Error occurs ...!')
        sys.exit(2)
	
	

if __name__ == "__main__":
   main(sys.argv)
