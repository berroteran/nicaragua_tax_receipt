## Nicaragua Tax Receipt

App reusable para Frappe / ERPNext 15 que agrega control de comprobantes
oficiales sobre retenciones aplicadas en `Payment Entry` a partir de
`Purchase Taxes and Charges Template`, y que ademas versiona campos utiles para
impresion y operacion como `concepto` en `Payment Entry` e `impresion_cheque`
en `Supplier`.

## Objetivo de negocio

En muchos flujos contables y fiscales de Nicaragua, cuando un pago aplica
retenciones de impuestos, no basta con calcular el monto retenido. Tambien se
necesita registrar el numero de comprobante oficial asociado a esa retencion
para fines de:

- control interno
- auditoria
- conciliacion documental
- trazabilidad por pago
- reportes fiscales y administrativos

ERPNext maneja bien la aplicacion de plantillas de impuestos y la generacion de
las filas de retencion en `Payment Entry`, pero no trae de base un mecanismo
especifico para exigir y persistir ese numero de comprobante oficial como parte
del flujo.

Esta app existe para cerrar esa brecha sin modificar el core de ERPNext.

## Razon de existencia

La necesidad funcional que resuelve es esta:

- una `Purchase Taxes and Charges Template` define la estructura de retencion
- al aplicarla en `Payment Entry`, ERPNext copia las filas a
  `Advance Taxes and Charges`
- cada fila de retencion puede necesitar su propio numero de comprobante oficial
- ese numero debe quedar visible, buscable y reportable dentro del sistema

La app separa correctamente:

- la regla reusable por fila de plantilla
- el dato transaccional propio de cada fila aplicada en el pago
- la trazabilidad detallada de cada fila de retencion

## Aporte funcional

La app agrega un comportamiento instalable y versionable por Git para que el
comprobante oficial pase a ser parte del sistema y no una nota externa o un
dato manual disperso.

Con esto se logra:

- definir por fila de impuesto si esa retencion exige comprobante oficial
- capturar un numero de comprobante por cada fila de retencion en el pago
- validarlo tambien en servidor, no solo en la interfaz
- dejar el dato disponible para filtros, busquedas y reportes
- versionar por Git campos manuales de uso frecuente para pagos y cheques sin
  romper sitios que ya los tengan creados

## Features

- Campo de configuracion por fila en `Purchase Taxes and Charges`:
  `custom_require_official_receipt_no`
- Campo reusable en `Payment Entry` para concepto del pago:
  `concepto`
- Campo reusable en `Supplier` para texto de impresion en cheque:
  `impresion_cheque`
- Campo de trazabilidad en `Advance Taxes and Charges`:
  `custom_official_receipt_no`
- Campo espejo en `Advance Taxes and Charges`:
  `custom_require_official_receipt_no`
- Validacion backend por fila cuando una retencion requiere comprobante
- Copia del check desde la plantilla al `Payment Entry` usando el flujo nativo
  de ERPNext al traer impuestos desde plantilla
- Campo `concepto` en `Payment Entry` listo para filtros, busqueda, reportes,
  impresiones y formatos de cheque
- Campo `impresion_cheque` en `Supplier` para formatos de impresion de cheque
- Politica conservadora para campos funcionales ya existentes en algunos sitios:
  si ya existen, la app no los reemplaza ni toca sus datos
- App desacoplada del core de ERPNext

## Modelo funcional

### 1. Plantilla

La plantilla no guarda el numero de comprobante real de cada pago.
La plantilla guarda la regla por cada fila de impuesto:

- esta fila requiere comprobante oficial
- esta fila no lo requiere

### 2. Payment Entry

El `Payment Entry` recibe las filas de impuestos desde la plantilla y cada fila
puede llevar:

- `custom_require_official_receipt_no`
- `custom_official_receipt_no`

Ademas, el `Payment Entry` puede exponer un campo funcional reutilizable:

- `concepto`

Ese campo sirve para:

- busqueda
- filtros
- reportes del pago
- print formats
- formatos de cheque
- consultas operativas

### 3. Filas de retencion

Cada fila de `Advance Taxes and Charges` recibe su propia regla y su propio
numero de comprobante.

Esto permite trazabilidad detallada por retencion individual, por ejemplo:

- 2% IR en la fuente
- 1% IR en la fuente

Cada una puede exigir y guardar un comprobante distinto si el caso de negocio lo
requiere.

### 4. Supplier

El `Supplier` puede exponer un campo funcional reutilizable:

- `impresion_cheque`

Su objetivo principal es servir a impresiones y formatos de cheque.

## Por que la regla vive por fila y no en el encabezado

En este caso la obligatoriedad del comprobante no pertenece al documento padre,
sino a cada impuesto de la plantilla.

Eso permite que:

- una fila de retencion exija comprobante
- otra fila no lo exija
- varias filas guarden numeros distintos
- la trazabilidad y validacion sean coherentes con cada impuesto aplicado

