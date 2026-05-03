from django.shortcuts import render, redirect
from django.contrib import messages
from database import DatabaseManager
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
from matplotlib.ticker import MaxNLocator
import base64
import io


def _get_db():
    """Devuelve una instancia de DatabaseManager apuntando a la BD del proyecto."""
    return DatabaseManager('videoteca.db')


def coleccion(request):
    """Muestra todos los videojuegos agrupados por plataforma."""
    db = _get_db()
    registros = db.obtener_coleccion_completa()
    db.conn.close()
    return render(request, 'catalogo/coleccion.html', {'registros': registros})


def añadir_juego(request):
    """Muestra el formulario (GET) o procesa el alta de un juego (POST)."""
    if request.method == 'POST':
        titulo     = request.POST.get('titulo', '').strip()
        plataforma = request.POST.get('plataforma', '').strip()
        anio       = request.POST.get('anio', '').strip()
        genero     = request.POST.get('genero', '').strip()
        tipo       = request.POST.get('tipo', 'Físico')
        extra      = request.POST.get('extra', '').strip()

        if not all([titulo, plataforma, anio, genero, extra]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'catalogo/formulario_juego.html',
                          {'accion': 'Añadir', 'datos': request.POST})

        if not anio.isdigit():
            messages.error(request, 'El año debe ser un número entero.')
            return render(request, 'catalogo/formulario_juego.html',
                          {'accion': 'Añadir', 'datos': request.POST})

        try:
            db = _get_db()
            db.insertar_juego(titulo, plataforma, int(anio), genero, tipo, extra)
            db.conn.close()
            messages.success(request, f'"{titulo}" añadido correctamente.')
            return redirect('coleccion')
        except ValueError as e:
            messages.error(request, str(e))

    return render(request, 'catalogo/formulario_juego.html', {'accion': 'Añadir'})


def editar_juego(request, id_juego):
    """Muestra el formulario con datos actuales (GET) o guarda cambios (POST)."""
    db = _get_db()
    registros = db.obtener_coleccion_completa()
    juego = next((r for r in registros if r[0] == id_juego), None)

    if juego is None:
        db.conn.close()
        messages.error(request, 'Videojuego no encontrado.')
        return redirect('coleccion')

    if request.method == 'POST':
        titulo     = request.POST.get('titulo', '').strip()
        plataforma = request.POST.get('plataforma', '').strip()
        anio       = request.POST.get('anio', '').strip()
        genero     = request.POST.get('genero', '').strip()
        extra      = request.POST.get('extra', '').strip()

        if not all([titulo, plataforma, anio, genero, extra]):
            messages.error(request, 'Todos los campos son obligatorios.')
        elif not anio.isdigit():
            messages.error(request, 'El año debe ser un número entero.')
        else:
            try:
                db.editar_juego(id_juego, titulo, plataforma, int(anio), genero, extra)
                db.conn.close()
                messages.success(request, f'"{titulo}" actualizado correctamente.')
                return redirect('coleccion')
            except ValueError as e:
                messages.error(request, str(e))

    db.conn.close()
    return render(request, 'catalogo/formulario_juego.html', {
        'accion': 'Editar',
        'juego': juego,
    })


def eliminar_juego(request, id_juego):
    """Pide confirmación (GET) o ejecuta el borrado (POST)."""
    db = _get_db()
    registros = db.obtener_coleccion_completa()
    juego = next((r for r in registros if r[0] == id_juego), None)

    if juego is None:
        db.conn.close()
        messages.error(request, 'Videojuego no encontrado.')
        return redirect('coleccion')

    if request.method == 'POST':
        db.eliminar_juego(id_juego)
        db.conn.close()
        messages.success(request, f'"{juego[1]}" eliminado correctamente.')
        return redirect('coleccion')

    db.conn.close()
    return render(request, 'catalogo/confirmar_borrado.html', {'juego': juego})


def prestar_juego(request, id_juego):
    """Registra el préstamo de un juego a una persona."""
    if request.method == 'POST':
        destinatario = request.POST.get('destinatario', '').strip()
        if not destinatario:
            messages.error(request, 'El nombre del prestatario no puede estar vacío.')
        else:
            db = _get_db()
            db.registrar_prestamo(id_juego, destinatario)
            db.conn.close()
            messages.success(request, f'Préstamo registrado a "{destinatario}".')
        return redirect('coleccion')

    return render(request, 'catalogo/formulario_prestamo.html',
                  {'id_juego': id_juego})


def devolver_juego(request, id_juego):
    """Registra la devolución de un juego prestado."""
    db = _get_db()
    db.eliminar_prestamo(id_juego)
    db.conn.close()
    messages.success(request, 'Devolución registrada correctamente.')
    return redirect('coleccion')


def analisis(request):
    """Genera las tres gráficas EDA y las incrusta en la página como imágenes."""
    conn = sqlite3.connect('videoteca.db')
    df = pd.read_sql_query("SELECT plataforma, anio, genero FROM juegos", conn)
    conn.close()

    df = df.dropna(subset=['plataforma', 'anio', 'genero'])
    df['plataforma'] = df['plataforma'].str.strip()
    df['genero']     = df['genero'].str.strip()
    df['anio']       = df['anio'].astype(int)

    grafica_b64 = None

    if not df.empty:
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
        fig.suptitle('Análisis de la Colección', fontsize=14)

        conteo = df['plataforma'].value_counts()
        conteo.plot(kind='bar', ax=ax1, color='skyblue')
        ax1.set_title('Juegos por plataforma')
        ax1.set_xlabel('Plataforma')
        ax1.set_ylabel('Número de juegos')
        ax1.tick_params(axis='x', rotation=45)
        ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

        temporal = df.groupby('anio').size().cumsum()
        temporal.plot(kind='line', ax=ax2, marker='o', color='green')
        ax2.set_title('Evolución de la colección')
        ax2.set_xlabel('Año')
        ax2.set_ylabel('Total acumulado')
        ax2.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=10))
        ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

        ax3.scatter(df['anio'], df['genero'], alpha=0.6, color='purple')
        ax3.set_title('Correlación género / lanzamiento')
        ax3.set_xlabel('Año')
        ax3.tick_params(axis='y', labelsize=8)

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        grafica_b64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close(fig)

    return render(request, 'catalogo/analisis.html', {'grafica': grafica_b64})
