import csv
import time
import tweepy

# Creamos un fichero para agregar los datos extraidos mediante un csv.writer.
csv_file = open('tweets.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)


def write_csv_header():
    """Añade el header al fichero csv."""
    csv_writer.writerow(['Fecha', 'Texto', 'Usuario', 'Localización', 'Longitud', 'Latitud'])


write_csv_header()

# Establecemos las keywords para la búsqueda de tweets: Temática actual "crisis económica".
keywords = ['#crisiseconómica', '#desempleo', '#ERTE', '#SEPE', '#paro', '#desempleados', 'crisiseconómica',
            'desempleo', 'ERTE', 'SEPE', 'paro', 'desempleados']


class MyStreamListener(tweepy.StreamListener):
    """Listener que escribe los tweets a un fichero en formato csv."""

    def __init__(self):
        """Configura la autenticación de la API de Twitter."""
        super().__init__()
        consumer_key = 'xxxxx'
        consumer_secret = 'xxxxx'
        access_token = 'xxxxx'
        access_token_secret = 'xxxxx'

        # Pasamos nuestras credenciales a Tweepy.
        try:
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)

        except:
            print('Error durante la autenticación.')

    def on_status(self, status):
        """Extrae y guarda en el fichero csv los atributos seleccionados."""
        print(status.text, status.created_at, status.user.screen_name)
        # Para obtener la localización del tweet, seleccionamos el atributo coordenadas por ser el más preciso.
        # Además, incluimos la localización proporcionada por el usuario para complementar esta información, ya que
        # a pesar de ser un atributo con mayor margen de error, gran parte de los usuarios no proporcionan sus
        # coordenadas.
        longitude = None
        latitude = None
        if status.coordinates:
            longitude = status.coordinates['coordinates'][0]
            latitude = status.coordinates['coordinates'][1]

        csv_writer.writerow([status.created_at, status.text, status.user.screen_name, status.user.location, longitude,
                             latitude])

    def on_error(self, status_code):
        """Informa cuando se produce el error 420"""
        if status_code == 420:
            print('Error: excedida la capacidad de intentos de conexión a la API.')
            return False


# Creamos un objeto Stream utilizando la clase "MyStreamListener", y conectamos con la API de Twitter.
stream_listener = MyStreamListener()
stream = tweepy.Stream(auth=stream_listener.auth, listener=stream_listener)
stream.filter(track=keywords, is_async=True)

# Establecemos el criterio de parada de la escucha de tweets: criterio temporal (tres horas).
runtime = 10800
time.sleep(runtime)
stream.disconnect()
