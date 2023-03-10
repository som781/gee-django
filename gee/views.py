from django.shortcuts import render

# generic base view
from django.views.generic import TemplateView 




#folium
import folium
from folium import plugins


#gee
import ee

# ee.Initialize()

email = 'somasunder-ee@ee-somasunder.iam.gserviceaccount.com'
key = 'gee/ee-somasunder-3fcf485d9012.json'
credentials = ee.ServiceAccountCredentials(email, key)
ee.Initialize(credentials)


#forntend
#home
class home(TemplateView):
    template_name = 'index.html'
    # Define a method for displaying Earth Engine image tiles on a folium map.
    

    def get_context_data(self, **kwargs):

        figure = folium.Figure()

        m = folium.Map(
            location=[11.0283259,77.0272806],
            zoom_start=15,
        )
        m.add_to(figure)

        

        dataset = ee.ImageCollection('MODIS/006/MOD13Q1').filter(ee.Filter.date('2022-07-01', '2022-11-30')).first()
        modisndvi = dataset.select('NDVI')
        visParams = {'min':0, 'max':3000, 'palette':['225ea8','41b6c4','a1dab4','034B48']}
        vis_paramsNDVI = {
            'min': 0,
            'max': 9000,
            'palette': [ 'FE8374', 'C0E5DE', '3A837C','034B48',]}

        map_id_dict = ee.Image(modisndvi).getMapId(vis_paramsNDVI)
        folium.raster_layers.TileLayer(
                    tiles = map_id_dict['tile_fetcher'].url_format,
                    attr = 'Google Earth Engine',
                    name = 'NDVI',
                    overlay = True,
                    control = True
                    ).add_to(m)
            
        

        

        m.add_child(folium.LayerControl())
    
        figure.render()

        print('test')
        return {"map": figure}

    

