from django.shortcuts import render
from django.conf import settings
import pandas as pd
from django.http import JsonResponse
from .ml_utils import get_models_and_preprocessors, preprocess_input_data
from .models import PredictionResult, ProductCategory, Product

# Home Page View
def home(request):
    categories = ProductCategory.objects.all()
    return render(request, 'landingpage/home.html', {'categories': categories})


# API to Get Products by Category
def get_products_by_category(request, category_name):
    try:
        category = ProductCategory.objects.get(name__iexact=category_name)
        products = Product.objects.filter(category=category)
        product_data = [
            {
                'name': product.name,
                'image': product.image.url if product.image else '',
                'description': product.description or ''
            }
            for product in products
        ]
        return JsonResponse({'products': product_data})
    except ProductCategory.DoesNotExist:
        return JsonResponse({'products': []})


# Polls View with Prediction Logic
def polls(request):
    print("🔥 Form prediksi diakses!")
    
    models = get_models_and_preprocessors()
    xgb_pipeline_model = models.get('xgb_pipeline_model')
    scaler = models.get('scaler')
    label_encoders_features = models.get('label_encoders_features')
    label_encoder_target = models.get('label_encoder_target')
    produk_kategori_mapping = models.get('produk_kategori_mapping')

    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        occupation = request.POST.get('occupation')
        event = request.POST.get('event')

        try:
            age = int(age)
        except (ValueError, TypeError):
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
                'Jumlah': 1,
                'Harga Produk': 10000.0,
                'Total Harga': 10000.0,
            }])

            processed = preprocess_input_data(input_df, label_encoders_features, scaler)
            ordered_cols = ['Usia', 'Gender', 'Pekerjaan', 'Event', 'Jumlah', 'Harga Produk', 'Total Harga']
            processed = processed[ordered_cols]

            prediction = xgb_pipeline_model.predict(processed)
            predicted_category = label_encoder_target.inverse_transform([prediction[0]])[0]

            recommended_names = produk_kategori_mapping.get(predicted_category, [])
            recommended_names_clean = list(dict.fromkeys([p.strip() for p in recommended_names]))

            recommended_products = Product.objects.filter(name__in=recommended_names_clean)

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
                'error': f"Terjadi kesalahan saat prediksi: {str(e)}",
                'form_data': request.POST.dict()
            })

    # Kalau method bukan POST, render form kosong
    return render(request, 'landingpage/polls.html')
