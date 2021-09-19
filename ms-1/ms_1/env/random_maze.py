from gym import Env
from gym.spaces import  Discrete
import numpy as np
import random
from scipy.stats import bernoulli
import yaml
# random.seed(3)
# np.random.seed(3)
from matplotlib import pyplot as plt
# left =0,up=1,right=2,down=3
class RandomMaze(Env):
    def __init__(self,params):
        # action space left =0,up=1,right=2,down=3
        self.action_space = Discrete(4)
        # state spaces are 3,7-terminal, 5 wall, rest all non terminal
        self.observation_space=Discrete(12)
        # initial state is 8
        self.startState=params["startState"]
        self.state=self.startState
        # prob of 0.8 of going in the desired action direction
        self.goInDirection=params["goInDirection"]
        self.goOrthogonal=(1-self.goInDirection)/2
        # it incurs a livingCost for every non terminal state
        self.livingCost=params["livingCost"]       
    
    def step(self,action):
        # stochasticity in the walk.
        # sample from uniform (0,1) distribution using random.random()
        random_num=np.random.random()
        if random_num<=self.goOrthogonal:
            action= (action-1)%4
        if random_num<=2*self.goOrthogonal and random_num>self.goOrthogonal:
            action = (action+1)%4
        if random_num > 2*self.goOrthogonal:
            pass
        # left action 0
        if action == 0 :
            if self.state!=0 and  self.state!=4 and self.state!=8 and self.state!=6:
                self.state-=1
            else:
                self.state=self.state
        # right action 2
        if action == 2 :
            if self.state!=4 and self.state!=11:
                self.state+=1
            else:
                self.state=self.state
        # up action =1
        if action == 1 :
            if self.state!=0 and self.state!=1 and self.state!=2 and self.state!=9:
                self.state-=4
            else:
                self.state=self.state
        # down action = 3
        if action == 3 :
            if self.state!=1 and self.state!=8 and self.state!=9  and self.state!=10 and self.state!=11:
                self.state+=4
            else:
                self.state=self.state
        
        if self.state==3:
            reward = 1
        elif self.state == 7:
            reward = -1
        else: 
            reward=-self.livingCost
        # check wether we reached a terminal state or not
        if self.state==3 or self.state==7:
            done = True
        else: 
            done = False
        # set placeholder for information
        info={}
        return self.state,reward,done,info
    
    def render(self):
        pass
    
    def currState(self):
        return self.state
    
    def reset(self):
        # reset state
        self.state=self.startState
        done=False
        return self.state,done
