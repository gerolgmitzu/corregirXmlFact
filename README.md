# Corregir XML Facturas

Este proyecto es una herramienta en Python para corregir los importes de impuestos y totales en archivos XML de facturas CFDI (Comprobante Fiscal Digital por Internet) de México.

## Descripción

El script `main.py` analiza un archivo XML de factura CFDI, recalcula los impuestos trasladados basándose en las bases y tasas correctas, y ajusta el total del comprobante. Esto es útil para corregir errores en los cálculos de impuestos que puedan ocurrir en la generación automática de facturas.

## Requisitos

- Python 3.10 o superior
- No se requieren bibliotecas externas adicionales (utiliza solo la biblioteca estándar de Python)

## Instalación

1. Clona este repositorio:
   ```
   git clone https://github.com/gerolgmitzu/corregirXmlFact.git
   cd corregirXmlFact
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```
   python -m venv env
   # En Windows:
   env\Scripts\activate
   # En Linux/Mac:
   source env/bin/activate
   ```

3. Instala las dependencias (si hay alguna):
   ```
   pip install -r requirements.txt
   ```

## Creación de Ejecutable (Opcional)

Para crear un ejecutable independiente que no requiera Python instalado:

1. Instala PyInstaller:
   ```
   pip install pyinstaller
   ```

2. Crea el ejecutable:
   ```
   pyinstaller --onefile --windowed main.py
   ```

   El ejecutable `main.exe` se creará en la carpeta `dist/`.

## Uso

Ejecuta el script principal:

```
python main.py
```

O, si estás en Windows, puedes hacer doble clic en `run.bat` para ejecutar el script sin necesidad de abrir un editor de código.

Si has creado el ejecutable con PyInstaller, simplemente ejecuta `dist/main.exe` (o distribúyelo como un archivo independiente).

Se abrirá un diálogo para seleccionar el archivo XML de la factura a corregir. El script procesará el archivo y guardará una versión corregida con el sufijo "_corregido.xml" en el mismo directorio.

## Funcionalidades

- Recalcula impuestos trasladados en conceptos individuales
- Ajusta el total de impuestos trasladados globales
- Corrige el total del comprobante
- Maneja redondeos precisos según las reglas del SAT

## Licencia

Ver archivo LICENSE para detalles.