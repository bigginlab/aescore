import os

import mlflow
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from scipy import stats
from sklearn.metrics import mean_squared_error

colors = {"train": "tab:blue", "valid": "tab:orange", "test": "tab:green"}


def regplot(true, predicted, name, std=None, color=None, path=""):
    """
    Regression plot of predicted versus true (experimental) values.

    Save plot as PNG and PDF, and track files in MLFlow.
    """

    if color is None:
        try:
            color = colors[name]
        except KeyError:
            color = "black"

    pr = stats.pearsonr(true, predicted)[0]
    sr = stats.spearmanr(true, predicted)[0]
    rmse = np.sqrt(mean_squared_error(true, predicted))

    g = sns.jointplot(x=true, y=predicted, kind="reg", color=color)

    if std is not None:
        # Add std as errorbar
        g.ax_joint.errorbar(
            true, predicted, yerr=std, fmt="none", ecolor=color, alpha=0.25
        )

    plt.xlabel("Experimental")
    plt.ylabel("Predicted")

    plt.text(
        0.5,
        0.05,
        f"RMSE = {rmse:.2f} | Pearson's $r$ = {pr:.2f} | Spearman's $\\rho$ = {sr:.2f}",
        horizontalalignment="center",
        verticalalignment="center",
        bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.5},
        transform=plt.gca().transAxes,
    )

    plt.tight_layout()

    savefig(f"regplot-{name}", path=path)

    # Log plots and values
    mlflow.log_param(f"pearson_{name}", pr)
    mlflow.log_param(f"spearman_{name}", sr)
    mlflow.log_param(f"rmse_{name}", rmse)


def savefig(name, path=""):
    """
    Save plot as PNG and PDF, and track files in MLFlow.
    """
    outprefix = os.path.join(path, name)

    for ext in [".pdf", ".png"]:
        out = outprefix + ext

        plt.savefig(out)
        mlflow.log_artifact(out)
