import os
import joblib
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import StandardScaler, LabelEncoder
import numpy as np

MODEL_DIR = 'landingpage/model/'

def get_models_and_preprocessors():
    models_and_preprocessors = {}
    try:
        models_and_preprocessors['xgb_pipeline_model'] = joblib.load(os.path.join(MODEL_DIR, 'xgb_pipeline_model.pkl'))
        print("✅ Model XGBoost dimuat.")
    except Exception as e:
        models_and_preprocessors['xgb_pipeline_model'] = None
        print(f"❌ Gagal memuat model XGBoost: {e}")

    try:
        models_and_preprocessors['scaler'] = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
        print("✅ Scaler dimuat.")
    except Exception as e:
        models_and_preprocessors['scaler'] = None
        print(f"❌ Scaler tidak ditemukan atau gagal dimuat: {e}")

    try:
        models_and_preprocessors['label_encoders_features'] = joblib.load(os.path.join(MODEL_DIR, 'label_encoders.pkl'))
        print("✅ Label encoders untuk fitur dimuat.")
    except Exception as e:
        models_and_preprocessors['label_encoders_features'] = {}
        print(f"❌ Label encoders untuk fitur tidak ditemukan atau gagal dimuat: {e}")

    try:
        models_and_preprocessors['label_encoder_target'] = joblib.load(os.path.join(MODEL_DIR, 'label_encoder.pkl'))
        print("✅ Label encoder untuk target dimuat.")
    except Exception as e:
        models_and_preprocessors['label_encoder_target'] = None
        print(f"❌ Label encoder untuk target tidak ditemukan atau gagal dimuat: {e}")

    try:
        df_mapping = joblib.load(os.path.join(MODEL_DIR, 'produk_kategori_mapping.pkl'))
        print("✅ Mapping kategori produk dimuat.")
        
        if isinstance(df_mapping, pd.DataFrame):
            mapping_dict = (
                df_mapping
                .groupby('Kategori Produk')['Nama Produk']
                .apply(list)
                .to_dict()
            )
            models_and_preprocessors['produk_kategori_mapping'] = mapping_dict
            print("Kategori produk tersedia:", list(mapping_dict.keys()))
        else:
            models_and_preprocessors['produk_kategori_mapping'] = df_mapping
    except Exception as e:
        models_and_preprocessors['produk_kategori_mapping'] = None
        print(f"❌ Mapping kategori produk tidak ditemukan atau gagal dimuat: {e}")

    return models_and_preprocessors

def preprocess_input_data(df, label_encoders_features, scaler=None):
    df = df.copy()

    # Kategorikal & numerik fitur
    categorical_features = list(label_encoders_features.keys())
    numerical_features = ['Usia', 'Jumlah', 'Harga Produk', 'Total Harga']

    # Encode kategorikal
    for col in categorical_features:
        if col in df.columns:
            print(f"Encoding kolom: {col}")
            le = label_encoders_features[col]
            try:
                df[col] = le.transform(df[col])
            except ValueError:
                print(f"⚠️ Nilai di kolom '{col}' tidak ditemukan dalam encoder. Menggunakan nilai default.")
                default_val = le.transform([le.classes_[0]])[0]
                df[col] = df[col].apply(lambda x: le.transform([x])[0] if x in le.classes_ else default_val)
        else:
            print(f"⚠️ Kolom '{col}' tidak ditemukan dalam input. Diisi 0.")
            df[col] = 0

    # Scaling numerik
    if scaler:
        try:
            expected_features = scaler.feature_names_in_
            for feat in expected_features:
                if feat not in df.columns:
                    print(f"⚠️ Kolom numerik '{feat}' hilang, diisi 0.")
                    df[feat] = 0
            df = df[expected_features]
            df[expected_features] = scaler.transform(df[expected_features])
            print(f"✅ Data setelah scaling:\n{df.head()}")
        except Exception as e:
            print(f"⚠️ Error saat scaling kolom numerik: {e}")

    return df

def predict_landing_page(input_data):
    models = get_models_and_preprocessors()
    xgb_model = models.get('xgb_pipeline_model')
    scaler = models.get('scaler')
    label_encoders_features = models.get('label_encoders_features')
    label_encoder_target = models.get('label_encoder_target')

    if xgb_model is None or scaler is None or not label_encoders_features:
        return "❌ Model atau preprocessor tidak berhasil dimuat."

    try:
        input_df = pd.DataFrame([input_data])
        input_df = input_df.drop(columns=['Nama Produk'], errors='ignore')

        processed_df = preprocess_input_data(input_df, label_encoders_features, scaler)

        # Urutkan sesuai fitur model
        if hasattr(xgb_model, 'feature_names_in_'):
            model_features = list(xgb_model.feature_names_in_)
        else:
            model_features = processed_df.columns.tolist()  # fallback

        for feat in model_features:
            if feat not in processed_df.columns:
                print(f"⚠️ Menambahkan kolom '{feat}' kosong.")
                processed_df[feat] = 0

        processed_df = processed_df[model_features]

        # Prediksi
        prediction_proba = xgb_model.predict_proba(processed_df)
        print(f"✅ Probabilitas prediksi: {prediction_proba}")

        predicted_class_encoded = prediction_proba.argmax(axis=1)

        if label_encoder_target:
            predicted_class = label_encoder_target.inverse_transform(predicted_class_encoded)[0]
            return f"✅ Prediksi: {predicted_class}, Probabilitas: {prediction_proba[0].max():.4f}"
        else:
            return f"✅ Prediksi (encoded): {predicted_class_encoded[0]}, Probabilitas: {prediction_proba[0].max():.4f}"

    except Exception as e:
        return f"❌ Terjadi kesalahan saat prediksi: {e}"
