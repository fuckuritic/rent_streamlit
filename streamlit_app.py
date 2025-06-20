import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings

warnings.filterwarnings("ignore")

# Загружаем сырой датасет в сайдбар через кнопку и используем декоратор для кеширования

st.title(":red[Привет!]")
st.subheader(
    "Приглашаем вас посмотреть наш отчет по исследованию аренды жилой недвижимости в Москве"
)
st.subheader(" ", divider="gray")

st.subheader(":red[Участники:]")
st.write(":green[Остромецкий Евгений]")
st.write(":green[Алиев Вадим]")
st.write(":green[Панфилов Сергей]")
st.write(":green[Матвеев Андрей]")

st.subheader(" ", divider="gray")

# Чтение CSV из файла (или ты уже получил df другим способом)
df = pd.read_csv("./data/interim/final_data.csv")  # ← здесь твой CSV читается сразу

st.subheader(":red[**Что мы сделали:**]")
st.subheader(":blue[ - Провели первичную обработку датасета]")
st.subheader(":blue[ - Спарсили данные из колонок и создали новые колонки]")
st.subheader(":blue[ - Нашли новые интересные признаки и добавили их в датасет]")
st.subheader(":blue[ - Заполнили пустые значения]")
st.subheader(":blue[ - Сделали энкодинг данных]")
st.subheader(":blue[ - Построили графики и проанализировали их]")
st.subheader(":blue[ - Сделали отчет в Streamlit]")

st.subheader(" ", divider="gray")

# Вывод заголовка
st.title(":green[Наш очищенный датасет]")

# Первые строки
st.subheader("Первые 5 строк:")
st.write(df.head())

st.title(":blue[Наш энкод-датасет]")
df_enc = pd.read_csv("./data/processed/encoding.csv")
st.subheader("Первые 10 строк:")
st.write(df_enc.head(10))

df1 = df.sort_values("price").reset_index(drop=True)
df2 = df[(df["price"] <= 150000) & (df["area_m2"] <= 200)]

st.title("Зависимость цены от площади")
fig = plt.figure()
plt.style.use("ggplot")
# plt.title("Зависимость цены от площади", color="red")
sns.scatterplot(
    data=df2, x="price", y="area_m2", color="#93BDCA", edgecolor="black", alpha=0.7
)
plt.xlabel("Цена аренды в рублях")
plt.ylabel("Общая площадь квартиры")

st.pyplot(fig)


st.title("Распределение квартир по количеству комнат")
fig, ax = plt.subplots()
sns.countplot(data=df, x="num_rooms", ax=ax)
plt.xlabel("Количество комнат")
plt.ylabel("Количество значений")
plt.xticks(ticks=np.arange(0, 6, 1))
st.pyplot(fig)


df3 = df.groupby("num_rooms")["price"].median().reset_index()
mean_prices = df3["price"].values
num_rooms = df3["num_rooms"].values
x = [1, 2, 3, 4, 5, 6]
# st.write(mean_prices)


st.title("Средняя стоимость квартир по количеству комнат")
fig, ax = plt.subplots()
ax.bar(x, mean_prices, width=0.7)
for i, v in enumerate(mean_prices):
    ax.text(x[i], v + 9000, str(v), ha="center", va="bottom")
ax.set_ylim(0, max(mean_prices) + 50000)
plt.xlabel("Количество комнат")
plt.ylabel("Средняя цена")
plt.xticks(ticks=np.arange(1, 7, 1))
st.pyplot(fig)


m = df.groupby("metro")["metro"].count().sort_values(ascending=False)[1:26]


fig3, ax3 = plt.subplots()
ax3.scatter(
    df["time_to_the_metro"],
    df["rent_price_per_metr"],
    alpha=0.5,
    color="green",
    edgecolor="black",
)
ax3.set_title("Зависимость цены от времени до метро")
ax3.set_xlabel("Время до метро (мин)")
ax3.set_ylabel("Цена за м²")
ax3.set_ylim(0, 6000)
ax3.set_xlim(-5, 60)
st.pyplot(fig3)


fig4, ax4 = plt.subplots()
df["layout_type"].value_counts().plot(kind="bar", ax=ax4, color="purple")
ax4.set_title("Распределение по типу планировки")
ax4.set_xlabel("Тип планировки")
ax4.set_ylabel("Количество объявлений")
st.pyplot(fig4)


fig6, ax6 = plt.subplots()
df["trash_chute"].value_counts().plot(
    kind="pie", autopct="%1.1f%%", ax=ax6, startangle=90
)
ax6.set_ylabel("")
ax6.set_title("Наличие мусоропровода")
st.pyplot(fig6)

# Группировка
df_metro_avg = (
    df.groupby("metro")["price"]
    .median()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# Переводим цену в тыс. ₽
df_metro_avg["price"] = df_metro_avg["price"] / 1000

# Рисуем график
fig, ax = plt.subplots()
ax.barh(df_metro_avg["metro"], df_metro_avg["price"], color="skyblue")
ax.set_xlabel("Средняя цена аренды (тыс. ₽)")
ax.set_title("Топ-10 станций метро по средней цене аренды")
ax.set_xlim(0, 900)
ax.invert_yaxis()

# Подписи на барах
for i, v in enumerate(df_metro_avg["price"]):
    ax.text(v + 1, i, f"{v:.1f}", va="center")  # например, "85.2"

st.pyplot(fig)
