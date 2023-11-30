"""
Data Inspection Utilities Module

This module provides utilities for exploring and visualizing data within a DataFrame.

Functions:
    - get_duplicates: Returns all duplicated rows in a DataFrame or those with specific content.
    - get_dataset_info: Returns summary and metadata from a DataFrame, including dimensions,
                        attribute set, data types, cardinality, values, and missing values.
    - plot_stem: Graphs a stem plot distribution of a specified variable in the DataFrame.
    - plot_cat: Graphs a bar plot of categorical variables in the DataFrame.
    - plot_pie: Graphs a pie chart of categorical variables in the DataFrame.

Usage:
    # Import the module and use the provided functions
    import edautils

    # Example: Get duplicates in the DataFrame
    edautils.get_duplicates(df)

    # Example: Get dataset information
    edautils.get_dataset_info(df)

    # Example: Plot stem plot distribution
    edautils.plot_stem(df, 'count_variable', 'Stem Plot Title')

    # Example: Plot bar plot of categorical variable
    edautils.plot_cat(df, 'categorical_variable')

    # Example: Plot pie chart of categorical variable
    edautils.plot_pie(df, 'categorical_variable')
"""

import matplotlib.pyplot as plt


def get_duplicates(df, content=None):
    """Returns all duplicated rows in a dataframe"""
    if content is None:
        return df[df.duplicated(keep=False)].shape[0]
    return df[df.duplicated(keep=False)]


def get_dataset_info(df):
    """Returns summary and metadata from a dataframe"""
    print(f"Dataset dimensions: {df.shape[0]} rows and {df.shape[1]} columns")
    print("-----------------------------------")
    print("Attribute set:")
    print(df.columns.tolist())
    print("-----------------------------------")
    print("Data types:")
    if df.shape[1] < 84:
        print(df.dtypes)
    else:
        print(df.dtypes.unique().tolist())
    print("-----------------------------------")
    print("Cardinality in variables:")
    print(df.nunique().sort_values())
    print("-----------------------------------")
    print("Values in variables:")
    for col in df:
        print(
            col,
            "->",
            " ".join(str(val) for val in sorted(df[col].value_counts().index[:5])),
            "...",
        )
    print("-----------------------------------")
    print("Missing values in %:")
    na_data = df.isna().sum()
    if na_data[na_data != 0].size < 64:
        print(df.isna().mean() * 100)
    else:
        print("Too much column with NA values")
        print(na_data[na_data != 0])
    print("-----------------------------------")
    print(f"Number of duplicated rows: {get_duplicates(df)}")


def plot_stem(df, count_var, title="", orientation="vertical"):
    """Graph a stem plot distribution"""
    x_vals = df[count_var].value_counts().index
    y_vals = df[count_var].value_counts().values
    plt.stem(x_vals, y_vals, linefmt="black", orientation=orientation)
    if not title:
        plt.title(count_var)
    else:
        plt.title(title)
    plt.show()


def plot_cat(df, catvar):
    """Graph a bar plot of categorical variables"""
    df[catvar].value_counts().plot.bar()
    plt.show()


def plot_pie(df, catvar):
    """Graph a pie chart of categorical variables"""
    df[catvar].value_counts(normalize=True).plot.pie(autopct="%1.0f%%")
    plt.show()
