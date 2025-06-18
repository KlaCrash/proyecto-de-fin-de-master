from Funciones_Proyecto import (
    configurar_servicio,
    inicializar_navegador,
    cargar_mas_resultados,
    esperar_div_padre,
    encontrar_div_hijos,
    extraer_titulo_y_estrellas_csv,
    extraer_precios_meses_csv,
    extraer_camas_csv,
    extraer_categorias_notas_csv,
    extraer_pois_csv,
    extraer_comentarios_csv
)
import time
from selenium.webdriver.common.by import By
import csv

# URL del sitio web
urls = {
    "Madrid": {
        "hotel": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8164cd8ddb75d5a8c96d0dc0708d7aed&aid=304142&dest_id=-390625&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&nflt=ht_id%3D204',  # URL para hoteles
        "hostal": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8164cd8ddb75d5a8c96d0dc0708d7aed&aid=304142&dest_id=-390625&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&nflt=ht_id%3D216',  # URL para hostales/pensiones
        "albergue": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8164cd8ddb75d5a8c96d0dc0708d7aed&aid=304142&dest_id=-390625&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&nflt=ht_id%3D203',  # URL para albergues
    },
    
    "Sevilla": {
        "hotel": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&dest_id=-402849&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&nflt=ht_id%3D204',  # URL para hoteles
        "hostal": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&dest_id=-402849&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&nflt=ht_id%3D216',  # URL para hostales/pensiones
        "albergue": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&dest_id=-402849&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&nflt=ht_id%3D203',  # URL para albergues
    },

    "Granada": {
        "hotel": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&dest_id=-384328&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&nflt=ht_id%3D204',  # URL para hoteles
        "hostal": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&dest_id=-384328&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&nflt=ht_id%3D216',  # URL para hostales/pensiones
        "albergue": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&dest_id=-384328&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&nflt=ht_id%3D203',  # URL para albergues
    },

    "Córdoba": {
        "hotel": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&checkin=2025-04-12&checkout=2025-04-13&dest_id=-378765&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D204',  # URL para hoteles
        "hostal": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&checkin=2025-04-12&checkout=2025-04-13&dest_id=-378765&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D216',  # URL para hostales/pensiones
        "albergue": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&checkin=2025-04-12&checkout=2025-04-13&dest_id=-378765&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D203',  # URL para albergues
    },

    "Málaga": {
        "hotel": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&checkin=2025-04-12&checkout=2025-04-13&dest_id=-390787&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D204',  # URL para hoteles
        "hostal": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&checkin=2025-04-12&checkout=2025-04-13&dest_id=-390787&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D216',  # URL para hostales/pensiones
        "albergue": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&checkin=2025-04-12&checkout=2025-04-13&dest_id=-390787&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D203',  # URL para albergues
    },

    "Barcelona": {
        "hotel": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&dest_id=-372490&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&nflt=ht_id%3D204',  # URL para hoteles
        "hostal": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&dest_id=-372490&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&nflt=ht_id%3D216',  # URL para hostales/pensiones
        "albergue": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&dest_id=-372490&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&nflt=ht_id%3D203',  # URL para albergues
    },

    "Valencia": {
        "hotel": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&dest_id=-406131&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&nflt=ht_id%3D204',  # URL para hoteles
        "hostal": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&dest_id=-406131&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&nflt=ht_id%3D216',  # URL para hostales/pensiones
        "albergue": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&dest_id=-406131&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&nflt=ht_id%3D203',  # URL para albergues
    },

    "Toledo": {
        "hotel": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&dest_id=-404357&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D204',  # URL para hoteles
        "hostal": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&dest_id=-404357&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D216',  # URL para hostales/pensiones
        "albergue": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&dest_id=-404357&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D203',  # URL para albergues
    },

    "Salamanca": {
        "hotel": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&dest_id=-400105&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D204',  # URL para hoteles
        "hostal": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&dest_id=-400105&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D216',  # URL para hostales/pensiones
        "albergue": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&dest_id=-400105&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D203',  # URL para albergues
    },

    "Bilbao": {
        "hotel": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&checkin=2025-04-12&checkout=2025-04-13&dest_id=-373608&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D204',  # URL para hoteles
        "hostal": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&checkin=2025-04-12&checkout=2025-04-13&dest_id=-373608&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D216',  # URL para hostales/pensiones
        "albergue": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&checkin=2025-04-12&checkout=2025-04-13&dest_id=-373608&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D203',  # URL para albergues
    },

    "Zaragoza": {
        "hotel": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&checkin=2025-04-12&checkout=2025-04-13&dest_id=-409149&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D204',  # URL para hoteles
        "hostal": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&checkin=2025-04-12&checkout=2025-04-13&dest_id=-409149&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D216',  # URL para hostales/pensiones
        "albergue": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&checkin=2025-04-12&checkout=2025-04-13&dest_id=-409149&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D203',  # URL para albergues
    },

    "Benidorm": {
        "hotel": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&checkin=2025-04-12&checkout=2025-04-13&dest_id=-373226&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D204',  # URL para hoteles
        "hostal": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&checkin=2025-04-12&checkout=2025-04-13&dest_id=-373226&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D216',  # URL para hostales/pensiones
        "albergue": 'https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AsDlz78GwAIB0gIkZjRmOTJhZWUtZTkwOC00NjZlLTg2NjgtNWNlNTZkMTNkNzY22AIF4AIB&sid=8eb0e60068c93b7156b24ed598dd28a4&aid=304142&checkin=2025-04-12&checkout=2025-04-13&dest_id=-373226&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null&nflt=ht_id%3D203'  # URL para albergues
    }
}

# Ruta al ejecutable de chromedriver
path = r'.\chromedriver-win64\chromedriver.exe'

