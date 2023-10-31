from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
from getWeather import parse_api
from dotenv import load_dotenv
import os
import requests
from io import BytesIO


def weather_graph(df, sun):
    hours = [i for i in df]
    new_df = pd.DataFrame({
        'HOUR': hours,
        'TEMP_C': df.iloc[0],
        'CONDITION': df.iloc[1],
        'WIND_KMH': df.iloc[2],
        'ICON': df.iloc[3]
    })

    sunrise = sun[0].split(' ')[0]
    sunset = sun[1].split(' ')[0].split(':')
    sunset[0] = str(int(sunset[0]) + 12)
    new_sunset = ':'.join(sunset)

    time_sunset = datetime.strptime(new_sunset, "%H:%M").time()
    time_sunrise = datetime.strptime(sunrise, "%H:%M").time()

    fig, ax = plt.subplots(figsize=(10, 6))

    x = new_df['HOUR']
    y = new_df['TEMP_C']
    ax.plot(x, y, marker='o', linestyle='-', color='b')
    ax.set_title(f'{locate}')
    daylight_x = []
    daylight_y = []

    for i in range(len(x)):
        response = requests.get(new_df['ICON'].iloc[i])
        img_data = response.content
        img = mpimg.imread(BytesIO(img_data))
        img_extent = [i - 0.5, i + 0.5, y[i] - 1.5, y[i] - 0.5]
        ax.imshow(img, extent=img_extent)
        ax.text(i, y[i] - 2, f'{new_df["WIND_KMH"][i]}\nкм/ч', ha='center', va='center', fontsize=8)
        ax.text(i, y[i] + 0.7, f'{new_df["TEMP_C"][i]}', ha='center', va='center', fontsize=8)
        time1 = datetime.strptime(x[i], "%H:%M").time()
        time2 = datetime.strptime(x[i-1], "%H:%M").time()
        if time1 > time_sunrise > time2:
            ax.text(i - 0.5, min(y) - 2.5, f'Рассвет: \n{sunrise}', ha='center', va='center', fontsize=8, color='green')

        if time1 > time_sunset > time2:
            ax.text(i - 0.5, min(y) - 2.5, f'Закат: \n{new_sunset}', ha='center', va='center', fontsize=8, color='red')
        if time_sunrise < time1 < time_sunset:
            daylight_y.append(y[i])
            daylight_x.append(x[i])

    ax.plot(daylight_x, daylight_y, marker='o', linestyle='-', color='yellow')
    ax.set_xlim(-1, len(x))
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation=45)
    ax.set_ylim(min(y) - 3, max(y) + 2)
    ax.set_xlabel('Время')
    ax.set_ylabel('Температура (°C)')
    plt.tight_layout()
    plt.savefig('output/weather_graph.png')



if __name__ == '__main__':
    load_dotenv()
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    locate = 'Пхукет'
    df, sun = parse_api(locate, WEATHER_API_KEY)
    weather_graph(df, sun)



