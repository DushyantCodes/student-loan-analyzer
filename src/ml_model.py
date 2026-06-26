import joblib
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

from src.data_processor import prepare_data


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"

MODELS_DIR.mkdir(parents=True, exist_ok=True)


def train_model():

    X_train, X_test, y_train, y_test, _ = prepare_data()

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        max_depth=10,
        min_samples_split=5,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("=" * 60)
    print("MODEL PERFORMANCE")
    print("=" * 60)

    print(f"Accuracy : {accuracy_score(y_test, predictions):.4f}")
    print(f"Precision: {precision_score(y_test, predictions):.4f}")
    print(f"Recall   : {recall_score(y_test, predictions):.4f}")
    print(f"F1 Score : {f1_score(y_test, predictions):.4f}")

    print("\nConfusion Matrix")
    print(confusion_matrix(y_test, predictions))

    print("\nClassification Report")
    print(classification_report(y_test, predictions))

    joblib.dump(model, MODELS_DIR / "loan_risk_model.pkl")

    print("\nModel saved successfully!")
    print(MODELS_DIR / "loan_risk_model.pkl")


if __name__ == "__main__":
    train_model()