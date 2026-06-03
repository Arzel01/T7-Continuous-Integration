import unittest
import json
import os
import library

class TestLoanBookFeature(unittest.TestCase):

    def setUp(self):
        """Configura un estado inicial controlado antes de cada test."""
        library.DB_FILE = "test_library_state.json"
        self.mock_data = {
          "members": [
            { "id": "M001", "name": "Alex Otero" },
            { "id": "M002", "name": "Kelly Silva" }
          ],
          "books": [
            { "isbn": "978-0132350884", "title": "Clean Code", "author": "Robert C. Martin" },
            { "isbn": "978-0201616224", "title": "The Pragmatic Programmer", "author": "Andrew Hunt" },
            { "isbn": "978-0134494166", "title": "Design Patterns", "author": "Erich Gamma" },
            { "isbn": "978-1491950296", "title": "Building Microservices", "author": "Sam Newman" }
          ],
          "loans": [
            # M001 ya tiene un libro prestado
            { "book_isbn": "978-0132350884", "member_id": "M001", "loan_date": "2026-05-25", "due_date": "2026-06-08" }
          ]
        }
        library.save_data(self.mock_data)

    def tearDown(self):
        """Limpia el archivo temporal de pruebas al finalizar."""
        if os.path.exists(library.DB_FILE):
            os.remove(library.DB_FILE)

    def test_loan_book_success(self):
        """Caso Feliz: Prestar un libro disponible a un usuario con cupo."""
        resultado = library.loan_book("978-0201616224", "M002")
        self.assertIn("Éxito", resultado)
        
        # Verificar que se guardó en el archivo
        data = library.load_data()
        self.assertEqual(len(data["loans"]), 2)

    def test_loan_already_loaned_book_throws_error(self):
        """Error: No se puede prestar un libro que ya está bajo préstamo."""
        with self.assertRaises(ValueError) as context:
            library.loan_book("978-0132350884", "M002") # Clean Code ya lo tiene M001
        
        self.assertIn("ya se encuentra prestado", str(context.exception))

    def test_loan_exceeding_max_limit_throws_error(self):
        """Error: Un usuario no puede tener más de 3 libros simultáneos."""
        # Forzamos que M001 llene su cupo de 3 libros agregando 2 más manualmente
        data = library.load_data()
        data["loans"].append({ "book_isbn": "978-0201616224", "member_id": "M001", "loan_date": "2026-05-20", "due_date": "2026-06-03" })
        data["loans"].append({ "book_isbn": "978-0134494166", "member_id": "M001", "loan_date": "2026-05-20", "due_date": "2026-06-03" })
        library.save_data(data)

        # Intentamos prestarle un 4to libro
        with self.assertRaises(ValueError) as context:
            library.loan_book("978-1491950296", "M001")
        
        self.assertIn("límite máximo de 3 libros", str(context.exception))

if __name__ == "__main__":
    unittest.main()