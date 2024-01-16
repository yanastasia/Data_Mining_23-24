import pandas as pd
import numpy as np

# Load the dataset
url = "http://archive.ics.uci.edu/ml/machine-learning-databases/voting-records/house-votes-84.data"
names = ["party"] + ["v%d" % i for i in range(1, 17)]
data = pd.read_csv(url, names=names)

# Replacing the "?" with NaN and remove rows with NaN
data.replace("?", pd.NaT, inplace=True)
data.dropna(inplace=True)

# Encode categorical attribute "party" with numerical values
party_encoder = {'republican': 0, 'democrat': 1}
data['party'] = data['party'].map(party_encoder)

# Number of folds for cross-validation
num_folds = 10
fold_size = len(data) // num_folds

# Initialize variables to store accuracy for each run
accuracies = []

for i in range(num_folds):
    # Split the data into training and testing sets for the current fold
    test_start = i * fold_size
    test_end = (i + 1) * fold_size
    test_data = data.iloc[test_start:test_end]
    train_data = pd.concat([data.iloc[:test_start], data.iloc[test_end:]])

    # Separate features and target variable for training and testing
    X_train, y_train = train_data.drop("party", axis=1), train_data["party"]
    X_test, y_test = test_data.drop("party", axis=1), test_data["party"]

    # Convert 'y' and 'n' to 1 and 0, respectively
    X_train_numeric = X_train.apply(lambda col: col.map({'y': 1, 'n': 0}))

    # Convert 'y' and 'n' to 1 and 0, respectively for the test set
    X_test_numeric = X_test.apply(lambda col: col.map({'y': 1, 'n': 0}))

    # Calculate probabilities for each class and feature
    prob_republican = len(y_train[y_train == 0]) / len(y_train)
    prob_democrat = len(y_train[y_train == 1]) / len(y_train)

    # Laplace smoothing
    prob_feature_given_republican = (X_train_numeric[y_train == 0].sum() + 1) / (len(X_train_numeric[y_train == 0]) + 2)
    prob_feature_given_democrat = (X_train_numeric[y_train == 1].sum() + 1) / (len(X_train_numeric[y_train == 1]) + 2)

    # Make predictions on the test set
    predictions = []

    for _, row in X_test_numeric.iterrows():
        prob_republican_given_feature = prob_republican * np.prod(prob_feature_given_republican ** row)
        prob_democrat_given_feature = prob_democrat * np.prod(prob_feature_given_democrat ** row)

        if prob_republican_given_feature > prob_democrat_given_feature:
            predictions.append(0)
        else:
            predictions.append(1)

    # Calculate accuracy
    accuracy = np.mean(predictions == y_test)
    accuracies.append(accuracy)

# Output accuracy for each run
for i, accuracy in enumerate(accuracies, 1):
    print(f"Run {i}: Accuracy = {accuracy:.4f}")

# Output arithmetic mean of accuracy scores
mean_accuracy = np.mean(accuracies)
print(f"\nMean Accuracy: {mean_accuracy:.4f}")
