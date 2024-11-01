# imports
import streamlit as st
import pickle
import pandas as pd
from streamlit_extras.let_it_rain import rain


# Title for adoption predictions
st.title('Am I Getting Adopted?')
st.divider()


city = st.selectbox('Select your city:', ('Austin', 'Dallas'), index = None)

if city == 'Austin':
    # take input
    animal_type = st.selectbox('Select cat or dog: ', ['Cat', 'Dog'], index = None)
    if animal_type == 'Cat':
        animal_type = 0
    else:
        animal_type = 1
    age = st.text_input('Enter age in months: ')
    fixed = st.selectbox('Select if animal will be spayed or neutered: ', ['Yes', 'No'], index = None)
    if fixed == 'Yes':
        fixed = 1
    else:
        fixed = 0
    duration = st.text_input('How many days has pet been at shelter: ')
    breed = st.text_input('Enter breed: ')
    intake_type = st.selectbox('Select intake reason: ', ['Abandoned', 'Stray', 'Public Assist',
                                                       'Owner Surrender', 'Euthanasia Request'], index = None)
    intake_condition = st.selectbox('Select animal condition: ', ['Normal', 'Injured', 'Sick', 'Med Attn', 'Aged',
                                                                  'Med Urgent', 'Behavior', 'Pregnant', 'Feral',
                                                                  'Neurologic', 'Parvo', 'Agonal', 'Congenital',
                                                                  'Panleuk', 'Nursing', 'Space', 'Other'], index = None)
    
    user_inputs = {'animal_type': animal_type, 'intake_age': age, 'spay_neuter': fixed, 'stay_duration':
                   duration, 'breed': breed, 'intake_type': intake_type, 'intake_condition': intake_condition}

    user_inputs_df = pd.DataFrame([user_inputs])

    # generate predictions
    if st.button('Click for prediction'):
        # read in model
        with open('../models/stacked_logr_austin_model.pkl', 'rb') as pickle_in:
            austin_model = pickle.load(pickle_in)
        austin_pred = austin_model.predict(user_inputs_df)
        if austin_pred == 1:
            st.balloons()
            st.text("This animal should get adopted at it's current shelter!")
            st.image('../images/gemini_image_success.jpg')
        else:
            rain(
                emoji = '⚠️',
                font_size = 36,
                falling_speed = 3,
                animation_length = 5)
            st.text(f'This animal only has a {round(austin_model.predict_proba(user_inputs_df)[0][1]*100, 2)}% chance of being adopted.\nLook into other shelters to transfer')
            st.image('../images/gemini_image_failure.jpg')


elif city == 'Dallas':
    # take input
    animal_type = st.selectbox('Select cat or dog: ', ['Cat', 'Dog'], index = None)
    duration = st.text_input('How many days has pet been at shelter: ')
    breed = st.text_input('Enter breed: ')
    intake_type = st.selectbox('Select intake type: ', ['Dispos Req', 'Stray', 'Foster', 'Owner Surrender', 'Confiscated',
                                                         'TNR', 'Keepsafe', 'Treatment', 'Transfer', 'Resource', 'Lost Report',
                                                         'Found Report'], index = None)
    intake_reason = st.text_input('Enter intake reason: ')
    
    user_inputs = {'animal_type': animal_type, 'stay_duration':duration, 'animal_breed': breed, 'intake_type': intake_type,
                   'reason': intake_reason}

    user_inputs_df = pd.DataFrame([user_inputs])

    # generate predictions
    if st.button('Click for prediction'):
        with open('../models/stacked_logr_dallas_model.pkl', 'rb') as pickle_in:
            dallas_model = pickle.load(pickle_in)
        dallas_pred = dallas_model.predict(user_inputs_df)
        if dallas_pred == 1:
            st.balloons()
            st.text("This animal should get adopted at it's current shelter!")
            st.image('../images/gemini_image_success.jpg')
        else:
            rain(
                emoji = '⚠️',
                font_size = 36,
                falling_speed = 3,
                animation_length = 5)
            st.text(f'This animal only has a {round(dallas_model.predict_proba(user_inputs_df)[0][1]*100, 2)}% chance of being adopted.\nLook into other shelters to transfer to.')
            st.image('../images/gemini_image_failure.jpg')