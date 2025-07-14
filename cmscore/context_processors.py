import mysql.connector
from django.core.files.storage import default_storage
from .forms import SearchForm
from django.conf import settings

db_settings = settings.DATABASES['default']

class CMI:
    def __init__(self, cmi_id, agency_code, name, detail, logo):
        self.cmi_id = cmi_id
        self.agency_code = agency_code
        self.name = name
        self.detail = detail
        self.logo_url = default_storage.url(logo)

def cmi_list(request):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
                    user=db_settings['USER'],
                    password=db_settings['PASSWORD'],
                    host=db_settings['HOST'],
                    database=db_settings['NAME'],
                    port=db_settings['PORT']
                )
        cursor = conn.cursor()

        query = "SELECT * FROM cmi"
        cursor.execute(query)

        cmi_list = []
        for row in cursor.fetchall():
            cmi = CMI(row[0], row[1], row[2], row[8], row[7])
            cmi_list.append(cmi)
    except mysql.connector.errors.Error as e:
        print(f"An error occurred: {e}")
        cmi_list = None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return {'cmi_list': cmi_list} if cmi_list is not None else {}

def search_form(request):
    return {'form': SearchForm()}