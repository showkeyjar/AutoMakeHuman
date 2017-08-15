#评价器

def create_critic_network(self, state_size, action_dim):
    print("Now we build the model")
    S = Input(shape=[state_size])
    A = Input(shape=[action_dim], name='action2')
    w1 = Dense(HIDDEN1_UNITS, activation='relu')(S)
    a1 = Dense(HIDDEN2_UNITS, activation='linear')(A)
    h1 = Dense(HIDDEN2_UNITS, activation='linear')(w1)
    h2 = merge([h1, a1], mode='sum')
    h3 = Dense(HIDDEN2_UNITS, activation='relu')(h2)
    V = Dense(action_dim, activation='linear')(h3)
    model = Model(input=[S, A], output=V)
    adam = Adam(lr=self.LEARNING_RATE)
    model.compile(loss='mse', optimizer=adam)
    print("We finished building the model")
    return model, A, S