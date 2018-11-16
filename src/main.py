from experiments import Experiment

import matplotlib.pyplot as plt

if __name__ == '__main__':
    exp = Experiment("leagueoflegends", 1e4, 75)
    model, losses, iterations = exp.regular_train()
    exp.predict(model, 1000, "s", True)

    plt.plot(iterations, losses)
    plt.xlabel("Iteration")
    plt.ylabel("Loss")
    plt.show()
    plt.savefig("plot.png")
