import time
import re
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def configurar_servicio(path):
    """
    Configura el servicio para el controlador de Chrome.

    :param path: Ruta al ejecutable de chromedriver.
    :return: Instancia del servicio configurado.
    """
    return Service(path)

def inicializar_navegador(service, url):
    """
    Inicializa el navegador y carga la URL especificada.

    :param service: Instancia del servicio de Selenium (chromedriver).
    :param url: URL que se desea cargar en el navegador.
    :return: Instancia del navegador Selenium.
    """
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    return driver

def cargar_mas_resultados(driver):
    """
    Hace scroll y pulsa el botón "Cargar más resultados" si existe.
    Repite hasta que no haya más.
    """
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Espera para que cargue el botón
            boton_cargar_mas = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    '//button[span[contains(text(), "Cargar más resultados")]]'
                ))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", boton_cargar_mas)
            time.sleep(0.5)
            boton_cargar_mas.click()
            print("Botón 'Cargar más resultados' pulsado.")
            time.sleep(2)  # Espera para que se carguen los nuevos hoteles
        except Exception as e:
            print("No hay más resultados para cargar o no se encontró el botón.")
            break

def esperar_div_padre(driver, xpath, timeout=10):
    """
    Espera hasta que un elemento esté presente en el DOM.

    :param driver: Instancia del navegador Selenium.
    :param xpath: XPath del elemento a esperar.
    :param timeout: Tiempo máximo de espera en segundos (por defecto 10).
    :return: El elemento encontrado o None si no se encuentra.
    """
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    except TimeoutException:
        print(f"El elemento con XPath '{xpath}' no se encontró en {timeout} segundos.")
        return None

def encontrar_div_hijos(driver, xpath='.//div[@data-testid="property-card"]'):
    """
    Encuentra todos los div hijos con el atributo data-testid="property-card".

    :param driver: Instancia del navegador Selenium.
    :param xpath: XPath para encontrar los div hijos (por defecto busca property-card).
    :return: Lista de elementos WebElement encontrados.
    """
    try:
        return driver.find_elements(By.XPATH, xpath)
    except Exception as e:
        print(f"Error al encontrar los div hijos: {e}")
        return []

def extraer_titulo_y_estrellas_csv(driver):
    """
    Extrae el título del hotel y el número de estrellas oficiales (0-5).
    Devuelve un diccionario con las claves 'titulo' y 'estrellas'.
    Si no hay título, devuelve None.
    """
    try:
        titulo_hotel = driver.find_element(By.XPATH, '//h2[contains(@class, "pp-header__title")]').text.strip()
    except Exception as e:
        print("No se pudo extraer el título del hotel:", e)
        return None

    try:
        time.sleep(0.5)  # Espera extra para asegurar carga
        estrellas_elem = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-testid="quality-rating"]'))
        )
        estrellas_label = estrellas_elem.get_attribute("aria-label").strip()
        match = re.search(r'(\d+)', estrellas_label)
        estrellas = int(match.group(1)) if match else 0
    except Exception as e:
        estrellas = 0
        print("No se pudo extraer la cantidad de estrellas:", e)

    return {"titulo": titulo_hotel, "estrellas": estrellas}

def extraer_precios_meses_csv(driver, num_pares_mensuales=6):
    """
    Extrae los precios por día de los próximos meses visibles en el calendario.
    Devuelve una lista de diccionarios con las claves 'fecha' y 'precio'.
    """
    fechas_vistas = set()
    dias_precios = []

    try:
        for intento in range(2):  # Intenta dos veces por si hay stale element
            try:
                boton_calendario = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '(//button[@data-testid="date-display-field-start"])[1]'))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", boton_calendario)
                time.sleep(1)
                boton_calendario.click()
                time.sleep(2)
                break  # Si funciona, sal del bucle
            except Exception as e:
                if "stale element reference" in str(e):
                    time.sleep(1)
                    continue
                else:
                    raise e
    except Exception as e:
        print("No se pudo abrir el calendario:", e)
        return []

    for i in range(num_pares_mensuales):
        celdas = driver.find_elements(By.XPATH, '//span[contains(@class, "ecb788f3b7 c0b8f1e8f8 d5dcd44e2b")]')
        print(f"Detectadas {len(celdas)} celdas de días con precios en la vista {i+1}.")

        for celda in driver.find_elements(By.XPATH, '//span[contains(@class, "ecb788f3b7")]'):
            try:
                fecha = celda.get_attribute("data-date")
                if not fecha or fecha in fechas_vistas:
                    continue
                fechas_vistas.add(fecha)
                try:
                    precio_elem = celda.find_element(By.XPATH, './/span[contains(@class, "e7362e5f34")]')
                    precio_texto = precio_elem.text.strip().replace('\xa0', '').replace('€', '').replace(',', '.')
                    precio = f"{float(precio_texto):.2f}" if precio_texto else ""
                except Exception:
                    precio = ""
                dias_precios.append({"fecha": fecha, "precio": precio})
            except Exception:
                continue
        for _ in range(2):
            try:
                boton_siguiente = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Mes siquiente"]'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_siguiente)
                time.sleep(0.5)
                primer_dia = None
                try:
                    primer_dia_elem = driver.find_element(By.XPATH, '(//span[contains(@class, "ecb788f3b7") and @data-date])[1]')
                    primer_dia = primer_dia_elem.get_attribute("data-date")
                except Exception:
                    pass
                boton_siguiente.click()
                time.sleep(1.5)
                if primer_dia:
                    WebDriverWait(driver, 10).until(
                        lambda d: d.find_element(By.XPATH, '(//span[contains(@class, "ecb788f3b7") and @data-date])[1]').get_attribute("data-date") != primer_dia
                    )
                time.sleep(0.5)
            except Exception as e:
                print("No se pudo avanzar al siguiente mes:", e)
                return dias_precios

    return dias_precios

