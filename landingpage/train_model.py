import pandas as pd
import joblib
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

# Lokasi penyimpanan model dan encoder
MODEL_DIR = 'landingpage/model'
os.makedirs(MODEL_DIR, exist_ok=True)

# 1. Load dataset
df = pd.read_csv('dataseToserbaLagi.csv', delimiter=';')
print(df.columns)

# 2. Drop kolom tidak relevan
df = df.drop(columns=[
    'Tanggal Penjualan',
    'Nama Customer',
    'Nama Produk',
    'Satuan',
    'Merk'
], errors='ignore')

# 3. Pisahkan fitur dan target
target_col = 'Kategori Produk'  # Ganti sesuai nama kolom targetmu
X = df.drop(columns=[target_col])
y = df[target_col]

# 4. Encode kolom kategorikal
label_encoders = {}
for col in X.select_dtypes(include='object').columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

# 5. Scaling fitur numerik
scaler = StandardScaler()
numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns
X[numerical_cols] = scaler.fit_transform(X[numerical_cols])

# 6. Encode target
le_target = LabelEncoder()
y_encoded = le_target.fit_transform(y)

# 7. Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# 8. Train model
model = XGBClassifier(eval_metric='mlogloss')model.fit(X_train, y_train)

# 9. Save model dan preprocessing tools
joblib.dump(model, os.path.join(MODEL_DIR, 'xgb_pipeline_model.pkl'))
joblib.dump(scaler, os.path.join(MODEL_DIR, 'scaler.pkl'))
joblib.dump(label_encoders, os.path.join(MODEL_DIR, 'label_encoders.pkl'))
joblib.dump(le_target, os.path.join(MODEL_DIR, 'label_encoder.pkl'))

# 10. Save mapping kategori → produk (jika tersedia)
if 'Nama Produk' in df.columns:
    mapping_df = df[[target_col, 'Nama Produk']].rename(columns={target_col: 'Kategori Produk'})
    joblib.dump(mapping_df, os.path.join(MODEL_DIR, 'produk_kategori_mapping.pkl'))

print("✅ Training selesai. Semua model dan encoder disimpan.")


