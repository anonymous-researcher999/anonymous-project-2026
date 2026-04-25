The structure of the repository and the main components are briefly described below. 

The scripts used to train the neural networks are located in the Codes folder.
The main script, Main_PINN.ipynb, is used to train the network using the modified loss function described in Section 3.1 of the paper.
while Main_default.ipynb corresponds to the version using the standard RMSE loss.
Both scripts call the other Python scripts within the same folder during execution.
Detailed explanations for each component of the implementation are provided as comments within the code files.

A total of four trained models (one default NN and three PINNs) are included.
The default NN and one PINN are trained for the same material, while the remaining two PINNs correspond to two different materials (Tables 2, 7, and 8).

For the inference stage, the trained models can be found in the Models folder, and the required variables are provided in the Vars folder.
Because of their relatively large size, the variables are compressed as a ZIP file and should be extracted before use.

The finite element simulation results for all three benchmark problems presented in the paper are available in the Data folder for direct comparison with the neural network predictions.
These data include the strain, stress, and damage paths at each integration point.

To generate higher quality plots, MATLAB was used. Therefore, the network outputs from the Python implementation were saved in .mat format.
The corresponding files for all three problems are stored in the read from python folder.
All MATLAB (.m) files are solely responsible for visualizing these results.

25/04/2026