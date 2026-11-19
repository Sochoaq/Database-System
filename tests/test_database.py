import sqlite3
import tempfile
import unittest
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from database import CyclingDatabase  # noqa: E402


class TestCyclingDatabase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.tmpdir.name) / "test_cycling.db")
        self.db = CyclingDatabase(self.db_path)

    def tearDown(self):
        self.db.close()
        self.tmpdir.cleanup()

    def test_insert_and_whitelist_ordered_query(self):
        self.db.add_cyclist("Egan", "Bernal", 101, 101010, "1997-01-13", "Colombia", 1, 12)
        self.db.add_cyclist("Nairo", "Quintana", 202, 202020, "1990-02-04", "Colombia", 2, 5)
        self.db.add_cyclist("Richard", "Carapaz", 303, 303030, "1993-05-29", "Ecuador", 3, 8)

        by_rank = self.db.list_cyclists("Ranking UCI")
        self.assertEqual([r[0] for r in by_rank], ["Nairo", "Richard", "Egan"])

        # Unknown order column safely defaults to Ranking_UCI instead of failing or injecting SQL
        fallback = self.db.list_cyclists("Nombre; DROP TABLE Ciclista;--")
        self.assertEqual([r[0] for r in fallback], ["Nairo", "Richard", "Egan"])

    def test_update_nationality_resists_sql_injection(self):
        self.db.add_cyclist("Rigoberto", "Uran", 404, 404040, "1987-01-26", "Colombia", 4, 15)
        payload = "Colombia'; DROP TABLE Ciclista;--"
        updated = self.db.update_nationality(404, payload)
        self.assertEqual(updated, 1)

        rows = self.db.list_cyclists("Num inscripcion")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][5], payload)

    def test_delete_and_summary_metrics(self):
        self.db.add_cyclist("Daniel", "Martinez", 11, 111, "1996-04-25", "Colombia", 7, 10)
        self.db.add_cyclist("Sergio", "Higuita", 22, 222, "1997-08-01", "Colombia", 8, 20)

        summary = self.db.get_logistics_summary()
        self.assertEqual(summary["total_cyclists"], 2)
        self.assertEqual(summary["total_teams"], 2)
        self.assertEqual(summary["total_countries"], 1)
        self.assertEqual(summary["best_uci_rank"], 10)
        self.assertEqual(summary["avg_uci_rank"], 15.0)

        deleted = self.db.delete_cyclist(11)
        self.assertEqual(deleted, 1)
        self.assertEqual(self.db.get_logistics_summary()["total_cyclists"], 1)


if __name__ == "__main__":
    unittest.main()
