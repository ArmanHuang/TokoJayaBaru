from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import pandas as pd
from .ml_utils import get_models_and_preprocessors, preprocess_input_data
from .models import Product, ProductCategory, PredictionResult
from django.conf import settings


def polls(request):
    try:
        # Ambil model dan komponen yang diperlukan
        models = get_models_and_preprocessors()
        xgb_pipeline_model = models.get('xgb_pipeline_model')
        scaler = models.get('scaler')
        label_encoders_features = models.get('label_encoders_features')
        label_encoder_target = models.get('label_encoder_target')
        produk_kategori_mapping = models.get('produk_kategori_mapping')

        # Cek apakah semua komponen penting tersedia
        if not all([xgb_pipeline_model, scaler, label_encoders_features, label_encoder_target, produk_kategori_mapping]):
            return HttpResponse("❌ Model Machine Learning belum lengkap atau gagal dimuat.", status=500)

    except Exception as e:
        return HttpResponse(f"❌ Gagal memuat model Machine Learning: {str(e)}", status=500)

    # Tangani request POST (submit form prediksi)
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        occupation = request.POST.get('occupation')
        event = request.POST.get('event')

        try:
            age = int(age)
        except ValueError:
            return render(request, 'landingpage/polls.html', {
                'error': "Umur harus berupa angka.",
                'form_data': request.POST.dict()
            })

        try:
            # Buat data frame dari input form
            input_df = pd.DataFrame([{
                'Usia': age,
                'Gender': gender,
                'Pekerjaan': occupation,
                'Event': event,
                'Jumlah': 1,
                'Harga Produk': 10000.0,
                'Total Harga': 10000.0,
            }])

            # Preprocess
            processed = preprocess_input_data(input_df, label_encoders_features, scaler)
            ordered_cols = ['Usia', 'Gender', 'Pekerjaan', 'Event', 'Jumlah', 'Harga Produk', 'Total Harga']
            processed = processed[ordered_cols]

            # Prediksi
            prediction = xgb_pipeline_model.predict(processed)
            predicted_category = label_encoder_target.inverse_transform([prediction[0]])[0]

            # Produk rekomendasi
            recommended_names = produk_kategori_mapping.get(predicted_category, [])
            recommended_names_clean = list(dict.fromkeys([p.strip() for p in recommended_names]))
            recommended_products = Product.objects.filter(name__in=recommended_names_clean)

            # Simpan hasil ke DB
            PredictionResult.objects.create(
                name=name,
                age=age,
                gender=gender,
                occupation=occupation,
                event=event,
                predicted_category=predicted_category,
                recommended_products=[p.name for p in recommended_products]
            )

            result = {
                'name': name,
                'age': age,
                'gender': gender,
                'occupation': occupation,
                'event': event,
                'category': predicted_category,
                'recommended': recommended_products
            }

            return render(request, 'landingpage/polls.html', {
                'result': result,
                'form_data': request.POST.dict()
            })

        except Exception as e:
            return render(request, 'landingpage/polls.html', {
                'error': f"❌ Terjadi kesalahan saat prediksi: {str(e)}",
                'form_data': request.POST.dict()
            })

    # Jika GET (form belum diisi), tampilkan form kosong
    return render(request, 'landingpage/polls.html')
