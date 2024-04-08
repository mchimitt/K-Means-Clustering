Matthew Chimitt
mmc200005
Assignment 3 Part II Readme

How to build and run the code:
1) Create a virtual environment
- in the command line, run "pip install virtualenv"
- run "python -m venv venv" to create an environment called env
- run ".\venv\Scripts\activate" to enter into the virtual environment

2) install the necessary packages
- tabulate (to create the table) - pip install tabulate
- urllib3 (to get the dataset as a text file) - pip install urllib3

3) Running k_means.py
- Inside the virtual environment, run "python k_means.py"
- When running, the terminal will display the current k means experiment, with each iteration and the current centroids for the clusters.
- After each experiment, a summary is shown including the centroids, number of clusters and their size, as well as the SSE value.
- Once all of the experiments are completed, a table summarizing each experiment is printed to the console. 
    - Each entry of the table has information such as the k value, the SSE value, and the size of each cluster.
- An example table is found in the Part II folder.