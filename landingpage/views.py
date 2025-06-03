# views.py
from django.shortcuts import render
import pandas as pd
from .ml_utils import get_models_and_preprocessors, preprocess_input_data
from .models import PredictionResult

def home(request):
    return render(request, 'landingpage/home.html')

def polls(request):
    models = get_models_and_preprocessors()
    xgb_pipeline_model = models.get('xgb_pipeline_model')
    scaler = models.get('scaler')
    label_encoders_features = models.get('label_encoders_features')
    label_encoder_target = models.get('label_encoder_target')
    produk_kategori_mapping = models.get('produk_kategori_mapping')

    # Static image map
    products_images = {
        'Baskom': '/static/images/baskom.png',
        'Gembok': '/static/images/gembok.png',
        'Pupuk': '/static/images/Pupuk Organik.png',
        # ... add all as before
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        occupation = request.POST.get('occupation')
        event = request.POST.get('event')
        unit = request.POST.get('unit')

        try:
            age = int(age)
        except ValueError:
            return render(request, 'landingpage/polls.html', {
                'error': "Umur harus berupa angka.",
                'form_data': request.POST.dict()
            })

        try:
            input_df = pd.DataFrame([{
                'Usia': age,
                'Gender': gender,
                'Pekerjaan': occupation,
                'Event': event,
                'Satuan': unit,
                'Jumlah': 1,
                'Harga Produk': 10000.0,
                'Total Harga': 10000.0,
            }])

            processed = preprocess_input_data(input_df, label_encoders_features, scaler)
            ordered_cols = ['Usia', 'Jumlah', 'Harga Produk', 'Total Harga', 'Gender', 'Pekerjaan', 'Event', 'Satuan']
            processed = processed[ordered_cols]

            prediction = xgb_pipeline_model.predict(processed)
            predicted_category = label_encoder_target.inverse_transform([prediction[0]])[0]

            recommended = produk_kategori_mapping.get(predicted_category, [])
            recommended = list(set([p.strip().replace(" ", "") for p in recommended]))

            PredictionResult.objects.create(
                name=name,
                age=age,
                gender=gender,
                occupation=occupation,
                event=event,
                unit=unit,
                predicted_category=predicted_category,
                recommended_products=recommended
            )

            result = {
                'name': name,
                'age': age,
                'gender': gender,
                'occupation': occupation,
                'event': event,
                'unit': unit,
                'category': predicted_category,
                'recommended': recommended,
                'product_images': {
                    p: products_images.get(p, '/static/images/default.png') for p in recommended
                }
            }

            return render(request, 'landingpage/polls.html', {
                'result': result,
                'form_data': request.POST.dict()
            })

        except Exception as e:
            return render(request, 'landingpage/polls.html', {
                'error': f"Terjadi kesalahan saat prediksi: {str(e)}",
                'form_data': request.POST.dict()
            })

    return render(request, 'landingpage/polls.html')
