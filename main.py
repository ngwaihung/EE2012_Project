import argparse
import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt

# Mathematical Expressions
p = lambda x,l: l * np.exp(l*(-x)) # Given exponential function
PDF = lambda x,l: l * np.exp(l*(-x)) # Derived PDF expression
CDF = lambda x,l: 1 - np.exp(l*(-x)) # Derived CDF expression
invCDF = lambda x,l: -1 * (np.log(1-x)/l) # Derived inverse transform expression

# Fetch N as a command-line argument
parser = argparse.ArgumentParser(description='Input parameters')
parser.add_argument("mVar",type=int,metavar='N',nargs='+',help='Number of random variables to generate')
parser.add_argument("t1",type=int,metavar='t1',nargs='+',help='T1')
parser.add_argument("t2",type=int,metavar='t2',nargs='+',help='T2')
parser.add_argument("t3",type=int,metavar='t3',nargs='+',help='T3')
args = parser.parse_args()

# Independent Variables
a = args.t1[0] * 1.0 # t = 3
b = args.t2[0] * 1.0 # t = 4
c = args.t3[0] * 1.0 # t = 5
N = args.mVar[0] # Number of random variables to generate

# Dependent Variables
lambda_a = float(1.0/a) # t = 3
lambda_b = float(1.0/b) # t = 4
lambda_c = float(1.0/c) # t = 5

# Get inverse transformation array
def getRandInv(la):
    uniRand = np.sort(np.random.uniform(0,1,N)) # Generates N number of random var from 0 to 1 in ascending order
    return invCDF(uniRand,la) # Returns the inverse transformed variables based on the derived inverse CDF function

# Get probability density array
def getPDF(mInv,la,lb,lc):
    return PDF(mInv,la), PDF(mInv,lb), PDF(mInv,lc)
    
# Get cumulative distribution array
def getCDF(mInv,la,lb,lc):
    return CDF(mInv,la), CDF(mInv,lb), CDF(mInv,lc)

# Get probability component lasts beyond 5 years
def getDurability(t,l):
    result = integrate.quad(lambda x: l * np.exp(l*(-x)), t, np.inf) # Returns a tuple of the integral and absolute error
    return result

# Plot PDF graph
def plotPDF(fig,mInv,pdfArr_a,pdfArr_b,pdfArr_c,nullArr):
    ax = fig.add_subplot(211)
    plt.ylabel('Probability')
    plt.xlabel('Random Variable')
    ax.plot(mInv,pdfArr_a)
    ax.plot(mInv,pdfArr_b)
    ax.plot(mInv,pdfArr_c)
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    # Show variables on x-axis
    line = ax.scatter(mInv,nullArr,s=80,facecolors='none',edgecolors='r')
    line.set_clip_on(False)
    ax.set_title('PDF',fontsize='medium')
    plt.legend(['t = ' + str(args.t1[0]),'t = ' + str(args.t2[0]),'t = ' + str(args.t3[0])], loc='upper right')
    return

# Plot CDF graph
def plotCDF(fig,mInv,cdfArr_a,cdfArr_b,cdfArr_c,nullArr):
    ax = fig.add_subplot(212)
    plt.ylabel('Probability')
    plt.xlabel('Random Variable')
    ax.plot(mInv,cdfArr_a)
    ax.plot(mInv,cdfArr_b)
    ax.plot(mInv,cdfArr_c)
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    # Show variables on x-axis
    line = ax.scatter(mInv,nullArr,s=80,facecolors='none',edgecolors='r')
    line.set_clip_on(False)
    ax.set_title('CDF',fontsize='medium')
    plt.legend(['t = ' + str(args.t1[0]),'t = ' + str(args.t2[0]),'t = ' + str(args.t3[0])], loc='lower right')
    return

def main():
    # Declare and initialize all arrays
    mInv = getRandInv((lambda_a+lambda_b+lambda_c)/3) # Take average of three lambdas
    pdfArr_a, pdfArr_b, pdfArr_c = getPDF(mInv,lambda_a,lambda_b,lambda_c)
    cdfArr_a, cdfArr_b, cdfArr_c = getCDF(mInv,lambda_a,lambda_b,lambda_c)
    nullArr = [0] * N # For plotting points on x-axis
    
    fig = plt.figure()
    fig.suptitle('Graphs of Probability Density Function and Cumulative Distribution Function')
    
    # PDF Plot
    plotPDF(fig,mInv,pdfArr_a,pdfArr_b,pdfArr_c,nullArr)
    
    # CDF Plot
    plotCDF(fig,mInv,cdfArr_a,cdfArr_b,cdfArr_c,nullArr)
    
    # Subplot adjustments
    plt.subplots_adjust(hspace=0.5, wspace=1.0)
    
    # Print probabilities of component lasting beyond 5 years for t = 3,4,5
    p_a, err_a = getDurability(5,lambda_a) # t = 3
    p_b, err_b = getDurability(5,lambda_b) # t = 4
    p_c, err_c = getDurability(5,lambda_c) # t = 5
    print "p(t=" + str(args.t1[0]) + ") =", p_a
    print "p(t=" + str(args.t2[0]) + ") =", p_b
    print "p(t=" + str(args.t3[0]) + ") =", p_c
    
    # Show plot
    plt.show()
    
    return
    
main()
