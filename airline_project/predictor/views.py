import pickle, os
import numpy as np
import pandas as pd
from django.shortcuts import render
from .models import Prediction

BASE = os.path.dirname(os.path.abspath(__file__))

model   = pickle.load(open(os.path.join(BASE, 'ml_models/best_model.pkl'), 'rb'))
scaler  = pickle.load(open(os.path.join(BASE, 'ml_models/scaler.pkl'),     'rb'))
imputer = pickle.load(open(os.path.join(BASE, 'ml_models/imputer.pkl'),    'rb'))


CLASS_MAP  = {'Business': 0, 'Eco': 1, 'Eco Plus': 2}
TRAVEL_MAP = {'Business travel': 0, 'Personal Travel': 1} 

def index(request):
    if request.method == 'POST':
        online_boarding  = int(request.POST['online_boarding'])
        inflight_wifi    = int(request.POST['inflight_wifi'])
        seat_comfort     = int(request.POST['seat_comfort'])
        cleanliness      = int(request.POST['cleanliness'])
        travel_class     = request.POST['travel_class']
        type_of_travel   = request.POST['type_of_travel']
        flight_distance  = int(request.POST['flight_distance'])
        total_delay      = int(request.POST['total_delay'])

        features = np.array([[
            online_boarding,
            inflight_wifi,
            seat_comfort,
            cleanliness,
            CLASS_MAP[travel_class],
            TRAVEL_MAP[type_of_travel],
            flight_distance,
            total_delay
        ]])

        features = imputer.transform(features)
        pred_label = model.predict(features)[0]
        pred_proba = model.predict_proba(features)[0]
        
        # Confidence = how sure the model is (highest probability)
        confidence = round(max(pred_proba) * 100, 1)

        # ✅ FIX: sat_probability = actual probability of SATISFIED class
        # This is index [1] because model.classes_ = ['neutral or dissatisfied', 'satisfied']
        # Both confidence and sat_probability now come from the SAME source (predict_proba)
        sat_probability = round(pred_proba[1] * 100, 1)
        
        result = 'Satisfied ✅' if pred_label == 'satisfied' else 'Neutral / Dissatisfied ❌'

        Prediction.objects.create(
            online_boarding  = online_boarding,
            inflight_wifi    = inflight_wifi,
            seat_comfort     = seat_comfort,
            cleanliness      = cleanliness,
            travel_class     = travel_class,
            type_of_travel   = type_of_travel,
            flight_distance  = flight_distance,
            total_delay      = total_delay,
            prediction       = result,
        )

        context = {
            'result'          : result,
            'confidence'      : confidence,
            'sat_probability' : sat_probability,   # ✅ NEW — fixes the gauge inconsistency
            'online_boarding' : online_boarding,
            'inflight_wifi'   : inflight_wifi,
            'seat_comfort'    : seat_comfort,
            'cleanliness'     : cleanliness,
            'travel_class'    : travel_class,
            'type_of_travel'  : type_of_travel,
            'flight_distance' : flight_distance,
            'total_delay'     : total_delay,
        }

        return render(request, 'predictor/result.html', context)

    return render(request, 'predictor/index.html')