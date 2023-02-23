import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def load_data():
    return pd.read_csv("finalOutputWithOCV.txt")


def plot_curves_no_temperature_data(df):
    def tempfunc(x):
        return int(x.split("_")[0][3:]) if x.split("_")[0][-1] != "_" else int(x.split("_")[0][3:-1])

    df["RunNum"] = df["Run"].apply(tempfunc)
    try:
        df.drop(df.index[df["T"] != 10], axis=0, inplace=True)  # Only working with 10C
    except:
        df.drop(df.index[df["#T"] != 10], axis=0, inplace=True)  # I don't know why it is saved like this
    df.drop(df.index[df["R1"] < 0], axis=0, inplace=True)  # No negative resistances
    df.drop(df.index[df["C1"] < 100], axis=0, inplace=True)  # Bad data
    df.drop(df.index[df["RunNum"] % 5 == 0], axis=0, inplace=True)  # Get rid of high current runs because messes up R1
    df.drop(df.index[df["SOC"] <= 0.1], axis=0, inplace=True)  # one bad data point in R1

    # Start plotting
    plt.figure(1, figsize=(16, 7))

    #Plot of R0 with fit
    ax = plt.subplot(2,4,1)
    plt.scatter(df["SOC"], df["R0"])
    myTemp = np.polyfit(df["SOC"], df["R0"], 6)
    x = np.linspace(0.1, 1, 101)
    plt.plot(x, np.polyval(myTemp, x))
    print("R0 Fit: "+str(myTemp))
    #Plot of residuals
    ax = plt.subplot(2,4,1+4)
    plt.scatter(df["SOC"], df["R0"]-np.polyval(myTemp, df["SOC"]))

    #Plot of R1 with fit
    ax = plt.subplot(2, 4, 2)
    plt.scatter(df["SOC"], df["R1"])
    myTemp = np.polyfit(df["SOC"], df["R1"], 6)
    x = np.linspace(0.1, 1, 101)
    plt.plot(x, np.polyval(myTemp, x))
    print("R1 Fit:" + str(myTemp))

    #Plot of residuals
    ax = plt.subplot(2, 4, 2 + 4)
    plt.scatter(df["SOC"], df["R1"] - np.polyval(myTemp, df["SOC"]))

    #Plot of C1 with fit
    ax = plt.subplot(2, 4, 3)
    plt.scatter(df["SOC"], df["C1"])
    myTemp = np.polyfit(df["SOC"], df["C1"], 4)
    x = np.linspace(0.1, 1, 101)
    y = np.array([max(i, df["C1"].min()) for i in np.polyval(myTemp, x)])
    plt.plot(x, y)
    print("C1 Fit: " + str(myTemp))
    #Plot of residuals
    ax = plt.subplot(2, 4, 3 + 4)
    plt.scatter(df["SOC"], df["C1"] - np.polyval(myTemp, df["SOC"]))

    #Plot of OCV with fit
    ax = plt.subplot(2,4,4)
    plt.scatter(df["OCV_SOC"], df["OCV"])
    myTemp = np.polyfit(df["OCV_SOC"], df["OCV"], 5)
    x = np.linspace(0.1, 1, 101)
    plt.plot(x, np.polyval(myTemp, x))
    print("OCV Fit: "+str(myTemp))
    #Plot of residuals
    ax = plt.subplot(2, 4, 4 + 4)
    plt.scatter(df["SOC"], df["OCV"] - np.polyval(myTemp, df["OCV_SOC"]))
    plt.savefig("paramsNoTemp.png")


def plot_curves(df):
    def tempfunc(x):
        return int(x.split("_")[0][3:]) if x.split("_")[0][-1] != "_" else int(x.split("_")[0][3:-1])

    df["RunNum"] = df["Run"].apply(tempfunc)
    clean_df = df[df["R1"] >= 0]
    clean_df.groupby(["T", "RunNum"]).mean().loc[-20].reset_index()
    clean_df.groupby(["T", "RunNum"]).mean().loc[-10].reset_index()
    clean_df.groupby(["T", "RunNum"]).mean().loc[0].reset_index()
    clean_df.groupby(["T", "RunNum"]).mean().loc[10].reset_index()
    clean_df.groupby(["T", "RunNum"]).mean().loc[25].reset_index()

    plt.figure(1, figsize=(15, 25))
    R0 = {}
    R1 = {}
    C1 = {}
    # R0
    counter = 0
    for i in ["n20C", "n10C", "C0", "C10", "C25"]:
        ax = plt.subplot(5, 3, 1 + counter * 3)
        R0[i] = np.polyfit(eval(i)["SOC"], eval(i)["R0"], 4)
        ax.set_title("R0 vs. SOC for " + i)
        counter += 1
        for j in range(1, 6):
            temp = eval(i)[eval(i)["RunNum"] % 5 == j - 1]
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
            temp = eval(i)[eval(i)["RunNum"] % 5 == j - 1]
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
            temp = eval(i)[eval(i)["RunNum"] % 5 == j - 1]
            plt.scatter(temp["SOC"], temp["C1"])
        x = np.linspace(0, 1, 101)
        y = np.polyval(C1[i], x)
        plt.plot(x, y)

    plt.figlegend(["Current: " + str(i) for i in range(1, 6)], ncol=5, loc=(0.3, 0.95))

    plt.savefig("exampleParameters.png")
    return


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    print("Running")
    df = load_data()
    # plot_curves(df)
    plot_curves_no_temperature_data(df)
