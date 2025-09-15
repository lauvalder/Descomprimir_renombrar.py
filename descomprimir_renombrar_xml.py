import os
import zipfile
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox

# Función para extraer datos del XML
def extraer_datos_xml(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        ns = {
            'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
            'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'
        }

        nit = root.findtext('cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID', namespaces=ns)
        razon_social = root.findtext('cac:AccountingSupplierParty/cac:Party/cac:PartyName/cbc:Name', namespaces=ns)
        numero = root.findtext('cbc:ID', namespaces=ns)
        fecha = root.findtext('cbc:IssueDate', namespaces=ns)

        return nit, razon_social, numero, fecha
    except Exception as e:
        print(f"Error al procesar {xml_path}: {e}")
        return None, None, None, None

# Función para descomprimir y renombrar
def procesar_zip_en_carpeta(carpeta_zip, carpeta_salida):
    for archivo in os.listdir(carpeta_zip):
        if archivo.endswith(".zip"):
            zip_path = os.path.join(carpeta_zip, archivo)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for nombre_archivo in zip_ref.namelist():
                    if nombre_archivo.endswith(".xml"):
                        zip_ref.extract(nombre_archivo, carpeta_salida)
                        xml_path = os.path.join(carpeta_salida, nombre_archivo)
                        nit, razon_social, numero, fecha = extraer_datos_xml(xml_path)
                        if nit and razon_social and numero and fecha:
                            nuevo_nombre = f"{nit}_{razon_social}_{numero}_{fecha}.xml"
                            nuevo_path = os.path.join(carpeta_salida, nuevo_nombre)
                            os.rename(xml_path, nuevo_path)
                            print(f"✅ Renombrado: {nuevo_nombre}")
                        else:
                            print(f"⚠️ No se pudo extraer datos de {nombre_archivo}")

# Interfaz para seleccionar carpeta ZIP y carpeta de salida
def seleccionar_carpetas_y_procesar():
    root = tk.Tk()
    root.withdraw()

    carpeta_zip = filedialog.askdirectory(title="Selecciona la carpeta con archivos ZIP")
    if not carpeta_zip:
        messagebox.showwarning("Cancelado", "No se seleccionó la carpeta de ZIP.")
        return

    carpeta_salida = filedialog.askdirectory(title="Selecciona la carpeta de salida para los XML renombrados")
    if not carpeta_salida:
        messagebox.showwarning("Cancelado", "No se seleccionó la carpeta de salida.")
        return

    os.makedirs(carpeta_salida, exist_ok=True)
    procesar_zip_en_carpeta(carpeta_zip, carpeta_salida)
    messagebox.showinfo("Proceso completado", f"Los XML renombrados están en:\n{carpeta_salida}")

# Ejecutar
seleccionar_carpetas_y_procesar()
