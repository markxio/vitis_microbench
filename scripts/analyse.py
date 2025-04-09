from os import listdir
from os.path import isfile, join
import pandas as pd

def get_files_in_dir(mydir: str) -> list:
    onlyfiles = [f for f in listdir(mydir) if isfile(join(mydir, f))]
    return onlyfiles

def print_min_max_std(myfiles: list, mytype: str):
    min_std=1.00
    max_std=0.00

    min_mean=1.0
    max_mean=1.0

    for myfile in myfiles:
        df=pd.read_csv(f"run_stats/{myfile}", index_col=0)
        # get std
        std=df.loc["std"][0]
        mean=df.loc["mean"][0]

        if std < min_std:
            min_std=std
            min_mean=mean
        if std > max_std:
            max_std=std
            max_mean=mean

    min_std_percent=min_std/min_mean
    max_std_percent=max_std/max_mean

    print(f"{mytype}")
    print(f'max_std: {max_std:.3f} or {max_std_percent:.3f}')
    print(f'min_std: {min_std:.3f} or {min_std_percent:.3f}')

if __name__=="__main__":
    mydir="run_stats"
    myfiles=get_files_in_dir(mydir)

    power_files=[f for f in myfiles if "power" in f]
    exec_files=[f for f in myfiles if "exec" in f]

    print_min_max_std(power_files, "power")
    print_min_max_std(exec_files, "exec")

 
