import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
import joblib

# Carrega e prepara
df = pd.read_csv("dataset.csv")
X = df.drop("label", axis=1)
y = df["label"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split e treino
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
clf = SVC(kernel="rbf", probability=True)
clf.fit(X_train, y_train)

# Avaliação
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Salva modelo e scaler
joblib.dump(clf, "modelo_svm.joblib")
joblib.dump(scaler, "scaler.joblib")
print("✅ Modelo e scaler salvos.")
