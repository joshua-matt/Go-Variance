# Go-Variance
In this project, I analyze the 18k and 9d subsets of [featurecat's Go dataset](https://github.com/featurecat/go-dataset/tree/master/) to discover how final positions differ between low- and high-ranked amateur Go players. Both of the analyses I perform rely on the covariance matrix of the dataset (hence "Go-Variance"), and we make sense of the analyses through pretty visualizations. Check out [writeup.pdf](https://github.com/joshua-matt/Go-Variance/blob/main/writeup.pdf) for the whole story! (Download the writeup to make the clickable links in the writeup work.)

## Data
In this repository, I include the data I used. The folders with the suffix `featurecat` contain the original game data in .sgf format. The folders with the suffix `csv` contain the final board states of the games in the corresponding `featurecat` folder. Finally, the folders with the suffix `norm` contain the mean-normalized versions of the `csv` data.

## Plots
I also include the plots I generated based on the data. In the `covariance` folder, you will find the visualization of the correlation matrices for each subset, as well as visualizations of the correlations associated with each of the 361 positions of the board. The latter images are simply the reshaped rows of the former. In the `PCA` folder, you will find visualizations of the principal components for each dataset.