## Alcance actual

La version actual implementa el flujo para:

- `Purchase Taxes and Charges`
- `Payment Entry`
- `Advance Taxes and Charges`
- `Supplier`

En particular, esta orientada al escenario donde el pago aplica impuestos de
compra / retenciones a proveedores y donde se requieren campos auxiliares para
impresion y documentacion operativa.

## Arquitectura tecnica

### Hooks

- `doctype_js["Payment Entry"]`
- `doc_events["Payment Entry"]["validate"]`

### Componentes

- `nicaragua_tax_receipt/hooks.py`
  registra hooks de frontend y backend
- `nicaragua_tax_receipt/tax_receipt.py`
  valida el comprobante por fila en servidor
- `nicaragua_tax_receipt/public/js/payment_entry.js`
  expone en la grilla de impuestos los campos por fila
- `nicaragua_tax_receipt/patches/v1_0/add_tax_receipt_custom_fields.py`
  crea los campos de retencion por fila y oculta los campos viejos del enfoque
  por encabezado
- `nicaragua_tax_receipt/patches/v1_1/add_payment_entry_concept_field.py`
  adopta o crea `Payment Entry.concepto`
- `nicaragua_tax_receipt/patches/v1_1/add_supplier_check_print_field.py`
  crea `Supplier.impresion_cheque` si el sitio no lo tiene

## Flujo de usuario

1. El usuario define o edita una `Purchase Taxes and Charges Template`.
2. Marca por fila si esa retencion requiere comprobante oficial.
3. En un `Payment Entry`, selecciona la plantilla de impuestos.
4. ERPNext copia las filas al detalle `Advance Taxes and Charges`.
5. Cada fila requerida debe recibir su propio `Official Receipt No`.
6. El servidor valida que no se pueda guardar vacio en las filas obligatorias.
7. El usuario puede usar `concepto` en el pago para impresiones, reportes y
   formatos de cheque.
8. El proveedor puede usar `impresion_cheque` en formatos de impresion.

## Beneficios

- mejora control fiscal y documental
- evita omisiones manuales
- reduce dependencia de notas libres o archivos externos
- hace el dato consultable dentro de ERPNext
- permite transportar la solucion entre instancias por Git
- evita tocar `erpnext` core

## Instalacion

### En un bench existente

```bash
cd /home/frappe/frappe-bench
bench get-app <URL_DEL_REPO>
bench --site <SITIO> install-app nicaragua_tax_receipt
bench --site <SITIO> migrate
bench build --app nicaragua_tax_receipt
bench clear-cache
```

### Ejemplo en este servidor

```bash
sudo -u frappe bash -lc '
cd /home/frappe/frappe-bench &&
bench --site testing15.inversionesbel.com install-app nicaragua_tax_receipt &&
bench --site testing15.inversionesbel.com migrate &&
bench build --app nicaragua_tax_receipt &&
bench --site testing15.inversionesbel.com clear-cache
'
```

## Versionado y despliegue

La app esta pensada para administrarse como repositorio Git independiente.

Esto permite:

- promover cambios por ramas y pull requests
- instalar la misma solucion en varios sitios ERPNext
- mantener historial de cambios funcionales y tecnicos
- desplegar fixes y mejoras sin tocar el core

## Politica de compatibilidad con sitios existentes

La app usa dos estrategias distintas:

### Campos propios de la app

Para los campos de retencion de esta app, el patch puede crearlos o ajustarlos
porque forman parte del comportamiento funcional esperado del modulo.

### Campos funcionales que algunos sitios ya tienen manualmente

Para estos campos la politica es conservadora:

- `Payment Entry.concepto`
- `Supplier.impresion_cheque`

La regla es:

- si el campo no existe, la app lo crea
- si el campo ya existe, la app lo ignora
- no se borran datos existentes
- no se renombran campos existentes

Esto permite instalar la app en sitios heterogeneos sin perder informacion ni
romper personalizaciones previas.

## Consideraciones

- La app crea `Custom Fields` por patch, no tocando DocTypes core.
- La validacion principal corre en servidor para evitar saltos por API o import.
- El comportamiento visual corre en cliente para mejorar la experiencia.
- Los labels actuales estan en ingles tecnico; pueden adaptarse a espanol si
  se desea estandarizar la experiencia de usuario.

## Posibles mejoras futuras

- traducciones formales `es`
- reportes listos para retenciones con comprobante
- print formats que muestren el comprobante oficial
- soporte para mas tipos de documentos fiscales relacionados
- naming y labels mas orientados a normativa local

## Desarrollo

Esta app usa el flujo normal de apps Frappe.

Herramientas de calidad presentes en el scaffold:

- `pre-commit`
- `ruff`
- `eslint`
- `prettier`
- `pyupgrade`

## Licencia

`mit`
