import matplotlib as mpl
mpl.rcParams['font.family'] = "Source Sans Pro"
mpl.rcParams['font.weight'] = "300"
import click

import scipy.stats
import numpy as np
from matplotlib import pyplot as plt

np.random.seed(1)

N = 150
mu = 0.86


@click.group()
def cli():
    pass

@click.command()
def bothlc():
    x = scipy.stats.bernoulli(mu).rvs(size=N)
    n = np.arange(1, N, 4)
    y = [beta_posterior(x[:i]) for i in n]
    y = np.asarray(y)
    plt.errorbar(n, y[:, 0], y[:, 1], color="blue", label="bayes")
    y = [calc_bootstrap_expectation(x[:i]) for i in n]
    y = np.asarray(y)
    plt.errorbar(n, y[:, 0], y[:, 1], color="green", label="bootstrap")
    plt.title("Overlay Learn Curves Bayesian Inference and Bootstrap")
    plt.xlabel("number of trials")
    plt.ylabel("estimated rate and std. deviation")
    plt.axhline(y=mu, color="red")
    plt.legend(fancybox=True)
    plt.savefig("assets/images/learncurve-both.png")

@click.command()
def learncurve():
    x = scipy.stats.bernoulli(mu).rvs(size=N)
    n = np.arange(1, N, 4)
    y = [beta_posterior(x[:i]) for i in n]
    y = np.asarray(y)
    plt.errorbar(n, y[:, 0], y[:, 1])
    mean, std = y[-1, 0], y[-1, 1]
    print("Mean: {}, std {}".format(mean, std))
    plt.title("Learn Curve Bayesian Inference (Beta-Prior)")
    plt.xlabel("number of trials")
    plt.ylabel("estimated rate and std. deviation")
    plt.axhline(y=mu, color="red")
    plt.savefig("assets/images/learncurvebayes.png")


@click.command()
def bslearncurve():
    x = scipy.stats.bernoulli(mu).rvs(size=N)
    n = np.arange(1, N, 4)
    y = [calc_bootstrap_expectation(x[:i]) for i in n]
    y = np.asarray(y)
    plt.errorbar(n, y[:, 0], y[:, 1])
    mean, std = y[-1, 0], y[-1, 1]
    print("Mean: {}, std {}".format(mean, std))
    plt.title("Learn Curve Of Bootstrapped Estimation")
    plt.xlabel("number of trials")
    plt.ylabel("estimated rate and std. deviation")
    plt.axhline(y=mu, color="red")
    plt.savefig("assets/images/learncurvebootstrap.png")


@click.command()
def bootstrap():
    x = scipy.stats.bernoulli(mu).rvs(size=N)
    m = np.fromiter((np.mean(np.random.choice(x, N)) for _ in range(1000)), dtype=float)

    plt.hist(m, np.linspace(0, 1, 50))
    plt.axvline(x=mu, color="red")
    plt.xlabel("Rate")
    plt.ylabel("Occurences")
    plt.savefig("assets/images/histogram.png")

    estimated_probability_bootstrap = m.mean()
    estimated_probability_variance_bootstrap = m.std()

    print("Bootstrap: {} +/-\t{}".format(estimated_probability_bootstrap,
                                         estimated_probability_variance_bootstrap))


cli.add_command(learncurve)
cli.add_command(bootstrap)
cli.add_command(bslearncurve)
cli.add_command(bothlc)


def beta_posterior(x, alpha_0=0.5, beta_0=0.5):
    dist = scipy.stats.beta((x == 1.0).sum() + alpha_0, (x == 0.0).sum() + beta_0)
    return dist.mean(), dist.std()


def calc_bootstrap_expectation(x):
    m = np.fromiter((np.mean(np.random.choice(x, N)) for _ in range(10000)), dtype=float)
    return m.mean(), m.std()


if __name__ == '__main__':
    cli()
