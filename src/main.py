from experiments import Experiment

import matplotlib.pyplot as plt

import os

if __name__ == '__main__':
    # sample_sizes = [1e4, 5e4, 1e5, 5e5, 1e6, 5e6]
    # for size in sample_sizes:
    #     exp = Experiment("leagueoflegends", size, 75)
    #     model, losses, iterations = exp.regular_train()
    #     exp.predict(model, 1000, "s", True)

    #     plt.title("Losses for size " + str(size))

    #     plt.plot(iterations, losses)
    #     plt.xlabel("Iteration")
    #     plt.ylabel("Loss")
        
    #     if not os.path.exists("plots/" + str(size) + ".png"):
    #         plt.savefig("plots/" + str(size) + ".png")
    #     else:
    #         count = 1
    #         while os.path.exists("plots/" + str(size) + ".png"):
    #             count += 1
    #         plt.savefig("plots/" + str(size) + ".png")

    #     print("#"*80)
    #     print("FINAL LOSS FOR SIZE ", size, losses[len(losses)-1])
    #     print("#"*80)

    #     plt.clf()

    exp = Experiment("leagueoflegends", None, 90)
    model, losses, iterations = exp.regular_train(epochs=1)
    exp.predict(model, 1000, "s", True)

    plt.title("Losses for size " + str(None))

    plt.plot(iterations, losses)
    plt.xlabel("Iteration")
    plt.ylabel("Loss")

