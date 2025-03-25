@echo off
echo ===== Agent Simulation Environment Setup =====

:: Check if conda is installed
where conda >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Conda not found. Please install Anaconda or Miniconda and add it to PATH.
    goto :EOF
)

:: Create conda environment (if it doesn't exist)
conda env list | findstr "agent_simulation" >nul
if %ERRORLEVEL% neq 0 (
    echo Creating agent_simulation environment...
    conda env create -f environment.yml
) else (
    echo agent_simulation environment already exists.
)

:: Activate environment and run simulation
echo Activating environment and running simulation...
call conda activate agent_simulation
python simulation/run_simulations.py %*

echo.
echo Simulation complete! Generated charts are saved in the current directory.
echo ========================================

pause 