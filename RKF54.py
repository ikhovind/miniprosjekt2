  #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 20:26:05 2018

@author: rivertz
"""

import numpy as np
import math as m 
import sys

class RungeKuttaFehlberg54:
    A=np.array(
        [[   0     ,    0     ,    0      ,    0     ,  0   ,0],
         [   1/4   ,    0     ,    0      ,    0     ,  0   ,0],
         [   3/32  ,    9/32  ,    0      ,    0     ,  0   ,0],
         [1932/2197,-7200/2197, 7296/2197 ,    0     ,  0   ,0],
         [ 439/216 ,   -8     , 3680/513  , -845/4104,  0   ,0],
         [  -8/27  ,    2     ,-3544/2565 , 1859/4104,-11/40,0]])
  
    B=np.array(
        [[  25/216 ,    0     , 1408/2565 , 2197/4104 ,-1/5 ,0],
         [  16/135 ,    0     , 6656/12825,28561/56430,-9/50,2/55]]);

    def __init__(self,
                 function,
                 dimension,
                 stepsize,
                 tolerance):
        '''Synopsis:
        function: right hand side of an autonomous equation.
                  The function takes a numpy array as input
                  Important time must always be Y[0].
                  When res=function(y), then res[0]=1
                  allways.

        dimension:number of equations and unknown functions included the time.

        stepsize: Initial stepsize

        tolerance: Tolerance of the method
                
        '''
        self.F=function;
        self.dim=dimension;
        self.h=stepsize;
        self.tol=tolerance;
    
    def step(self,
             Win):
        ''' Do one step of the method with the current stepsize'''
        s=np.zeros((6,self.dim))
        
        for i in range(0,6):
            s[i,:]=self.F(Win+self.h*self.A[i,0:i].dot(s[0:i,:]))

        Zout=Win+self.h*(self.B[0,:].dot(s));
        Wout=Win+self.h*(self.B[1,:].dot(s));
        
        E=np.linalg.norm(Wout-Zout,2)/np.linalg.norm(Wout,2);
        
        return Wout, E

    def safeStep(self,
                 Win,
                 max_t=m.inf):
        ''' Do one step of the method with adapted stepsize
        If max_t is set to a finite value of t.
        '''

        if ((self.h+Win[0])>max_t):
            self.h=max_t-Win[0];
        Wout,E = self.step(Win);
        # Check if the error is tolerable
        if(not self.isErrorTolerated(E)):
            #Try to adjust the optimal step length
            self.adjustStep(E);
            Wout,E = self.step(Win);
        # If the error is still not tolerable
        counter=0;
        while(not self.isErrorTolerated(E)):
            #Try if dividing the steplength with 2 helps. 
            self.divideStepByTwo();
            Wout,E = self.step(Win);
            counter = counter + 1;
            if(counter>10):
                sys.exit(-1);
            
        self.adjustStep(E);
        
        return Wout, E

    def isErrorTolerated(self,E):
        return E<self.tol;

    def adjustStep(self,E):
        if(E==0):
            s=2;
        else:
            s=m.pow(self.tol*self.h/(2*E),0.25);
        self.h = s * self.h;

    def divideStepByTwo(self):
        self.h=self.h/2;
        
    def setStepLength(self,stepLength):
        self.h=stepLength;        
        
