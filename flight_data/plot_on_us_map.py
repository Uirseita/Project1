import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from math import log10


def plot_delay_avr_percentage():
    avr_delay = pd.read_csv('airport_delay.csv')
    avr_delay['delay_percentage'] = avr_delay['delay_count'] \
                                    / avr_delay['total_count']
    avr_delay = avr_delay[avr_delay['total_count'] >= 10]
    # continental US
    lat = avr_delay['LATITUDE'].values
    lon = avr_delay['LONGITUDE'].values
    size = avr_delay['passenger_count'].apply(lambda x: log10(x)).values
    colors = avr_delay['delay_percentage'].values
    m = Basemap(llcrnrlon=-128,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=51,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-96,
                resolution='l', epsg=4687)
    m.arcgisimage(service="ESRI_StreetMap_World_2D", xpixels=950)
    m.drawcoastlines(color='gray')
    m.drawcountries(color='black')
    m.drawstates(color='grey')
    m.scatter(lon, lat, latlon=True,
          c=colors, cmap=plt.cm.hot_r, alpha=0.7, s=2.5 ** size)
    # make a color bar
    plt.colorbar(label=r'Delay Percentage')
    plt.clim(0, 0.4)
    # make a legend
    for a in [50000, 500000, 5000000]:
        plt.scatter([], [], c='k', alpha=0.5, s=2.5 ** log10(a),
                    label=str(2*a))
    plt.legend(scatterpoints=1, frameon=False,
               labelspacing=1, loc='lower right', title='Annual Passenger Count')
    fig = plt.gcf()
    fig.set_size_inches(18.5, 7.5)
    plt.show()


    # Alaska
    m = Basemap(llcrnrlon=-170,llcrnrlat=50,urcrnrlon=-110,urcrnrlat=72,
            projection='lcc',lat_1=59,lat_2=66,lon_0=-142,
                resolution='l', epsg=2964)
    m.arcgisimage(service="ESRI_StreetMap_World_2D", xpixels=950)
    m.drawcountries(color='black')
    m.drawstates(color='grey')
    m.scatter(lon, lat, latlon=True,
          c=colors, cmap=plt.cm.hot_r, alpha=0.7, s=2.5 ** size * 4)
    ax_2 = plt.gca()
    ax_2.text(.7,.15,'Alaska',
            horizontalalignment='center',
            transform=ax_2.transAxes, color='red', fontsize=25)


    # Hawaii
    m = Basemap(llcrnrlon=-160,llcrnrlat=18,urcrnrlon=-154,urcrnrlat=23,
            projection='lcc',lat_1=19.5,lat_2=22,lon_0=-156,
                resolution='l', epsg=2782)
    m.arcgisimage(service="ESRI_StreetMap_World_2D", xpixels=500)
    m.drawcountries(color='black')
    m.drawstates(color='grey')
    m.scatter(lon, lat, latlon=True,
          c=colors, cmap=plt.cm.hot_r, alpha=0.7, s=2.5 ** size * 4)
    ax_3 = plt.gca()
    ax_3.text(.35,.4,'Hawaii',
            horizontalalignment='center',
            transform=ax_3.transAxes, color='red', fontsize=25)


    # Puerto Rico & US Virgin Islands
    m = Basemap(llcrnrlon=-68,llcrnrlat=17.5,urcrnrlon=-64,urcrnrlat=18.6,
            projection='lcc',lat_1=18,lat_2=18.5,lon_0=-66,
                resolution='l', epsg=2866)
    m.arcgisimage(service="ESRI_StreetMap_World_2D", xpixels=1000)
    m.drawcountries(color='black')
    m.drawstates(color='grey')
    m.scatter(lon, lat, latlon=True,
          c=colors, cmap=plt.cm.hot_r, alpha=0.7, s=2.5 ** size * 4)
    ax_4 = plt.gca()
    ax_4.text(.37,.15,'Puerto Rico & US Virgin Islands',
            horizontalalignment='center',
            transform=ax_4.transAxes, color='red', fontsize=17)


    # American Samoa
    m = Basemap(llcrnrlon=-171,llcrnrlat=-14.4,urcrnrlon=-170.5,urcrnrlat=-14.2,
            projection='lcc',lat_1=-14.4,lat_2=-14.2,lon_0=-170.75,
                resolution='l', epsg=3102)
    m.arcgisimage(service="ESRI_StreetMap_World_2D", xpixels=1000)
    m.drawcountries(color='black')
    m.drawstates(color='grey')
    m.scatter(lon, lat, latlon=True,
          c=colors, cmap=plt.cm.hot_r, alpha=0.7, s=2.5 ** size * 100 / 16)
    ax_5 = plt.gca()
    ax_5.text(.35,.75,'American Samoa',
            horizontalalignment='center',
            transform=ax_5.transAxes, color='red', fontsize=25)

    # Guam
    m = Basemap(llcrnrlon=144.5,llcrnrlat=13.2,urcrnrlon=145,urcrnrlat=13.7,
            projection='lcc',lat_1=13.3,lat_2=13.6,lon_0=144.75,
                resolution='l', epsg=4675)
    m.arcgisimage(service="ESRI_StreetMap_World_2D", xpixels=1000)
    m.drawcountries(color='black')
    m.drawstates(color='grey')
    m.scatter(lon, lat, latlon=True,
          c=colors, cmap=plt.cm.hot_r, alpha=0.7, s=2.5 ** size * 100 / 16)
    ax_6 = plt.gca()
    ax_6.text(.35,.75,'Guam',
            horizontalalignment='center',
            transform=ax_6.transAxes, color='red', fontsize=25)


