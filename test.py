import os
import unittest
import app as kanban

class Tests(unittest.TestCase):

    def setUp(self):
        kanban.app.config['TESTING'] = True
        kanban.app.config['WTF_CSRF_ENABLED'] = False
        kanban.app.config['DEBUG'] = False
        kanban.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.app = kanban.app.test_client()
        db = kanban.db
        db.drop_all()
        db.create_all()
        self.assertEqual(kanban.app.debug, False)

    def tearDown(self):
        pass

    def test_index(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        response = self.app.post(
          '/add',
          data = dict(title = "Test Item Title", description = "Test Item Description", status = 1),
          follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_updatetodo(self):
        self.test_add()
        response = self.app.get("/updatetodo/1", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_updatedoing(self):
        self.test_add()
        response = self.app.get("/updatedoing/1", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_updatedone(self):
        self.test_add()
        response = self.app.get("/updatedone/1", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        self.test_add()
        response = self.app.get("/delete/1", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
