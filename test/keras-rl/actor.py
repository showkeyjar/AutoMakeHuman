#操作器
import keras

def create_actor_network(self, state_size, action_dim):
    print("Now we build the model")
    S = Input(shape=[state_size])
    h0 = Dense(HIDDEN1_UNITS, activation='relu')(S)
    h1 = Dense(HIDDEN2_UNITS, activation='relu')(h0)
    Steering = Dense(1, activation='tanh', init=lambda shape, name: normal(shape, scale=1e-4, name=name))(h1)
    Acceleration = Dense(1, activation='sigmoid', init=lambda shape, name: normal(shape, scale=1e-4, name=name))(h1)
    Brake = Dense(1, activation='sigmoid', init=lambda shape, name: normal(shape, scale=1e-4, name=name))(h1)
    V = merge([Steering, Acceleration, Brake], mode='concat')
    model = Model(input=S, output=V)
    print("We finished building the model")
    return model, model.trainable_weights, S

rl.agents.ddpg.DDPGAgent(nb_actions, actor, critic, critic_action_input, memory, gamma=0.99, batch_size=32, nb_steps_warmup_critic=1000, nb_steps_warmup_actor=1000, train_interval=1, memory_interval=1, delta_range=None, delta_clip=inf, random_process=None, custom_model_objects={}, target_model_update=0.001)