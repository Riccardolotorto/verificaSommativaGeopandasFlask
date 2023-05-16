from flask import Flask, render_template, request
app = Flask(__name__)

import pandas as pd 
import geopandas as gpd
import os 
import contextily as ctx
import matplotlib.pyplot as plt

quartieri = gpd.read_file('Quartieri/NIL_WM.dbf')
quartieri3857 = quartieri.to_crs(3857)

df = pd.read_csv('sosta_turistici.csv')
from geopandas import GeoDataFrame
from shapely.geometry import Point
geometry = [Point(xy) for xy in zip(df["LONG_X_4326"], df["LAT_Y_4326"])]
df = df.drop(['LONG_X_4326', 'LAT_Y_4326'], axis=1)
parcheggi = GeoDataFrame(df, crs="EPSG:4326", geometry=geometry)
parcheggi3857 = parcheggi.to_crs(3857)
quartieriParcheggi = quartieri3857[quartieri3857.intersects(parcheggi3857.unary_union)]

@app.route('/')
def home():
    listaQuartieriParcheggi = list(quartieriParcheggi['NIL'])
    listaQuartieriParcheggi.sort()
    return render_template("home.html", lista = listaQuartieriParcheggi)


@app.route('/esercizio1')
def es1():
    quartiere = request.args.get('quartiere')
    return render_template("mappa.html")







#dir = "static/images"
#file_name = "es8-9-10.png"
#save_path = os.path.join(dir, file_name)
#plt.savefig(save_path, dpi = 150)















if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)