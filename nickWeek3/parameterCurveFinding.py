import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    return pd.read_csv("finalOutput.txt")

def plot_curves(df):
    tempfunc = lambda x: int(x.split("_")[0][3:]) if x.split("_")[0][-1] != "_" else int(x.split("_")[0][3:-1])
    df["RunNum"] = df["Run"].apply(tempfunc)
    clean_df = df[df["R1"] >= 0]
    temperatures = [-20, -10, 0, 10, 25]
    n20C = clean_df.groupby(["T", "RunNum"]).mean().loc[-20].reset_index()
    n10C = clean_df.groupby(["T", "RunNum"]).mean().loc[-10].reset_index()
    C0 = clean_df.groupby(["T", "RunNum"]).mean().loc[0].reset_index()
    C10 = clean_df.groupby(["T", "RunNum"]).mean().loc[10].reset_index()
    C25 = clean_df.groupby(["T", "RunNum"]).mean().loc[25].reset_index()

    plt.figure(1, figsize=(15, 25))
    R0 = {}
    R1 = {}
    C1 = {}
    # R0
    counter = 0
    for i in ["n20C", "n10C", "C0", "C10", "C25"]:
        ax = plt.subplot(5,3,1+counter*3)
        R0[i] = np.polyfit(eval(i)["SOC"], eval(i)["R0"], 4)
        ax.set_title("R0 vs. SOC for "+i)
        counter += 1
        for j in range(1, 6):
            temp = eval(i)[eval(i)["RunNum"]%5 == j-1]
            plt.scatter(temp["SOC"], temp["R0"])
        x = np.linspace(0, 1, 101)
        y = np.polyval(R0[i], x)
        plt.plot(x, y)

    # R1
    counter = 0
    for i in ["n20C", "n10C", "C0", "C10", "C25"]:
        ax = plt.subplot(5, 3, 2 + counter * 3)
        ax.set_title("R1 vs. SOC for " + i)
        R1[i] = np.polyfit(eval(i)["SOC"], eval(i)["R1"], 4)
        counter += 1
        for j in range(1, 6):
            temp = eval(i)[eval(i)["RunNum"] % 5 == j-1]
            plt.scatter(temp["SOC"], temp["R1"])
        x = np.linspace(0, 1, 101)
        y = np.polyval(R1[i], x)
        plt.plot(x, y)
    # C1
    counter = 0
    for i in ["n20C", "n10C", "C0", "C10", "C25"]:
        ax = plt.subplot(5, 3, 3 + counter * 3)
        ax.set_title("C1 vs. SOC for " + i)
        C1[i] = np.polyfit(eval(i)["SOC"], eval(i)["C1"], 4)
        counter += 1
        for j in range(1, 6):
            temp = eval(i)[eval(i)["RunNum"] % 5 == j-1]
            plt.scatter(temp["SOC"], temp["C1"])
        x = np.linspace(0, 1, 101)
        y = np.polyval(C1[i], x)
        plt.plot(x, y)

    leg = plt.figlegend(["Current: "+str(i) for i in range(1,6)], ncol=5, loc=(0.3, 0.95))

    plt.savefig("exampleParameters.png")
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df = load_data()
    plot_curves(df)
