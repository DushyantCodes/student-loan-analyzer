import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "bank_loan_data.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    """Load raw dataset."""
    return pd.read_csv(RAW_DATA_PATH)


def clean_data(df):
    """Clean missing values."""

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Fill missing categorical values
    categorical_columns = df.select_dtypes(include="object").columns

    for column in categorical_columns:
        mode = df[column].mode()[0]
        df[column] = df[column].fillna(mode)

    # Fill missing numerical values
    numerical_columns = df.select_dtypes(exclude="object").columns

    for column in numerical_columns:
        median = df[column].median()
        df[column] = df[column].fillna(median)

    return df


def encode_data(df):
    """Encode categorical columns."""

    encoders = {}

    categorical_columns = df.select_dtypes(include="object").columns

    for column in categorical_columns:
        encoder = LabelEncoder()
        df[column] = encoder.fit_transform(df[column])

        encoders[column] = encoder

    return df, encoders


def split_data(df):
    """Split into train and test sets."""

    X = df.drop("loan_status", axis=1)
    y = df["loan_status"]

    return train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )


def save_processed_data(X_train, X_test, y_train, y_test):
    """Save processed datasets."""

    X_train.to_csv(PROCESSED_DIR / "X_train.csv", index=False)
    X_test.to_csv(PROCESSED_DIR / "X_test.csv", index=False)

    y_train.to_csv(PROCESSED_DIR / "y_train.csv", index=False)
    y_test.to_csv(PROCESSED_DIR / "y_test.csv", index=False)


def prepare_data():
    """Complete preprocessing pipeline."""

    df = load_data()

    df = clean_data(df)

    df, encoders = encode_data(df)

    X_train, X_test, y_train, y_test = split_data(df)

    save_processed_data(
        X_train,
        X_test,
        y_train,
        y_test
    )

    return X_train, X_test, y_train, y_test, encoders


if __name__ == "__main__":

    X_train, X_test, y_train, y_test, encoders = prepare_data()

    print("=" * 50)
    print("Data preprocessing completed.")
    print("=" * 50)
    print(f"Training samples : {len(X_train)}")
    print(f"Testing samples  : {len(X_test)}")
    print(f"Features         : {X_train.shape[1]}")