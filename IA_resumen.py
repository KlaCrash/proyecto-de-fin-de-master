import csv
import re
import heapq
from collections import Counter

# Lista básica de stopwords en español (puedes ampliarla)
STOPWORDS = set([
    'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'y', 'o', 'pero', 'de', 'del', 'en', 'con', 'por', 'para', 'es', 'muy', 'lo', 'al', 'a', 'que', 'se', 'su', 'mi', 'tu', 'sus', 'mis', 'tus'
])

def limpiar_palabra(p):
    return p.lower()

def resumir_comentario(texto, num_frases=2):
    texto = re.sub(r'\s+', ' ', texto)
    frases = re.split(r'(?<=[.!?]) +', texto)
    palabras = [limpiar_palabra(p) for p in re.findall(r'\w+', texto.lower()) if limpiar_palabra(p) not in STOPWORDS]
    frecuencia = Counter(palabras)

    puntuaciones = {}
    for i, frase in enumerate(frases):
        frase_palabras = [limpiar_palabra(p) for p in re.findall(r'\w+', frase.lower()) if limpiar_palabra(p) not in STOPWORDS]
        # Pondera la primera y última frase
        extra = 1 if i == 0 or i == len(frases)-1 else 0
        puntuaciones[frase] = sum(frecuencia.get(p, 0) for p in frase_palabras) + extra

    frases_resumen = heapq.nlargest(num_frases, puntuaciones, key=puntuaciones.get)
    resumen = ' '.join(frases_resumen)
    return resumen

# Leer y resumir comentarios, guardando el resultado
with open('comentarios.csv', newline='', encoding='utf-8') as f_in, \
     open('comentarios_resumidos.csv', 'w', newline='', encoding='utf-8') as f_out:
    reader = csv.DictReader(f_in, delimiter=';')
    fieldnames = ['hotel_id', 'resumen']
    writer = csv.DictWriter(f_out, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()

    for row in reader:
        resumen = resumir_comentario(row['comentario'], num_frases=2)
        writer.writerow({'hotel_id': row['hotel_id'], 'resumen': resumen})
