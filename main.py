import os
import xml.etree.ElementTree as ET
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN, ROUND_UP
from tkinter import Tk, filedialog

def recalcula_xml(infile: str, outfile: str = None):
    """Corrige importes e impuestos de un CFDI XML básico."""

    ET.register_namespace('cfdi', "http://www.sat.gob.mx/cfd/4")
    ET.register_namespace('cce20', "http://www.sat.gob.mx/ComercioExterior20")
    ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")

    tree = ET.parse(infile)
    root = tree.getroot()
    
    #print(root)

    # Namespace común del SAT
    ns = {"cfdi": "http://www.sat.gob.mx/cfd/4"}

    # Recalcular subtotales y totales

    comprobante = root

    subtotal = comprobante.attrib.get("SubTotal", "0.00")
    subtotal = Decimal(subtotal)
    Descuento = comprobante.attrib.get("Descuento", "0.00")
    Descuento = Decimal(Descuento)
    total_impuestos = Decimal("0.00")

    # Correccion de nodos impuestos en conceptos
    for impuestos in root.findall(".//cfdi:Concepto/cfdi:Impuestos", ns):
        if impuestos is not None:
            for traslado in impuestos.findall(".//cfdi:Traslado", ns):
                
                base_impuesto = Decimal(traslado.attrib.get("Base", "0")) - Decimal(traslado.attrib.get("Descuento", "0"))
                #print(f"🔍 Revisando traslado: Base={base_impuesto} TasaOCuota={traslado.attrib.get('TasaOCuota')} Importe={traslado.attrib.get('Importe')}")
                tasa_impuesto = Decimal(traslado.attrib.get("TasaOCuota", "0"))
                impuesto_importe = Decimal(traslado.attrib.get("Importe", "0"))
                limite_inferior = ((base_impuesto - Decimal(10 ** -2/2)) * tasa_impuesto).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
                limite_superior = ((base_impuesto + Decimal(10 ** -2/2) - Decimal(10 ** -12)) * tasa_impuesto).quantize(Decimal("0.01"), rounding=ROUND_UP)
                if not(limite_inferior <= impuesto_importe <= limite_superior):
                    dif_inferior = abs(impuesto_importe - limite_inferior)
                    dif_superior = abs(impuesto_importe - limite_superior)
                    if dif_inferior < dif_superior:
                        importe_calc = limite_inferior
                    else:
                         importe_calc = limite_superior
                    print(traslado.attrib)
                    print(f"  ⚠️ Importe de impuesto corregido de {impuesto_importe} a {importe_calc} {limite_inferior} - {limite_superior}")
                    traslado.set("Importe", str(importe_calc))
                    impuesto_importe = importe_calc
                total_impuestos += impuesto_importe
    

    # Asignar nuevos valores al nodo de impuestos globales
    impuestos_global = root.find("cfdi:Impuestos", ns)

    if impuestos_global is not None:
        print(f"🧮 Actualizando TotalImpuestosTrasladados: {impuestos_global.attrib.get('TotalImpuestosTrasladados')} → {total_impuestos}")
        impuestos_global.set("TotalImpuestosTrasladados", str(total_impuestos.quantize(Decimal("0.01"))))
        for traslado in impuestos_global.findall(".//cfdi:Traslado", ns):
            traslado.set("Importe", str(total_impuestos.quantize(Decimal("0.01"))))

    total = (subtotal + total_impuestos - Descuento).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


    # Asignar nuevos valores al nodo principal (Comprobante)
    comprobante.set("Total", str(total))

    # Archivo de salida
    if not outfile:
        base, ext = os.path.splitext(infile)
        outfile = f"{base}_corregido{ext}"

    tree.write(outfile, encoding="UTF-8", xml_declaration=True)
    print(f"✅ Archivo corregido guardado como: {outfile}")



if __name__ == "__main__":
    # Oculta la ventana principal de tkinter
    Tk().withdraw()

    # Abre el explorador de archivos para seleccionar el XML
    xml_path = filedialog.askopenfilename(
        title="Selecciona el XML de factura a corregir",
        filetypes=[("Archivos XML", "*.xml")]
    )

    if xml_path:
        recalcula_xml(xml_path)
    else:
        print("⚠️ No se seleccionó ningún archivo.")
