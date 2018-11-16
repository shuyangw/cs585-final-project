from experiments import Experiment

import matplotlib.pyplot as plt

import os

if __name__ == '__main__':
    sample_sizes = [1e4, 5e4, 1e5, 5e5, 1e6, 6e6]
    for size in sample_sizes:
        exp = Experiment("leagueoflegends", size, 75)
        model, losses, iterations = exp.regular_train()
        exp.predict(model, 1000, "s", True)
        

        plt.title("Losses for size" + str(size))

        plt.plot(iterations, losses)
        plt.xlabel("Iteration")
        plt.ylabel("Loss")
        
        if not os.path.exists("plots/plot.png"):
            plt.savefig("plots/plot.png")
        else:
            count = 0
            while os.path.exists("plots/plot.png" + str(count)):
                count += 1
            plt.savefig("plots/plot" + str(count) + ".png")


        print("FINAL LOSS FOR SIZE", size, losses[len(losses)-1])

