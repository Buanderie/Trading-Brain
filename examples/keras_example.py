"""
In this example we demonstrate how to implement a DQN agent and
train it to trade optimally on a periodic price signal.
Training time is short and results are unstable.
Do not hesitate to run several times and/or tweak parameters to get better results.
Inspired from https://github.com/keon/deep-q-learning
"""
#Needed to get paths set up for import tbrn
import os,sys
curfilePath = os.path.abspath(__file__)
curDir = os.path.abspath(os.path.join(curfilePath,os.pardir))
parentDir = os.path.abspath(os.path.join(curDir,os.pardir))
sys.path.insert(0,parentDir)
from tbrn.agents.keras.keras_agent import KerasAgent

if __name__=="__main__":
    from tgym.envs import SpreadTrading
    from tgym.gens.deterministic import WavySignal
    # Instantiating the environmnent
    generator = WavySignal(period_1=25, period_2=50, epsilon=-0.5)
    episodes = 100
    episode_length = 400
    trading_fee = .2
    time_fee = 0
    history_length = 2
    environment = SpreadTrading(spread_coefficients=[1],
                                data_generator=generator,
                                trading_fee=trading_fee,
                                time_fee=time_fee,
                                history_length=history_length,
                                episode_length=episode_length)
    state = environment.reset()
    # Instantiating the agent
    memory_size = 3000
    state_size = len(state)
    gamma = 0.96
    epsilon_min = 0.01
    batch_size = 64
    action_size = len(SpreadTrading._actions)
    train_interval = 10
    learning_rate = 0.0008
    agent = KerasAgent(state_size = state_size,
                     action_size = action_size,
                     memory_size = memory_size,
                     episodes = episodes,
                     episode_length = episode_length,
                     train_interval = train_interval,
                     gamma = gamma,
                     learning_rate = learning_rate,
                     batch_size=batch_size,
                     epsilon_min =epsilon_min)
    # Warming up the agent
    for _ in range(memory_size):
        action = agent.act(state)
        next_state, reward, done, _ = environment.step(action)
        agent.observe(state, action, reward, next_state, done, warming_up=True)
    # Training the agent
    for ep in range(episodes):
        state = environment.reset()
        rew=0
        for _ in range(episode_length):
            action = agent.act(state)
            next_state,reward,done,_ = environment.step(action)
            loss = agent.observe(state, action, reward, next_state, done)
            state = next_state
            rew+=reward
        print("Ep:"+str(ep)
            +"| rew:"+str(round(rew,2))
            +"| eps:"+str(round(agent.epsilon,2))
            +"| loss:"+str(round(loss,4)))
    # Running the agent
    done = False
    state = environment.reset()
    while not done:
        action = agent.act(state)
        state,_,done, info = environment.step(action)
        if 'status' in info and info['status'] == 'Closed plot':
            done = True
        else:
            environment.render()