def extraer_camas_csv(driver):
    """
    Extrae la información de camas de la pestaña actual del hotel.
    Devuelve una lista de diccionarios, cada uno con una opción de habitación y sus tipos de cama.
    """
    camas_info = []
    try:
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(1)
        filas_camas = driver.find_elements(By.XPATH, '//tr[contains(@class, "b7e718a9ac")]')
        for idx, fila in enumerate(filas_camas[1:], start=1):  # Saltar el primer <tr>
            camas_fila = []
            try:
                span_camas = fila.find_elements(By.XPATH, './/span[contains(@class, "d7a50099f7")]')
                for span in span_camas:
                    texto_cama = span.text.strip()
                    if texto_cama:
                        camas_fila.append(texto_cama)
                if camas_fila:
                    camas_info.append({
                        "opcion_habitacion": idx,
                        "camas": ", ".join(camas_fila)
                    })
                    print(f"Opción de habitación {idx}: {', '.join(camas_fila)}")
            except Exception:
                continue
    except Exception as e:
        print("Error extrayendo camas:", e)
    return camas_info

def extraer_categorias_notas_csv(driver):
    """
    Extrae las categorías y notas de un hotel abierto en una ventana.
    Devuelve una lista de diccionarios con las claves 'categoria' y 'nota'.
    """
    categorias_notas = []
    try:
        div_padre = driver.find_element(By.XPATH, '//div[@role="group" and @aria-label="Categorías de los comentarios"]')
    except Exception:
        print("No se encontró el div padre de categorías")
        return categorias_notas

    try:
        divs_hijos = div_padre.find_elements(By.XPATH, './/div[@data-testid="review-subscore"]')
        for div_hijo in divs_hijos:
            # Extrae la categoría
            try:
                span_categoria = div_hijo.find_element(By.XPATH, './/span[contains(@class, "d96a4619c0")]')
                categoria = span_categoria.text.strip()
            except Exception:
                categoria = ""
            # Extrae la nota
            nota = ""
            try:
                div_nota = div_hijo.find_element(By.XPATH, './/div[contains(@class, "a9918d47bf") and @aria-hidden="true"]')
                nota = div_nota.text.strip()
            except Exception:
                try:
                    div_nota = div_hijo.find_element(By.XPATH, 'following-sibling::div[contains(@class, "ca9d921c46")]/div[contains(@class, "a9918d47bf") and @aria-hidden="true"]')
                    nota = div_nota.text.strip()
                except Exception:
                    nota = ""
            categorias_notas.append({"categoria": categoria, "nota": nota})
    except Exception:
        print("Error al extraer categorías y notas")
    return categorias_notas

def extraer_pois_csv(driver):
    """
    Extrae los puntos de interés (POI) de la pestaña actual y los devuelve en formato lista de diccionarios.
    Cada diccionario tiene las claves 'seccion' y 'poi'.
    """
    poi_csv = []
    try:
        # Espera hasta que al menos un bloque esté presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-testid="poi-block"]'))
        )
        # Encuentra todos los bloques hijos POI
        bloques_poi = driver.find_elements(By.XPATH, '//div[@data-testid="poi-block"]')
        for bloque in bloques_poi:
            # Extrae el título de la sección (puede estar en un <div> o <h3>)
            try:
                titulo = bloque.find_element(By.XPATH, './/div[contains(@class, "e7addce19e")]').text.strip()
            except:
                try:
                    titulo = bloque.find_element(By.XPATH, './/h3').text.strip()
                except:
                    titulo = ""
            # Extrae los elementos <li> (POIs) de la sección
            items = bloque.find_elements(By.XPATH, './/li')
            for item in items:
                texto_poi = item.text.strip()
                if texto_poi:
                    poi_csv.append({"seccion": titulo, "poi": texto_poi})
    except Exception as e:
        print("No se encontraron bloques POI:", e)
    return poi_csv

def extraer_comentarios_csv(driver, max_comentarios=10):
    """
    Extrae hasta max_comentarios de Booking y los devuelve como lista de diccionarios.
    Cada diccionario tiene la clave 'comentario'.
    """
    comentarios_extraidos = 0
    comentarios = []

    while comentarios_extraidos < max_comentarios:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="featuredreview-text"]'))
            )
            comentarios_en_pagina = driver.find_elements(By.XPATH, '//div[@data-testid="featuredreview-text"]')
            for div in comentarios_en_pagina:
                try:
                    spans = div.find_elements(By.XPATH, './/span')
                    texto = ""
                    for s in spans:
                        t = s.text.strip()
                        if t and t != '"' and len(t) > 2:
                            texto = t
                            break
                    if texto and texto not in [c["comentario"] for c in comentarios]:
                        comentarios.append({"comentario": texto})
                        comentarios_extraidos += 1
                        if comentarios_extraidos >= max_comentarios:
                            break
                except Exception:
                    continue
            # Intenta pulsar el botón "Siguiente"
            boton_siguiente = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Siguiente" and @type="button"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", boton_siguiente)
            boton_siguiente.click()
            time.sleep(1)
        except Exception:
            break

    return comentarios
