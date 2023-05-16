from flask import Flask, render_template, request
app = Flask(__name__)

import pandas as pd 
import geopandas as gpd
import os 
import contextily as ctx
import matplotlib.pyplot as plt

quartieri = gpd.read_file('Quartieri/NIL_WM.dbf')
quartieri3857 = quartieri.to_crs(3857)

df = pd.read_csv('sosta_turistici.csv', sep = ";")
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
    quartiereSelezionato = quartieri3857[quartieri3857.NIL == quartiere]
    parcheggiQuartiereSelezionato = parcheggi3857[parcheggi3857.within(quartiereSelezionato.geometry.item())]
    ax = quartiereSelezionato.plot(figsize = (17, 12), edgecolor = 'k', facecolor = 'none')
    parcheggiQuartiereSelezionato.plot(ax = ax, markersize = 25, color = 'red')
    ctx.add_basemap(ax)

    dir = "static/images"
    file_name = "es1.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("mappa.html", immagine = file_name)



@app.route('/esercizio2')
def es2():
    longitudine = float(request.args.get('longitudine'))
    latitudine = float(request.args.get('latitudine'))
    from shapely.geometry import Point
    punto = gpd.GeoSeries([Point(longitudine, latitudine)], crs = 4326).to_crs(3857)
    m500 = parcheggi3857[parcheggi3857.distance(punto.geometry.item()) < 500]
    if len(m500) > 0:
        quartieriParcheggi500 = quartieri3857[quartieri3857.intersects(m500.unary_union)]
        ax = m500.plot(figsize = (17, 12), markersize = 40, color = 'red')
        quartieriParcheggi500.plot(ax = ax, edgecolor = 'k', facecolor = 'none', linewidth = 2)
        ctx.add_basemap(ax)

        dir = "static/images"
        file_name = "es2.png"
        save_path = os.path.join(dir, file_name)
        plt.savefig(save_path, dpi = 150)
        return render_template("mappa.html", immagine = file_name)
    else:
        risultato = "non ci sono parcheggi nel raggio di 500 metri"
        return render_template("errore.html", ris = risultato)





if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)