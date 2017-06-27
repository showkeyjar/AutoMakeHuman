#环境评估


def target_train(self):
    actor_weights = self.model.get_weights()
    actor_target_weights = self.target_model.get_weights()
    for i in xrange(len(actor_weights)):
        actor_target_weights[i] = self.TAU * actor_weights[i] + (1 - self.TAU) * actor_target_weights[i]
    self.target_model.set_weights(actor_target_weights)