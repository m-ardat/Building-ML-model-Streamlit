# Импорт библиотек
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import random
import joblib

# Рукописная функция
def check_number(input_value):
  """Проверяет, является ли ввод числом.
  Args:
    input_value: Введенное значение.
  Returns:
    True, если ввод является числом, False в противном случае.
  """
  try:
    int(input_value)
    return True
  except ValueError:
    return False

car_mil_med = 240
# Словарь марка модели: страна
model_dict_country = {'Volvo': 'Sweden', 'Volkswagen': 'Germany','Mercedes-Benz': 'Germany',
                      'BMW': 'Germany', 'Audi': 'Germany', 'Toyota': 'Japan',
                      'Nissan': 'Japan', 'Mitsubishi': 'Japan', 'Isuzu': 'Japan',
                      'Lexus': 'Japan', 'Honda': 'Japan', 'Datsun': 'Japan',
                      'Tata': 'India', 'Maruti': 'India', 'Mahindra': 'India',
                      'Ambassador': 'India', 'Skoda': 'Czech', 'Renault': 'France',
                      'Peugeot': 'France', 'Jeep': 'USA', 'Ford': 'USA',
                      'Chevrolet': 'USA', 'Jaguar': 'GB', 'Land': 'GB',
                      'MG': 'GB', 'Fiat': 'Italy', 'Hyundai': 'SK',
                      'Kia': 'SK', 'Daewoo': 'SK', 'Force': 'Taiwan'
                      }

model_dict_number = {'Volvo': 0, 'Volkswagen': 1,'Mercedes-Benz': 2,
                      'BMW': 3, 'Audi': 4, 'Toyota': 5,
                      'Nissan': 6, 'Mitsubishi': 7, 'Isuzu': 8,
                      'Lexus': 9, 'Honda': 10, 'Datsun': 11,
                      'Tata': 12, 'Maruti': 13, 'Mahindra': 14,
                      'Ambassador': 15, 'Skoda': 16, 'Renault': 17,
                      'Peugeot': 18, 'Jeep': 19, 'Ford': 20,
                      'Chevrolet': 21, 'Jaguar': 22, 'Land': 23,
                      'MG': 24, 'Fiat': 25, 'Hyundai': 26,
                      'Kia': 27, 'Daewoo': 28, 'Force': 29
                      }

map_dict_country = {'Sweden': 10, 'GB': 9, 'Germany': 8,
                    'Japan': 7, 'Taiwan': 6, 'USA': 5,
                    'Czech': 4, 'France': 3, 'SK': 2,
                    'India': 1, 'Italy': 0
                    }

# Кортеж брендов автомобилей
keys_model = tuple(model_dict_country.keys())

# Загружаем картинку
img = Image.open("ford_price.png")

# Отображаем заголовок с картинкой по центру
col1h, col2h, col3h = st.columns([1, 8, 1])
with col2h:
    # Заголовок
    st.title("Предсказание стоимости автомобиля")
    # Картинка
    st.image(img, width=700)

# Горизонтальная черта
st.markdown("---")

# Текст - подзаголовок
st.subheader("Для расчёта, пожалуйста, введите характеристики")
# Делим страницу на части
col1, col2 = st.columns([5, 5])
# Заполнение левой части
with col1:
    # Первая кнопка
    car_year = st.text_input("Год выпуска машины")
    # Проверка ввода
    if car_year:
        if check_number(car_year):
            car_year = int(car_year)
            car_year8 = 1 if car_year >= 2015 else 0
        else:
            st.error("Введите корректное число.")

    # Вторая кнопка
    car_mileage = st.number_input("Пробег машины (км)")
    car_km_dr_ok = 1 if car_mileage <= 75000 else 0

    # Третья кнопка
    car_torque = st.number_input("Крутящий момент (Нм)")

    # Четвёртая кнопка
    car_power = st.number_input("Пиковая мощность двигателя (л.с.)")

    # Кнопка - выбор
    fuel_select = ("Дизель", "Бензин", "Другое")
    fuel_mapping = {"Дизель": 0, "Бензин": 1, "Другое": random.choice([2, 3])}
    car_fuel = st.radio(label="Тип топлива", options=fuel_select)
    car_fuel = fuel_mapping[car_fuel]

# Заполнение правой части
with col2:
    # Кнопка - выбор
    car_model = st.selectbox("Марка автомобиля", options=keys_model)
    car_country = model_dict_country[car_model]
    car_model = model_dict_number[car_model]
    car_country = map_dict_country[car_country]

    # Кнопка - выбор
    car_transmission = st.selectbox("Коробка передач", ("РКПП", "АКПП"))
    car_transmission = 1 if car_transmission == "АКПП" else 0

    # Кнопка - выбор
    car_owner = st.selectbox("Первый владелец", ("Да", "Нет"))
    car_owner = 1 if car_owner == "Да" else random.choice([2, 3, 4])

    # Кнопка - ползунок
    car_seats = st.slider('Количество мест', 2, 14)

    # Кнопка - выбор
    car_seller = st.selectbox("Продавец", ("Физ.лицо", "Дилер"))
    car_seller = 0 if car_seller == "лицо" else random.choice([1, 2])

# Горизонтальная черта
st.markdown("---")

# Делим страницу на части
col1f, col2f = st.columns([5, 5])
# Заполнение левой части
with col1f:
    button_clicked_res = st.button("Рассчитать стоимость", key="button1")
    st.write('<style>div.row-widget.stButton > button {background-color: black; color: white}</style>',
             unsafe_allow_html=True)
with col2f:
    if button_clicked_res:
        X = [[car_year, car_mileage, car_mil_med, car_power, car_torque,
             car_seats, car_year8, car_fuel, car_seller, car_transmission,
             car_owner, car_model, car_country, car_km_dr_ok
              ]]

        column = ['year', 'km_driven', 'mileage', 'max_power',
                  'torque', 'seats', 'year8', 'fuel',
                  'seller_type', 'transmission', 'owner', 'name_number',
                  'country_number', 'km_dr_ok'
                  ]

        X_df = pd.DataFrame(X, columns=column)

        # Загрузка модели
        model = joblib.load('model.pkl')

        predict = model.predict(X_df)
        pred_f = np.abs(int(predict[0]))

        st.markdown(
            f'<div style="background-color: white;'
            f'color: black;">Предсказанная стоимость автомобиля: {pred_f}</div>',
            unsafe_allow_html=True
        )