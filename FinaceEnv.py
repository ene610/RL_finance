
import gym
from gym import spaces
import numpy as np
from BtcHistoricalData import MarketData
from gym.spaces.discrete import Discrete

class CustomEnv(gym.Env):
    def __init__(self):
        self.pygame = MarketData()
        #self.action_space = Discrete(22) se azione definisce quanto investire e quanto vendere
        self.action_space = Discrete(3)
        #con molta probabilità qui tocca utilizzare Box
        #https://github.com/openai/gym/blob/master/gym/spaces/box.py
        # * Independent bound for each dimension::
        #>>> Box(low=np.array([-1.0, -2.0]), high=np.array([2.0, 4.0]), dtype=np.float32)

        self.observation_space = np.array((2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2)) #TODO : cambia

    def reset(self):
        self.pygame.reset()
        self.pygame = MarketData()
        obs = self.pygame.observe()
        return obs

    def observe(self):
        return self.pygame.observe()

    def step(self, action):
        self.pygame.action(action)
        obs = self.pygame.observe()
        reward = self.pygame.evaluete()
        done = self.pygame.is_done()

        return obs, reward, done, {}

    def render(self, mode='human'):
        self.pygame.view()