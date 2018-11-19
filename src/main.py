from experiments import Experiment

import matplotlib.pyplot as plt

import os

def range_train():
    sample_sizes = [1e6]
    for size in sample_sizes:
        exp = Experiment("leagueoflegends", size, 75)
        model, losses, iterations = exp.regular_train()
        exp.predict(model, 1000, "s", True)

        plt.title("Losses for size " + str(size))

        plt.plot(iterations, losses)
        plt.xlabel("Iteration")
        plt.ylabel("Loss")
        
        if not os.path.exists("plots/" + str(size) + ".png"):
            plt.savefig("plots/" + str(size) + ".png")
        else:
            count = 1
            while os.path.exists("plots/" + str(size) + ".png"):
                count += 1
            plt.savefig("plots/" + str(size) + ".png")

        print("#"*80)
        print("FINAL LOSS FOR SIZE ", size, losses[len(losses)-1])
        print("#"*80)

        plt.clf()

def single_complete_train():
    exp = Experiment("leagueoflegends", None, 90)
    model, losses, iterations = exp.regular_train(epochs=1)
    exp.predict(model, 1000, "s", True)

    plt.title("Losses for size " + str(None))

    plt.plot(iterations, losses)
    plt.xlabel("Iteration")
    plt.ylabel("Loss")

def custom():
    filename = "../kelvin"
    exp = Experiment(
        subreddit=None, sample_size=0, percentile=0,
        custom=True, custom_file=filename
    )
    model, losses, iterations = exp.regular_train(epochs=5)
    exp.predict(model, 100, "s", False)


if __name__ == '__main__':
    custom()
    # range_train()


   
