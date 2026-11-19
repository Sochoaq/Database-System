# Vuelta a Colombia — Sistema de Gestión Logística y Trazabilidad UCI

Plataforma de escritorio para gestión operativa y logística de ciclistas en competencias por etapas (*Vuelta a Colombia*), construida en **Python**, **PyQt5** y **SQLite3** con capa de acceso a datos desacoplada y consultas parametrizadas.

---

## Arquitectura del Sistema

```mermaid
flowchart LR
    A["PyQt5 Desktop UI (UI.py / main.py)"] -->|"Validación de entrada y eventos"| B["CyclingDatabase Data Layer (database.py)"]
    B -->|"SQL Parametrizado + Whitelist ORDER BY"| C["SQLite Storage (Base_Preparcial.db)"]
```

### Componentes

| Archivo | Responsabilidad |
| :--- | :--- |
| [`database.py`](database.py) | Capa de persistencia headless (`CyclingDatabase`): creación idempotente de esquema, operaciones CRUD parametrizadas, ordenamiento seguro por lista blanca (`ORDER_COLUMNS`) y métricas agregadas (`get_logistics_summary`). |
| [`main.py`](main.py) | Ventana principal PyQt5 conectada a `Ui_MainWindow` (`UI.py`) y `CyclingDatabase`, con validación de campos y punto de entrada protegido por `if __name__ == "__main__"`. |
| [`UI.py`](UI.py) | Definición de interfaz gráfica multi-pestaña (Agregar, Consultar, Borrar, Actualizar). |
| [`tests/test_database.py`](tests/test_database.py) | Pruebas unitarias automatizadas con bases SQLite temporales para CRUD, ordenamiento seguro y resistencia frente a inyección SQL. |

---

## Modelo Relacional (`Ciclista`)

| Columna | Tipo SQLite | Descripción |
| :--- | :--- | :--- |
| `Nombre` | `TEXT NOT NULL` | Nombres del corredor |
| `Apellido` | `TEXT NOT NULL` | Apellidos del corredor |
| `Numero_inscripcion` | `INTEGER PRIMARY KEY` | Dorsal / código único de inscripción |
| `Cedula` | `INTEGER NOT NULL` | Documento de identidad |
| `Fecha_Nacimiento` | `TEXT NOT NULL` | Fecha de nacimiento |
| `Pais_Origen` | `TEXT NOT NULL` | Nacionalidad deportiva |
| `Numero_equipo` | `INTEGER NOT NULL` | Identificador de escuadra |
| `Ranking_UCI` | `INTEGER NOT NULL` | Posición en clasificación UCI |

---

## Seguridad e Integridad de Datos

* **Prevención de SQL Injection:** Toda inserción, eliminación y actualización de nacionalidad utiliza marcadores `?` (`cursor.execute(..., params)`) en lugar de concatenación de cadenas.
* **Ordenamiento controlado:** Las consultas `SELECT ... ORDER BY` resuelven el criterio de ordenamiento mediante un diccionario cerrado (`CyclingDatabase.ORDER_COLUMNS`).

---

## Ejecución y Pruebas

```bash
pip install -r requirements.txt

# Ejecutar pruebas unitarias de la capa de base de datos
python -m unittest discover -s tests -v

# Iniciar interfaz de escritorio
python main.py
```

Documentación de usuario adicional disponible en [Documentacion de usuario.pdf](Documentacion%20de%20usuario.pdf).