def plot_delay_avr_minutes():
    avr_delay = pd.read_csv('airport_delay.csv')
    avr_delay = avr_delay[avr_delay['total_count'] >= 10]
    # set the stations 3 std of avr_day far away mean to mean + 3 std
    inx = avr_delay[
        np.abs(avr_delay.avr_delay - avr_delay.avr_delay.mean()) > (
                    3 * avr_delay.avr_delay.std())].index.tolist()
    set_value = avr_delay.avr_delay.mean() + 3 * avr_delay.avr_delay.std()
    for i in inx:
        avr_delay.loc[i, 'avr_delay'] = set_value

    # continental US
    lat = avr_delay['LATITUDE'].values
    lon = avr_delay['LONGITUDE'].values
    size = avr_delay['passenger_count'].apply(lambda x: log10(x)).values
    colors = avr_delay['avr_delay'].values
    m = Basemap(llcrnrlon=-128, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=51,
                projection='lcc', lat_1=33, lat_2=45, lon_0=-96,
                resolution='l', epsg=4687)
    m.arcgisimage(service="ESRI_StreetMap_World_2D", xpixels=950)
    m.drawcoastlines(color='gray')
    m.drawcountries(color='black')
    m.drawstates(color='grey')
    m.scatter(lon, lat, latlon=True,
              c=colors, cmap=plt.cm.hot_r, alpha=0.7, s=2.5 ** size)
    # make a color bar
    plt.colorbar(label=r'Delay Percentage')
    plt.clim(0, 0.4)
    # make a legend
    for a in [50000, 500000, 5000000]:
        plt.scatter([], [], c='k', alpha=0.5, s=2.5 ** log10(a),
                    label=str(2 * a))
    plt.legend(scatterpoints=1, frameon=False,
               labelspacing=1, loc='lower right',
               title='Annual Passenger Count')
    fig = plt.gcf()
    fig.set_size_inches(18.5, 7.5)
    plt.show()

    # Alaska
    m = Basemap(llcrnrlon=-170, llcrnrlat=50, urcrnrlon=-110, urcrnrlat=72,
                projection='lcc', lat_1=59, lat_2=66, lon_0=-142,
                resolution='l', epsg=2964)
    m.arcgisimage(service="ESRI_StreetMap_World_2D", xpixels=950)
    m.drawcountries(color='black')
    m.drawstates(color='grey')
    m.scatter(lon, lat, latlon=True,
              c=colors, cmap=plt.cm.hot_r, alpha=0.7, s=2.5 ** size * 4)
    ax_2 = plt.gca()
    ax_2.text(.7, .15, 'Alaska',
              horizontalalignment='center',
              transform=ax_2.transAxes, color='red', fontsize=25)

    # Hawaii
    m = Basemap(llcrnrlon=-160, llcrnrlat=18, urcrnrlon=-154, urcrnrlat=23,
                projection='lcc', lat_1=19.5, lat_2=22, lon_0=-156,
                resolution='l', epsg=2782)
    m.arcgisimage(service="ESRI_StreetMap_World_2D", xpixels=500)
    m.drawcountries(color='black')
    m.drawstates(color='grey')
    m.scatter(lon, lat, latlon=True,
              c=colors, cmap=plt.cm.hot_r, alpha=0.7, s=2.5 ** size * 4)
    ax_3 = plt.gca()
    ax_3.text(.35, .4, 'Hawaii',
              horizontalalignment='center',
              transform=ax_3.transAxes, color='red', fontsize=25)

    # Puerto Rico & US Virgin Islands
    m = Basemap(llcrnrlon=-68, llcrnrlat=17.5, urcrnrlon=-64, urcrnrlat=18.6,
                projection='lcc', lat_1=18, lat_2=18.5, lon_0=-66,
                resolution='l', epsg=2866)
    m.arcgisimage(service="ESRI_StreetMap_World_2D", xpixels=1000)
    m.drawcountries(color='black')
    m.drawstates(color='grey')
    m.scatter(lon, lat, latlon=True,
              c=colors, cmap=plt.cm.hot_r, alpha=0.7, s=2.5 ** size * 4)
    ax_4 = plt.gca()
    ax_4.text(.37, .15, 'Puerto Rico & US Virgin Islands',
              horizontalalignment='center',
              transform=ax_4.transAxes, color='red', fontsize=17)

    # American Samoa
    m = Basemap(llcrnrlon=-171, llcrnrlat=-14.4, urcrnrlon=-170.5,
                urcrnrlat=-14.2,
                projection='lcc', lat_1=-14.4, lat_2=-14.2, lon_0=-170.75,
                resolution='l', epsg=3102)
    m.arcgisimage(service="ESRI_StreetMap_World_2D", xpixels=1000)
    m.drawcountries(color='black')
    m.drawstates(color='grey')
    m.scatter(lon, lat, latlon=True,
              c=colors, cmap=plt.cm.hot_r, alpha=0.7, s=2.5 ** size * 100 / 16)
    ax_5 = plt.gca()
    ax_5.text(.35, .75, 'American Samoa',
              horizontalalignment='center',
              transform=ax_5.transAxes, color='red', fontsize=25)

    # Guam
    m = Basemap(llcrnrlon=144.5, llcrnrlat=13.2, urcrnrlon=145, urcrnrlat=13.7,
                projection='lcc', lat_1=13.3, lat_2=13.6, lon_0=144.75,
                resolution='l', epsg=4675)
    m.arcgisimage(service="ESRI_StreetMap_World_2D", xpixels=1000)
    m.drawcountries(color='black')
    m.drawstates(color='grey')
    m.scatter(lon, lat, latlon=True,
              c=colors, cmap=plt.cm.hot_r, alpha=0.7, s=2.5 ** size * 100 / 16)
    ax_6 = plt.gca()
    ax_6.text(.35, .75, 'Guam',
              horizontalalignment='center',
              transform=ax_6.transAxes, color='red', fontsize=25)

if __name__ == "__main__":
    pass
