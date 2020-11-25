call cd ..
call conda env create -f environment.yml
call conda activate NukeWatch
call ipython kernel install --user --name=NukeWatch
pause