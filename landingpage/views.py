from django.shortcuts import render
from .models import PredictionResult
from .ml_utils import get_models_and_preprocessors, preprocess_input_data
import pandas as pd

def home(request):
    return render(request, 'landingpage/home.html')


def polls(request):
    models = get_models_and_preprocessors()
    xgb_pipeline_model = models.get('xgb_pipeline_model')
    scaler = models.get('scaler')
    label_encoders_features = models.get('label_encoders_features')
    label_encoder_target = models.get('label_encoder_target')
    produk_kategori_mapping = models.get('produk_kategori_mapping')

    

    # Initialize the product images
    products_images = {
        'Baskom': '/static/images/baskom.png',
        'BatuAsah': '/static/images/batuasah.png',
        'BotolKecap': '/static/images/botolkecap.png',
        'BoxDonat': '/static/images/boxdonat.png',
        'Celemek': '/static/images/celemek.png',
        'Ember': '/static/images/ember.png',
        'Garpu': '/static/images/garpu.png',
        'GasPortable': '/static/images/gasportable.png',
        'Gayung': '/static/images/gayung.png',
        'JepitanBakaran': '/static/images/jepitanbakaran.png',
        'KeranjangSampah': '/static/images/keranjangsampah.png',
        'KesetKaki': '/static/images/kesetkaki.png',
        'KuninganKompor': '/static/images/kuningankompor.png',
        'Mancis': '/static/images/mancis.png',
        'Panci': '/static/images/panci.png',
        'PerangkapTikus': '/static/images/PerangkapTikus.png',
        'Pisau': '/static/images/pisau.png',
        'Regulator': '/static/images/regulator.png',
        'Sapu': '/static/images/sapu.png',
        'Saringan': '/static/images/saringan.png',
        'SelangGas': '/static/images/selanggas.png',
        'Sendok': '/static/images/sendok.png',
        'Serbet': '/static/images/serbet.png',
        'Tampi': '/static/images/tampi.png',
        'TudungSaji': '/static/images/tudungsaji.png',
        'Toples': '/static/images/toples.png',
        'Fitting': '/static/images/Fitting.png',
        'Isolasi': '/static/images/isolasi.png',
        'Kabel': '/static/images/kabel.png',
        'Kalkulator': '/static/images/kalkulator.png',
        'LampuLED': '/static/images/lampuled.png',
        'Plug': '/static/images/plug.png',
        'Saklar': '/static/images/saklar.png',
        'Socket': '/static/images/socket.png',
        'StopKontak': '/static/images/stopkontak.png',
        'TestPen': '/static/images/testpen.png',
        'Elbow': '/static/images/elbow.png',
        'Evamatic': '/static/images/evamatic.png',
        'Klem': '/static/images/klem.png',
        'Kran': '/static/images/kran.png',
        'Kuas': '/static/images/kuas.png',
        'LemLilin': '/static/images/lemlilin.png',
        'MataGerinda': '/static/images/matagerinda.png',
        'Meteran': '/static/images/meteran.png',
        'Obeng': '/static/images/obeng.png',
        'Paku': '/static/images/paku.png',
        'SarungTangan': '/static/images/sarungtangan.png',
        'SealTape': '/static/images/sealtape.png',
        'Selang': '/static/images/selang.png',
        'Skop': '/static/images/skop.png',
        'Skrap': '/static/images/skrap.png',
        'TaliTambang': '/static/images/talitambang.png',
        'Thinner': '/static/images/thinner.png',
        'Gembok': '/static/images/gembok.png',
        'Hanger': '/static/images/hanger.png',
        'JasHujan': '/static/images/jashujan.png',
        'JepitanBaju': '/static/images/jepitanbaju.png',
        'Karpet': '/static/images/karpet.png',
        'KlemSelang': '/static/images/KlemSelang.png',
        'Payung': '/static/images/payung.png',
        'Polybag': '/static/images/polybag.png',
        'Celengan': '/static/images/celengan.png',
        'TanahCampur': '/static/images/TanahCampur.png',
        'Tas' : '/static/images/Tas.png',
        'Sekam': '/static/images/Sekam.png',
        'Spon':'/static/images/Spon.png',
        'Sikat':'/static/images/Sikat.png',
        'SumbuKompor':'/static/images/SumbuKompor.png',
        'SoletKaret':'/static/images/SoletKaret.png',
        'TempatBakaran':'/static/images/TempatBakaran.png',
        'TaplakMeja':'/static/images/TaplakMeja.png',
        'Pot':'/static/images/Pot.png',
        'Pupuk': '/static/images/Pupuk Organik.png',
        
    }
    
    if request.method == 'POST':
        # Ambil data form
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        occupation = request.POST.get('occupation')
        event = request.POST.get('event')
        unit = request.POST.get('unit')

        try:
            age = int(age)
        except ValueError:
            error_message = "Umur harus berupa angka."
            return render(request, 'landingpage/polls.html', {'error': error_message, 'form_data': request.POST.dict()})

        try:
            input_data = pd.DataFrame([{
                'Usia': age,
                'Gender': gender,
                'Pekerjaan': occupation,
                'Event': event,
                'Satuan': unit,
                'Jumlah': 1,
                'Harga Produk': 10000.0,
                'Total Harga': 10000.0,
            }])

            processed_data = preprocess_input_data(input_data, label_encoders_features, scaler)
            feature_order_training = ['Usia', 'Jumlah', 'Harga Produk', 'Total Harga', 'Gender', 'Pekerjaan', 'Event', 'Satuan']
            processed_data = processed_data[feature_order_training]

            predicted_encoded = xgb_pipeline_model.predict(processed_data)
            predicted_category = label_encoder_target.inverse_transform([predicted_encoded[0]])[0]

             # Ambil produk dari mapping berdasarkan kategori hasil prediksi
            recommended_products = produk_kategori_mapping.get(predicted_category, [])

            # Remove duplicates due to inconsistent spacing or formatting
            recommended_products = list(set([product.strip().replace(" ", "") for product in recommended_products]))


            # ✅ SIMPAN KE DATABASE
            PredictionResult.objects.create(
                name=name,
                age=age,
                gender=gender,
                occupation=occupation,
                event=event,
                unit=unit,
                predicted_category=predicted_category,
                recommended_products=recommended_products
            )

            result = {
                'name': name,
                'age': age,
                'gender': gender,
                'occupation': occupation,
                'event': event,
                'unit': unit,
                'category': predicted_category,
                'recommended': recommended_products,
                'product_images': {product: products_images.get(product.strip(), '/static/images/default.png') for product in recommended_products}
            }

            return render(request, 'landingpage/polls.html', {
                'result': result,
                'form_data': request.POST.dict()
            })

        except Exception as e:
            error_message = f"Terjadi kesalahan saat prediksi: {str(e)}"
            return render(request, 'landingpage/polls.html', {'error': error_message, 'form_data': request.POST.dict()})

    return render(request, 'landingpage/polls.html')
