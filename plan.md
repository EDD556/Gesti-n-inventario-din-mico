
# Plan de Sistema de Consulta de Existencias

## Fase 1: Estructura Base y Consulta de Existencias ✅
- [x] Crear esquema de base de datos en Supabase (tablas: inventarios, familias_especiales)
- [x] Implementar página principal de consulta con filtros (SKU, familia, fecha)
- [x] Mostrar existencias de manera amigable con cards/tabla
- [x] Selector de fecha con valor por defecto (día actual)
- [x] Integración con Supabase para consultas

---

## Fase 2: Gestión de Excel y Actualización de Datos ✅
- [x] Crear funcionalidad para subir archivo Excel
- [x] Procesar Excel (pandas) y validar estructura (SKU, descripción, familia, existencia)
- [x] Guardar datos en Supabase con fecha actual
- [x] Opción para actualizar Excel del día (sobrescribir)
- [x] Feedback visual del proceso de carga

---

## Fase 3: Configuración y Familias Especiales
- [ ] Crear página de Configuración (visible solo en desktop)
- [ ] Mover opción de subir Excel a Configuración
- [ ] Implementar CRUD de familias especiales
- [ ] Agregar SKUs a familias especiales (múltiples SKUs por familia)
- [ ] Integrar filtro de familias especiales en página principal
- [ ] Navegación responsive (menú lateral/hamburguesa)

---

## Notas
- Base de datos: Supabase
- UI/UX: Intuitiva, amigable, responsive
- Desktop: Menú completo con Configuración
- Mobile: Solo consulta (sin Configuración)
- Tablas necesarias en Supabase: 
  - inventarios (id, sku, descripcion, familia, existencia, fecha)
  - familias_especiales (id, nombre_familia)
  - familias_skus (id, familia_id, sku)
