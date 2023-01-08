import io
import folium
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        coordinate = (41.368268383757226, 36.2139464913406)
        m = folium.Map(
        	tiles='Stamen Terrain',
            # width= 300,
            # height= 430,
        	zoom_start=13,
        	location = coordinate
        )
        folium.Marker(
            location=[41.36469330997877, 36.18545070300669],
            popup="HAVA ARACI KONUMU",
            icon=folium.Icon(icon="cloud")
        ).add_to(m)

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        self.webView = QWebEngineView()
        self.webView.setHtml(data.getvalue().decode())