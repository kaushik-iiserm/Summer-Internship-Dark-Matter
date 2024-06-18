import ROOT as r
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import gamma
import glob
import os

gem_file = '/home/kaushik/Desktop/FinalInternship2024/dataset/models/*_*'
dir_list = glob.glob(gem_file)  

def polya(G,Go,m):
    return (((np.exp(-m*G/Go)) * m * ((m*G/Go)**(m-1))) / gamma(m))
def polya_2(G,Go,m):
    x = np.linspace(np.min(G),np.max(G),100)
    bin_width = x[1] - x[0] # =20
    polya_height = polya(G, Go, m)
    total_area = np.sum(polya_height * bin_width)
    polya_height = polya_height/total_area
    return polya_height

for dir_path in dir_list:
 
    # Define the pattern for the files within the current directory
    file_pattern = os.path.join(dir_path, '*')
    
    # Get all files in the current directory
    file_list = glob.glob(file_pattern) ## list of all the files in the directory
    # print(file_list)
    for file_path in file_list:
        lower_bounds = [2, 1]
        upper_bounds = [2000, 2.5]
        # print(file_path)
        # Extract the file name from the path (optional)
        file_name = os.path.basename(file_path)
        name_part = os.path.basename(os.path.dirname(file_path))
        if file_name == 'GEM.root':
            # print(file_path)
            gem_file = r.TFile.Open(file_path)
            # print('Opening the file...')
            tree = gem_file.Get("Garfield;1")
            # print('Done!')
            # defining the variables

            avalanche_e = []
            detached_e_position_X = []
            detached_e_position_Y = []
            detached_e_position_Z = []

            # filling the variables

            for entry in tree:
                avalanche = getattr(entry,"numberOfAvalancheElectrons")
                for value in avalanche:
                    avalanche_e.append(value)
                    
                # position = getattr(entry,"initialElectronXpositions")
                # for value in position:
                #     detached_e_position_X.append(value) 
                    
                # position = getattr(entry,"initialElectronYpositions")
                # for value in position:
                #     detached_e_position_Y.append(value)
                
                # position = getattr(entry,"initialElectronZpositions")
                # for value in position:
                #     detached_e_position_Z.append(value)
                fig, ax = plt.subplots()
                count, bins, _ = ax.hist(avalanche_e, bins=100, density=True, alpha=0.6, color='g')
                count = np.array(count)
                bins = np.array(bins)
                count = count[1:]
                bins = bins[1:]
                bins = bins[1:] - (bins[1] - bins[0])/2
                bins = bins[count !=0]
                count = count[count !=0]
                
                params, cov = curve_fit(polya_2, bins, count, bounds=(lower_bounds, upper_bounds))
                gain_fit, m_fit = params
                x = np.linspace(0,np.max(bins),100)
                # x = np.linspace(np.min(bins),np.max(bins),100)
                pdf_fit = polya_2(x, gain_fit, m_fit)
                
                ax.plot(x, pdf_fit, 'k-',color='blue', label='Fitted Polya Distribution')

                ax.set_title('Fitting Polya Distribution')
                ax.set_xlabel('Number of Avalanche Electrons')
                ax.set_ylabel('Probability')
                ax.legend()
                ax.grid()
                # print('Done!')
                                
                
                # Save the plot with the extracted part of the path in the filename
                save_path = f'/home/kaushik/Desktop/FinalInternship2024/dataset/histograms/{name_part}.png'
                plt.savefig(save_path,dpi=100)
                ax.clear()
                # print(np.mean(np.array(avalanche_e)), np.std(np.array(avalanche_e)))
                ## analysis of the data
                # print('Done!') 
                # gem_file.Close() 
                with open("data.txt","r+") as f:
                    old = f.read()
                    f.seek(0)
                    f.write(f"{name_part} {gain_fit}\n{old}")


# import pandas as pd
# import re

# # Function to clean and format the data
# def clean_and_format_data(file_path):
#     with open(file_path, 'r') as file:
#         content = file.readlines()

#     # Use regular expressions to split the data
#     cleaned_data = []
#     for line in content:
#         # Split by one or more spaces or tabs
#         split_line = re.split(r'\s+', line.strip())
#         cleaned_data.append(split_line)
#     # Create a DataFrame from the cleaned data
#     df = pd.DataFrame(cleaned_data[1:], columns=["Field Configuration", "Gain"])

#     return df

# # Path to your text file
# file_path = 'data.txt'

# # Clean and format the data, and create a DataFrame
# df = clean_and_format_data(file_path)

# # Display the DataFrame
# # print(df)
# df[['Drift', 'Avalanche', 'Induction']] = df['Field Configuration'].str.split('_', expand=True)

# # Drop the original "Field Configuration" column if no longer needed
# df = df.drop(columns=['Field Configuration'])

# # Display the DataFrame
# print(df)

# df.to_csv('gain.csv', index=False)

# df = pd.read_csv("gain.csv", header=0)

# print("Done!!")

