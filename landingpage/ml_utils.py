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
        models_and_preprocessors['produk_kategori_mapping'] = joblib.load(os.path.join(MODEL_DIR, 'produk_kategori_mapping.pkl'))
        print("✅ Mapping kategori produk dimuat.")
    except Exception as e:
        models_and_preprocessors['produk_kategori_mapping'] = None
        print(f"❌ Mapping kategori produk tidak ditemukan atau gagal dimuat: {e}")

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

    return models_and_preprocessors

def preprocess_input_data(df, label_encoders_features, scaler=None):
    df = df.copy()

    # Encode kolom kategorikal
    for col, le in label_encoders_features.items():
        if col in df.columns:
            print(f"Encoding kolom: {col}")
            try:
                df[col] = le.transform(df[col])
            except ValueError:
                print(f"⚠️ Nilai di kolom '{col}' tidak ditemukan dalam encoder. Menggunakan nilai default.")
                default_value = le.transform([le.classes_[0]])[0] if len(le.classes_) > 0 else -1
                df[col] = df[col].apply(lambda x: default_value if x not in le.classes_ else le.transform([x])[0])
        else:
            print(f"⚠️ Kolom '{col}' tidak ditemukan dalam data input untuk encoding.")

    # Scaling kolom numerik
    if scaler:
        numerical_features_to_scale = ['Harga Produk', 'Jumlah', 'Total Harga', 'Usia']
        present_numerical_features = [col for col in numerical_features_to_scale if col in df.columns]

        scaler_feature_names = list(scaler.feature_names_in_) if hasattr(scaler, 'feature_names_in_') else present_numerical_features
        ordered_numerical_features = [col for col in scaler_feature_names if col in present_numerical_features]

        if ordered_numerical_features:
            try:
                df[ordered_numerical_features] = scaler.transform(df[ordered_numerical_features])
                print(f"Data setelah scaling: {df[ordered_numerical_features].head()}")
            except ValueError as e:
                print(f"⚠️ Error saat scaling kolom numerik: {e}")

    return df

def predict_landing_page(input_data):
    models = get_models_and_preprocessors()
    xgb_model = models.get('xgb_pipeline_model')
    scaler = models.get('scaler')
    label_encoders_features = models.get('label_encoders_features')
    label_encoder_target = models.get('label_encoder_target')
    produk_kategori_mapping = models.get('produk_kategori_mapping')
    

    if xgb_model is None or scaler is None or not label_encoders_features:
        return "Model atau preprocessor tidak berhasil dimuat."

    try:
        input_df = pd.DataFrame([input_data])
        input_df = input_df.drop(columns=['Nama Produk'], errors='ignore')

        processed_df = preprocess_input_data(input_df, label_encoders_features, scaler)

        # Urutkan fitur sesuai model
        if hasattr(xgb_model, 'feature_names_in_'):
            processed_df = processed_df[xgb_model.feature_names_in_]
        else:
            feature_order_training = ['Usia', 'Gender', 'Pekerjaan', 'Event', 'Satuan', 'Jumlah', 'Harga Produk', 'Total Harga']
            processed_df = processed_df[feature_order_training]

        prediction_proba = xgb_model.predict_proba(processed_df)
        print(f"Probabilitas prediksi: {prediction_proba}")

        predicted_class_encoded = prediction_proba.argmax(axis=1)

        if label_encoder_target:
            predicted_class = label_encoder_target.inverse_transform(predicted_class_encoded)[0]
            return f"Prediksi: {predicted_class}, Probabilitas: {prediction_proba[0].max():.4f}"
        else:
            return f"Prediksi (encoded): {predicted_class_encoded[0]}, Probabilitas: {prediction_proba[0].max():.4f}"

    except Exception as e:
        return f"Terjadi kesalahan saat prediksi: {e}"
