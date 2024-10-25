# Portfolio Management Project

## Description
[Add a brief description of your portfolio management project here.]

## Setup and Usage

### 1. Activating the Virtual Environment

Before starting the project, you need to activate the virtual environment:

1. Open PowerShell
2. Run the following command:
   ```bash
   .venv/Scripts/Activate
   ```
   Alternatively, you can use `Ctrl + Shift + P` in VS Code to set up the Python interpreter.

### 2. Running the Project

When using a virtual environment, follow these steps:

1. First, run the following command in the terminal:
   ```bash
   python 
   ```
2. After that, you can use the "Run" button in VS Code.

## Difficulties Encountered

1. Virtual Environment Activation
   - When starting the project, the virtual environment must be activated first.
   - Use the following command in PowerShell:
     ```bash
     e:/zhaoj/download/workSpace/.venv/Scripts/Activate
     ```
   - Alternatively, use `Ctrl + Shift + P` in VS Code to set up the Python interpreter.

2. Running the Project in VS Code
   - When using a virtual environment, the "Run" button in VS Code may not work directly.
   - First, run the following command in the terminal:
     ```bash
     python .\src\chatGPT\TestGpt.py
     ```
   - After executing this command, you can use the "Run" button in VS Code.

3. Github
   3.1 connect to github
      3.1.1 set ssh key in local ('''bash ssh-keygen -t ed255519 -C "zhaoj@zhaoj.com"''')
      3.1.2 the ssh key is saved in local ('''bash                            e:\zhaoj\download\workSpace\id_ed255519.pub''')
      3.1.3 new ssh key in github
   3.2. issues when i try to push code to existing repository
      3.2.1 connect to the repository with ('''bash git remote add origin git@github.com:zhaoj007/portfolio-management.git'''   )(the origin is the name of the repository, which is Alias)
      3.2.2 push code to the repository with ('''bash git push -u origin master''')
      3.2.3 branch name conflict(master, main), the github default set our brach as subranch when we push code to the repository
      3.2.4 solve: 
         3.2.4.1 pull request in github 

code discipline
1. avoid nesting-----solution inversion, merge , extraction
2. avoid code duplication
3. name the function meaningfully
