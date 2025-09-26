import numpy as np
import pandas as pd
import streamlit as st
import joblib
import os

st.title('Pitch Classification Tool')
st.markdown("Enter the information of the pitch's characteristics.")

lhp_group_model = joblib.load('../pitch classification/lhp_xgb.pkl')
rhp_group_model = joblib.load('../pitch classification/rhp_xgb.pkl')
lhp_indiv_model = joblib.load('../pitch classification/lhp_indiv_xgb.pkl')
rhp_indiv_model = joblib.load('../pitch classification/rhp_indiv_xgb.pkl')

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

## change these to the average and std for each pitch characteristic
# Average whiff rates for each pitch category - taken from original notebook
fb_avg_whiff = 0.1845164707936013
bb_avg_whiff = 0.3204844619335899
os_avg_whiff = 0.3206088046863918

# Standard Deviation of whiff rates for each pitch category - taken from original notebook
fb_sd_whiff = 0.04856098798686459
bb_sd_whiff = 0.041828507247725584
os_sd_whiff = 0.0516169174758499

with col1:
    pitcher_hand = st.selectbox("Throws: ", ['R', 'L'])
    ivb = st.text_input("IVB: ")

with col2:
    velo = st.text_input("Velo: ")
    hb = st.text_input("HB: ")

with col3:
    spin = st.text_input("Spin Rate:")
    vrel = st.text_input("vRel: ")

with col4:
    spin_axis = st.text_input("Spin Axis: ")
    hrel = st.text_input("hRel: ")

st.markdown("Add your metrics and click Predict")

CLASS_NAMES = ["Changeup", "Curveball", "Cutter", "Four-Seam", "Sinker", "Slider", "Splitter"]

if st.button('Predict'):
    if pitcher_hand == 'R':
        velo_mu = 85.328988
        velo_sigma = 5.884044
        spin_mu = 2198.533963
        spin_sigma = 312.120216
        spin_axis_mu = 180.344428
        spin_axis_sigma = 73.749812
        ivb_mu = 8.540271
        ivb_sigma = 9.275871
        hb_mu = 5.177089
        hb_sigma = 10.753775
        vrel_mu = 5.699887
        vrel_sigma = 0.574529
        hrel_mu = 1.714317
        hrel_sigma = 0.749964

        pitch = pd.DataFrame({'RelSpeed': (float(velo) - velo_mu) / velo_sigma,
                            'SpinRate': (float(spin) - spin_mu) / spin_sigma,
                            'SpinAxis': (float(spin_axis) - spin_axis_mu) / spin_axis_sigma,
                            'InducedVertBreak': (float(ivb) - ivb_mu) / ivb_sigma,
                            'HorzBreak': (float(hb) - hb_mu) / hb_sigma,
                            'RelHeight': (float(vrel) - vrel_mu) / vrel_sigma,
                            'RelSide': (float(hrel) - hrel_mu) / hrel_sigma
                            }, index=[0])
        
        pred_probs = rhp_indiv_model.predict_proba(pitch)
        probs_df = pd.DataFrame(pred_probs, columns=CLASS_NAMES).round(3)
        probs_df = probs_df[probs_df.mean().sort_values(ascending=False).index]
        probs_df = probs_df.applymap(lambda v: f"{round(v*100, 3)}%")
        st.subheader("Predicted Probabilities")
        st.dataframe(probs_df)

    else:
        velo_mu = 83.892891
        velo_sigma = 5.937886
        spin_mu = 2124.585489
        spin_sigma = 305.871343
        spin_axis_mu = 173.801030
        spin_axis_sigma = 72.875846
        ivb_mu = 9.021346
        ivb_sigma = 9.130833
        hb_mu = -6.397521
        hb_sigma = 10.639517
        vrel_mu = 5.662678
        vrel_sigma = 0.511727
        hrel_mu = -1.849377
        hrel_sigma = 0.804853

        pitch = pd.DataFrame({'RelSpeed': (float(velo) - velo_mu) / velo_sigma,
                            'SpinRate': (float(spin) - spin_mu) / spin_sigma,
                            'SpinAxis': (float(spin_axis) - spin_axis_mu) / spin_axis_sigma,
                            'InducedVertBreak': (float(ivb) - ivb_mu) / ivb_sigma,
                            'HorzBreak': (float(hb) - hb_mu) / hb_sigma,
                            'RelHeight': (float(vrel) - vrel_mu) / vrel_sigma,
                            'RelSide': (float(hrel) - hrel_mu) / hrel_sigma
                            }, index=[0])
        
        pred_probs = lhp_indiv_model.predict_proba(pitch)
        probs_df = pd.DataFrame(pred_probs, columns=CLASS_NAMES).round(3)
        probs_df = probs_df[probs_df.mean().sort_values(ascending=False).index]
        probs_df = probs_df.applymap(lambda v: f"{round(v*100, 3)}%")
        st.subheader("Predicted Probabilities")
        st.dataframe(probs_df)