hoteles = []
precios = []
camas = []
categorias = []
pois = []
comentarios_tabla = []

hotel_id = 1

for ciudad, tipos in urls.items():
    for tipo, url in tipos.items():
        print(f"Procesando {tipo} en {ciudad}...")

        service = configurar_servicio(path)
        driver = inicializar_navegador(service, url)

        # Espera a que cargue la lista principal
        div_padre = esperar_div_padre(driver, '//*[@id="bodyconstraint-inner"]/div/div/div[2]/div[3]/div[2]/div[2]/div[3]', 10)

        # Carga todos los resultados posibles antes de empezar
        cargar_mas_resultados(driver) # Comentar esta línea si solo quieres la muestra que usa la demo.

        # Ahora sí, obtén todos los hoteles visibles
        div_hijos = encontrar_div_hijos(driver)

        if div_hijos and len(div_hijos) > 0:
            for idx, div_hijo in enumerate(div_hijos):
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", div_hijo)
                    time.sleep(0.3)
                    imagen_div = div_hijo.find_element(By.XPATH, './/a[@data-testid="property-card-desktop-single-image"]')
                    driver.execute_script("arguments[0].click();", imagen_div)
                    time.sleep(2)
                    ventanas = driver.window_handles
                    if len(ventanas) > 1:
                        driver.switch_to.window(ventanas[1])

                        # Llama a la función para extraer el título y las estrellas
                        try:
                            nombre_estrellas = extraer_titulo_y_estrellas_csv(driver)
                            print(f"Hotel {idx+1} en {ciudad}: {nombre_estrellas}")
                        except Exception as e:
                            print(f"Error extrayendo título/estrellas en {ciudad}, hotel {idx+1}: {e}")
                            nombre_estrellas = []

                        # Llama a la función para extraer el precio y la fecha
                        try:
                            precios_fecha = extraer_precios_meses_csv(driver, num_pares_mensuales=6)
                        except Exception as e:
                            print(f"Error extrayendo precios/fechas en {ciudad}, hotel {idx+1}: {e}")
                            precios_fecha = []

                        # Llama a la función para extraer las opciones de las camas
                        try:
                            opciones_camas = extraer_camas_csv(driver)
                        except Exception as e:
                            print(f"Error extrayendo camas en {ciudad}, hotel {idx+1}: {e}")
                            opciones_camas = []
                            
                        # Llama a la función para extraer las categorías y sus notas
                        try:
                            time.sleep(2)
                            categorias_notas = extraer_categorias_notas_csv(driver)
                        except Exception as e:
                            print(f"Error extrayendo categorías/notas en {ciudad}, hotel {idx+1}: {e}")
                            categorias_notas = []

                        # Llama a la función para extraer los puntos de interés (POIs) y sus distancias
                        try:
                            pois_distancia = extraer_pois_csv(driver)
                        except Exception as e:
                            print(f"Error extrayendo POIs en {ciudad}, hotel {idx+1}: {e}")
                            pois_distancia = []

                        # Llama a la función para extraer los comentarios
                        try:
                            comentarios = extraer_comentarios_csv(driver, max_comentarios=10)
                        except Exception as e:
                            print(f"Error extrayendo comentarios en {ciudad}, hotel {idx+1}: {e}")
                            comentarios = []

                        driver.close()
                        driver.switch_to.window(ventanas[0])

                    time.sleep(1)  # Espera entre hoteles
                    hoteles.append({
                        "hotel_id": hotel_id,
                        "ciudad": ciudad,
                        "tipo": tipo,
                        "nombre": nombre_estrellas.get("titulo", ""),
                        "estrellas": nombre_estrellas.get("estrellas", "")
                    })

                    for p in precios_fecha:
                        precios.append({
                            "hotel_id": hotel_id,
                            "fecha": p.get("fecha", ""),
                            "precio": p.get("precio", "")
                        })

                    for c in opciones_camas:
                        camas.append({
                            "hotel_id": hotel_id,
                            "opcion_habitacion": c.get("opcion_habitacion", ""),
                            "camas": c.get("camas", "")
                        })

                    for cn in categorias_notas:
                        categorias.append({
                            "hotel_id": hotel_id,
                            "categoria": cn.get("categoria", ""),
                            "nota": cn.get("nota", "")
                        })

                    for poi in pois_distancia:
                        pois.append({
                            "hotel_id": hotel_id,
                            "seccion": poi.get("seccion", ""),
                            "poi": poi.get("poi", "")
                        })

                    for com in comentarios:
                        comentarios_tabla.append({
                            "hotel_id": hotel_id,
                            "comentario": com.get("comentario", "")
                        })

                    hotel_id += 1

                except Exception as e:
                    print(f"No se pudo procesar el hotel {idx+1} en {ciudad}: {e}")
        else:
            print(f"No se encontraron hoteles en {ciudad} para {tipo}.")


# Guardar cada tabla en su CSV
with open('hoteles.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["hotel_id", "ciudad", "tipo", "nombre", "estrellas"], delimiter=';')
    writer.writeheader()
    writer.writerows(hoteles)

with open('precios.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["hotel_id", "fecha", "precio"], delimiter=';')
    writer.writeheader()
    writer.writerows(precios)

with open('camas.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["hotel_id", "opcion_habitacion", "camas"], delimiter=';')
    writer.writeheader()
    writer.writerows(camas)

with open('categorias_notas.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["hotel_id", "categoria", "nota"], delimiter=';')
    writer.writeheader()
    writer.writerows(categorias)

with open('pois.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["hotel_id", "seccion", "poi"], delimiter=';')
    writer.writeheader()
    writer.writerows(pois)

with open('comentarios.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["hotel_id", "comentario"], delimiter=';')
    writer.writeheader()
    writer.writerows(comentarios_tabla)

