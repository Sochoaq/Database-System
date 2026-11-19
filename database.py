"""Headless SQLite data access layer for Vuelta a Colombia cycling logistics."""

from __future__ import annotations

import sqlite3
from typing import Any, Dict, List, Optional, Tuple


class CyclingDatabase:
    """Parameterized SQLite storage and query manager for registered cyclists."""

    ORDER_COLUMNS: Dict[str, str] = {
        "Nombre": "Nombre",
        "Apellido": "Apellido",
        "Num inscripcion": "Numero_inscripcion",
        "Numero_inscripcion": "Numero_inscripcion",
        "Cedula": "Cedula",
        "Fecha nacimiento": "Fecha_Nacimiento",
        "Fecha_Nacimiento": "Fecha_Nacimiento",
        "Pais origen": "Pais_Origen",
        "Pais_Origen": "Pais_Origen",
        "Num equipo": "Numero_equipo",
        "Numero_equipo": "Numero_equipo",
        "Ranking UCI": "Ranking_UCI",
        "Ranking_UCI": "Ranking_UCI",
    }

    def __init__(self, db_path: str = "Base_Preparcial.db") -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS Ciclista (
                Nombre TEXT NOT NULL,
                Apellido TEXT NOT NULL,
                Numero_inscripcion INTEGER PRIMARY KEY,
                Cedula INTEGER NOT NULL,
                Fecha_Nacimiento TEXT NOT NULL,
                Pais_Origen TEXT NOT NULL,
                Numero_equipo INTEGER NOT NULL,
                Ranking_UCI INTEGER NOT NULL
            )
            """
        )
        self.conn.commit()

    def add_cyclist(
        self,
        nombre: str,
        apellido: str,
        numero_inscripcion: int | str,
        cedula: int | str,
        fecha_nacimiento: str,
        pais_origen: str,
        numero_equipo: int | str,
        ranking_uci: int | str,
    ) -> None:
        """Insert a cyclist record using parameterized SQL."""
        self.conn.execute(
            """
            INSERT INTO Ciclista (
                Nombre, Apellido, Numero_inscripcion, Cedula,
                Fecha_Nacimiento, Pais_Origen, Numero_equipo, Ranking_UCI
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(nombre).strip(),
                str(apellido).strip(),
                int(numero_inscripcion),
                int(cedula),
                str(fecha_nacimiento).strip(),
                str(pais_origen).strip(),
                int(numero_equipo),
                int(ranking_uci),
            ),
        )
        self.conn.commit()

    def list_cyclists(self, order_by: str = "Ranking UCI") -> List[Tuple[Any, ...]]:
        """Query cyclists ordered by a strictly whitelisted column name."""
        column = self.ORDER_COLUMNS.get(order_by, "Ranking_UCI")
        cursor = self.conn.execute(f"SELECT * FROM Ciclista ORDER BY {column} ASC")
        return cursor.fetchall()

    def delete_cyclist(self, numero_inscripcion: int | str) -> int:
        """Delete a cyclist by registration number and return affected row count."""
        cursor = self.conn.execute(
            "DELETE FROM Ciclista WHERE Numero_inscripcion = ?",
            (int(numero_inscripcion),),
        )
        self.conn.commit()
        return cursor.rowcount

    def update_nationality(
        self, numero_inscripcion: int | str, nueva_nacionalidad: str
    ) -> int:
        """Update nationality using parameterized SQL to prevent SQL injection."""
        cursor = self.conn.execute(
            "UPDATE Ciclista SET Pais_Origen = ? WHERE Numero_inscripcion = ?",
            (str(nueva_nacionalidad).strip(), int(numero_inscripcion)),
        )
        self.conn.commit()
        return cursor.rowcount

    def get_logistics_summary(self) -> Dict[str, Any]:
        """Compute aggregate logistics and UCI ranking metrics."""
        row = self.conn.execute(
            """
            SELECT
                COUNT(*) AS total_cyclists,
                COUNT(DISTINCT Numero_equipo) AS total_teams,
                COUNT(DISTINCT Pais_Origen) AS total_countries,
                MIN(Ranking_UCI) AS best_uci_rank,
                AVG(Ranking_UCI) AS avg_uci_rank
            FROM Ciclista
            """
        ).fetchone()
        total, teams, countries, best_rank, avg_rank = row
        return {
            "total_cyclists": int(total or 0),
            "total_teams": int(teams or 0),
            "total_countries": int(countries or 0),
            "best_uci_rank": int(best_rank) if best_rank is not None else None,
            "avg_uci_rank": round(float(avg_rank), 2) if avg_rank is not None else None,
        }

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> "CyclingDatabase":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
