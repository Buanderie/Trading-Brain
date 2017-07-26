Trading Brain is a framework example for implementing and testing trading strategies.
It is composed of mainly three components communicating through APIs:
- Brain
- Memory
- Agent

This library can be used to test agents with the Trading-Gym.

## Installation

Install packages in requirements.txt file

## Roll out your own `Agent`

To create your own agent, it must inherit from the `Agent` base class which can be found at 'tbrn/base/agent.py'. It consists of three basic methods that need to be overridden in order to implement your own logic:
- `act`: returns the action chosen by the agent.
- `observe`: returns a real value (can be the loss in the case of a `KerasAgent` for instance). This method is where the learning logic of the agent is located. Can be blank for dummy agents.
- `end`: any logic at the end of an episode.

## Examples

One example can be found in `examples/`

- Simple keras agent (`examples/keras_example.py`)
- Dueling Double DQN tensorflow agent (`examples/tf_example.py`)

Read more about this example at our [Trading Gym](https://github.com/Prediction-Machines/Trading-Gym)


*Copyright © 2017 RKR Epsilon UK Ltd. All rights reserved.*
