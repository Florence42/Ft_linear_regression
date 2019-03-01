#!/usr/bin/python

import sys, csv, pickle, os.path
from math import *

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


def read_data(inputfile):
    print(inputfile)
    with open(inputfile,"r") as f:
        tmp = f.readline()
        tmp = tmp.replace('\n', '')
        b = tmp.split("=")
        beta0 = float(b[1])
        tmp = f.readline()
        tmp = tmp.replace('\n', '')
        b = tmp.split("=")
        beta1 = float(b[1])
        return beta0, beta1      

        
'''' print the graph'''
def print_graph(tab, beta1, beta0, x, y):
    import matplotlib.pyplot as plt
    plt.title("Pricing graph")
    a = []
    b = []
    i = 0
    n = len(tab)
    while i < n:
        a.append(tab[i][0])
        b.append(tab[i][1])
        i = i + 1
    plt.plot(a, b, "bo", label="csv data")   
       
    ''' plot the line for the machine learning '''
    ''' only 2 points '''
    a =[]
    a.append(tab[0][0])
    a.append(tab[n-1][0])
    b = []
    tmp = estimated_price(beta1, beta0, tab[0][0])
    b.append(tmp)
    tmp = estimated_price(beta1, beta0, tab[n-1][0])
    b.append(tmp)
    plt.plot(a, b, "r-.", label= "machine learning")
    plt.plot([x], [y], 'go')
    plt.xlabel('Mileage')    
    plt.ylabel('Price')
    plt.legend()  
    #plt.interactive(True)  
    plt.show()

def estimated_price(theta1, theta0, mileage):
    return(theta1 * mileage + theta0)

def treat_csv_file(inputfile ):
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
        return tab        
    
def predict_price(beta0 = 0., beta1 = 0.):
    bcheck = False
    if os.path.exists('data.save') :
        beta0, beta1 = read_data('data.save')
        tab = treat_csv_file('data.csv') 
        bcheck = True
    print( 'Press enter now to get a price .......')
    print( '__________________________________________________')
    n = 1
    while n != 0 :
        print ('Enter mileage to get the price, or 0 to quit :')
        n = int(input())
        if n == 0:
            print("See you soon...")
            sys.exit()
        else:
            price = int((n * beta1) + beta0)
            print( 'price         : =', price )
            if bcheck :
                print('\n')
                print("The graph will be displayed ...")
            print( '\n__________________________________________________')
            if bcheck :
                print_graph(tab, beta1, beta0, n , price )
                #plt.interactive(False)
            
   
def main(argv):
    try:
        print("\nPredict pricing  will start")
        print("\nLets' start the fun ....")	
        predict_price()	        
    except Exception:
        print ('An Error occurs ...!')
        sys.exit(2)
	
	

if __name__ == "__main__":
   main(sys.argv)
