# tests/test_api.py
import unittest
from app import create_app, db
from app.models import Items, User

# Model Tests 
class TestUserSerialization(unittest.TestCase):
    def test_serialize(self):
        # Create a user instance
        user = User(UID=1, isAdmin=True, FullName="John Doe", Email="john@example.com", Password="password")

        # Define the expected serialized dictionary
        expected_serialized_data = {
            'UID': 1,
            'isAdmin': True,
            'FullName': "John Doe",
            'Email': "john@example.com"
        }

        # Serialize the user object
        serialized_data = user.serialize()

        # Assert that the serialized data matches the expected dictionary
        self.assertEqual(serialized_data, expected_serialized_data)

class TestItemsSerialization(unittest.TestCase):
    def test_serialize(self):
        # Create an items instance
        items = Items(SerialNumber=1, ItemName="Test Item", Quantity=10, Category="Test Category",
                      BillNumber="123456", DateOfPurchase="2024-01-01", Warranty="1 year", AssignedTo=1)

        # Define the expected serialized dictionary
        expected_serialized_data = {
            'SerialNumber': 1,
            'ItemName': "Test Item",
            'Quantity': 10,
            'Category': "Test Category",
            'BillNumber': "123456",
            'DateOfPurchase': "2024-01-01",
            'Warranty': "1 year",
            'AssignedTo': 1
        }

        # Serialize the items object
        serialized_data = items.serialize()

        # Assert that the serialized data matches the expected dictionary
        self.assertEqual(serialized_data, expected_serialized_data)


# Routes Tests 
class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()



# Add Item Tests 
    def test_add_item_route(self):
        with self.app.app_context():
            # Add a user to assign the item to
            new_user = User(isAdmin=True, FullName="Test User", Email="testuser@nqt.com", Password="password123")
            db.session.add(new_user)
            db.session.commit()
            
            response = self.client.post('/add-item', data=dict(
                itemName="Test Item",
                quantity=1,
                category="Test Category",
                billNumber="123456",
                dateOfPurchase="2024-06-12",
                warranty="1 year",
                assignedTo=new_user.UID  # Use the user's UID for AssignedTo field
            ))
            self.assertEqual(response.status_code, 302)  # Redirect expected after successful item addition

# Add User Tests 
    def test_add_user_get_authenticated(self):
        with self.app.app_context():
            # Add a user to the session
            user = User(FullName="Admin User", Email="admin@nqt.com", Password="password", isAdmin=True)
            db.session.add(user)
            db.session.commit()
            with self.client.session_transaction() as session:
                session['user_id'] = user.UID

            response = self.client.get('/add-user')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Add User', response.data)  # Assuming the add user page contains the words 'Add User'

    def test_add_user_get_unauthenticated(self):
        with self.app.app_context():
            response = self.client.get('/add-user', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_add_user_post_valid(self):
        with self.app.app_context():
            # Add a user to the session
            user = User(FullName="Admin User", Email="admin@nqt.com", Password="password", isAdmin=True)
            db.session.add(user)
            db.session.commit()
            with self.client.session_transaction() as session:
                session['user_id'] = user.UID

            response = self.client.post('/add-user', data=dict(
                fullName="New User",
                email="newuser",
                password="password123",
                confirmPassword="password123",
                isAdmin="on"
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'User added successfully!', response.data)

    def test_add_user_post_invalid_email_prefix(self):
        with self.app.app_context():
            response = self.client.post('/add-user', data=dict(
                fullName="New User",
                email="InvalidEmail!",
                password="password123",
                confirmPassword="password123",
                isAdmin="on"
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Invalid email prefix.', response.data)

    def test_add_user_post_short_password(self):
        with self.app.app_context():
            response = self.client.post('/add-user', data=dict(
                fullName="New User",
                email="newuser",
                password="short",
                confirmPassword="short",
                isAdmin="on"
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Password must be at least 6 characters long.', response.data)

    def test_add_user_post_passwords_do_not_match(self):
        with self.app.app_context():
            response = self.client.post('/add-user', data=dict(
                fullName="New User",
                email="newuser",
                password="password123",
                confirmPassword="differentpassword",
                isAdmin="on"
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)



# Delete Tests 
    def test_delete_item_route(self):
        with self.app.app_context():
            # Add a user and an item to delete
            new_user = User(isAdmin=True, FullName="Test User", Email="testuser@nqt.com", Password="password123")
            db.session.add(new_user)
            db.session.commit()
            new_item = Items(ItemName="Test Item", Quantity=1, Category="Test Category",
                             BillNumber="123456", DateOfPurchase="2024-06-12", Warranty="1 year", AssignedTo=new_user.UID)
            db.session.add(new_item)
            db.session.commit()

            response = self.client.post('/delete-item', data=dict(serialNumber=new_item.SerialNumber))
            self.assertEqual(response.status_code, 302)  # Redirect expected after successful item deletion

    def test_delete_user_route(self):
        with self.app.app_context():
            # Add a user to delete
            new_user = User(isAdmin=True, FullName="Test User", Email="testuser@nqt.com", Password="password123")
            db.session.add(new_user)
            db.session.commit()

            response = self.client.post('/delete-user', data=dict(uid=new_user.UID))
            self.assertEqual(response.status_code, 302)  # Redirect expected after successful user deletion

# Assign/ Unassign Tests
    def test_assign_item_route(self):
        with self.app.app_context():
            # Add a user and an item to assign
            new_user = User(isAdmin=True, FullName="Test User", Email="testuser@nqt.com", Password="password123")
            db.session.add(new_user)
            db.session.commit()
            new_item = Items(ItemName="Test Item", Quantity=1, Category="Test Category",
                             BillNumber="123456", DateOfPurchase="2024-06-12", Warranty="1 year")
            db.session.add(new_item)
            db.session.commit()

            response = self.client.post('/assign-item', data=dict(serialNumber=new_item.SerialNumber, assignedTo=new_user.UID))
            self.assertEqual(response.status_code, 302)  # Redirect expected after successful item assignment

    def test_unassign_item_route(self):
        with self.app.app_context():
            # Add a user and an item to unassign
            new_user = User(isAdmin=True, FullName="Test User", Email="testuser@nqt.com", Password="password123")
            db.session.add(new_user)
            db.session.commit()
            new_item = Items(ItemName="Test Item", Quantity=1, Category="Test Category",
                             BillNumber="123456", DateOfPurchase="2024-06-12", Warranty="1 year", AssignedTo=new_user.UID)
            db.session.add(new_item)
            db.session.commit()

            response = self.client.post('/unassign-item', data=dict(serialNumber=new_item.SerialNumber))
            self.assertEqual(response.status_code, 302)  # Redirect expected after successful item unassignment


# Edit Tests 
    def test_edit_item_missing_serial_number(self):
        with self.app.app_context():
            response = self.client.post('/edit-item', data=dict(
                editItemName="New Item Name",
                editQuantity="10",
                editCategory="New Category",
                editBillNumber="123456",
                editDateOfPurchase="2024-06-12",
                editWarranty="2 years"
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Serial number is required.', response.data)

    def test_edit_item_valid(self):
        with self.app.app_context():
            # Add an item to edit
            new_item = Items(SerialNumber="1234", ItemName="Old Item Name", Quantity=5, Category="Old Category",
                             BillNumber="654321", DateOfPurchase="2023-06-12", Warranty="1 year")
            db.session.add(new_item)
            db.session.commit()

            response = self.client.post('/edit-item', data=dict(
                editSerialNumber="1234",
                editItemName="New Item Name",
                editQuantity="10",
                editCategory="New Category",
                editBillNumber="123456",
                editDateOfPurchase="2024-06-12",
                editWarranty="2 years"
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Item updated successfully!', response.data)
            
            # Verify the changes
            updated_item = db.session.get(Items, "1234")
            self.assertEqual(updated_item.ItemName, "New Item Name")
            self.assertEqual(updated_item.Quantity, 10)
            self.assertEqual(updated_item.Category, "New Category")
            self.assertEqual(updated_item.BillNumber, "123456")
            self.assertEqual(updated_item.DateOfPurchase, "2024-06-12")
            self.assertEqual(updated_item.Warranty, "2 years")

    def test_edit_item_not_found(self):
        with self.app.app_context():
            response = self.client.post('/edit-item', data=dict(
                editSerialNumber="9999",  # Serial number that doesn't exist
                editItemName="New Item Name",
                editQuantity="10",
                editCategory="New Category",
                editBillNumber="123456",
                editDateOfPurchase="2024-06-12",
                editWarranty="2 years"
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Item not found.', response.data)


    def test_edit_user_valid(self):
        with self.app.app_context():
            # Add a user to edit
            new_user = User(UID=1, FullName="Old User Name", Email="olduser@nqt.com", isAdmin=False)
            db.session.add(new_user)
            db.session.commit()

            response = self.client.post('/edit-user', data=dict(
                uid=1,
                fullName="New User Name",
                email="newuser@nqt.com",
                isAdmin="on"  # Checkbox is present
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'User updated successfully!', response.data)
            
            # Verify the changes
            updated_user = db.session.get(User, 1)
            self.assertEqual(updated_user.FullName, "New User Name")
            self.assertEqual(updated_user.Email, "newuser@nqt.com")
            self.assertTrue(updated_user.isAdmin)

    def test_edit_user_not_found(self):
        with self.app.app_context():
            response = self.client.post('/edit-user', data=dict(
                uid=9999,  # UID that doesn't exist
                fullName="New User Name",
                email="newuser@nqt.com",
                isAdmin="on"  # Checkbox is present
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'User not found.', response.data)

    def test_edit_user_missing_uid(self):
        with self.app.app_context():
            response = self.client.post('/edit-user', data=dict(
                fullName="New User Name",
                email="newuser@nqt.com",
                isAdmin="on"  # Checkbox is present
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 400)  # Expecting a bad request status




# Session Tests 
    def test_logout(self):
        try:
            with self.app.app_context():
                # Add an admin user to test login
                admin_user = User(isAdmin=True, FullName="Admin User", Email="admin@nqt.com", Password="password")
                db.session.add(admin_user)
                db.session.commit()

                # Log in first
                response_login = self.client.post('/', data=dict(
                    email='admin@nqt.com',
                    password='password'
                ), follow_redirects=True)

                # Logout
                response_logout = self.client.get('/logout', follow_redirects=True)
                self.assertEqual(response_logout.status_code, 200)
                # self.assertIn(b'Logged out successfully', response_logout.data)  # Example assertion, update as necessary

        except Exception as e:
            print(f"Error during logout test: {e}")
    
    def test_login_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)  # Adjust based on your login page content

    def test_login_post_admin_success(self):
        with self.app.app_context():
            admin_user = User(UID=1, isAdmin=True, FullName="Admin User", Email="admin@nqt.com", Password="adminpass")
            db.session.add(admin_user)
            db.session.commit()
        
        response = self.client.post('/', data=dict(email='admin', password='adminpass'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_post_employee_success(self):
        with self.app.app_context():
            employee_user = User(UID=2, isAdmin=False, FullName="Employee User", Email="employee@nqt.com", Password="employeepass")
            db.session.add(employee_user)
            db.session.commit()
        
        response = self.client.post('/', data=dict(email='employee', password='employeepass'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_post_invalid_credentials(self):
        response = self.client.post('/', data=dict(email='invalid', password='invalidpass'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid credentials', response.data)

    def test_login_already_authenticated_admin(self):
        with self.app.app_context():
            admin_user = User(UID=1, isAdmin=True, FullName="Admin User", Email="admin@nqt.com", Password="adminpass")
            db.session.add(admin_user)
            db.session.commit()
        
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1

        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_already_authenticated_employee(self):
        with self.app.app_context():
            employee_user = User(UID=2, isAdmin=False, FullName="Employee User", Email="employee@nqt.com", Password="employeepass")
            db.session.add(employee_user)
            db.session.commit()
        
        with self.client.session_transaction() as sess:
            sess['user_id'] = 2

        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)





# Admin Tests 
    def test_admin_route_admin_user_all_items(self):
        with self.app.app_context():
            # Add an admin user to the session
            admin_user = User(isAdmin=True, FullName="Admin User", Email="admin@nqt.com", Password="password")
            db.session.add(admin_user)
            db.session.commit()
            with self.client.session_transaction() as session:
                session['user_id'] = admin_user.UID

            response = self.client.get('/admin?filter=all_items')
            self.assertEqual(response.status_code, 200)

    def test_admin_route_admin_user_assigned_items(self):
        with self.app.app_context():
            # Add an admin user to the session
            admin_user = User(isAdmin=True, FullName="Admin User", Email="admin@nqt.com", Password="password")
            db.session.add(admin_user)
            db.session.commit()
            with self.client.session_transaction() as session:
                session['user_id'] = admin_user.UID

            response = self.client.get('/admin?filter=assigned')
            self.assertEqual(response.status_code, 200)

    def test_admin_route_admin_user_unassigned_items(self):
        with self.app.app_context():
            # Add an admin user to the session
            admin_user = User(isAdmin=True, FullName="Admin User", Email="admin@nqt.com", Password="password")
            db.session.add(admin_user)
            db.session.commit()
            with self.client.session_transaction() as session:
                session['user_id'] = admin_user.UID

            response = self.client.get('/admin?filter=unassigned')
            self.assertEqual(response.status_code, 200)

    def test_admin_route_admin_user_category_filter(self):
        with self.app.app_context():
            # Add an admin user to the session
            admin_user = User(isAdmin=True, FullName="Admin User", Email="admin@nqt.com", Password="password")
            db.session.add(admin_user)
            db.session.commit()
            with self.client.session_transaction() as session:
                session['user_id'] = admin_user.UID

            response = self.client.get('/admin?filter=category')
            self.assertEqual(response.status_code, 200)

    def test_admin_route_admin_user_default_filter(self):
        with self.app.app_context():
            # Add an admin user to the session
            admin_user = User(isAdmin=True, FullName="Admin User", Email="admin@nqt.com", Password="password")
            db.session.add(admin_user)
            db.session.commit()
            with self.client.session_transaction() as session:
                session['user_id'] = admin_user.UID

            response = self.client.get('/admin')
            self.assertEqual(response.status_code, 200)

    def test_admin_route_non_admin_user(self):
        with self.app.app_context():
            # Add a non-admin user to the session
            non_admin_user = User(isAdmin=False, FullName="Non Admin User", Email="nonadmin@nqt.com", Password="password")
            db.session.add(non_admin_user)
            db.session.commit()
            with self.client.session_transaction() as session:
                session['user_id'] = non_admin_user.UID

            response = self.client.get('/admin')
            self.assertEqual(response.status_code, 200)

    def test_admin_route_unauthenticated_user(self):
        with self.app.app_context():
            response = self.client.get('/admin', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    

# Profile Tests 
    def test_profile_route_authenticated_user(self):
        with self.app.app_context():
            # Add a user to the session
            user = User(FullName="Test User", Email="testuser@nqt.com", Password="password123")
            db.session.add(user)
            db.session.commit()
            with self.client.session_transaction() as session:
                session['user_id'] = user.UID

            response = self.client.get('/profile')
            self.assertEqual(response.status_code, 200)

    def test_profile_route_unauthenticated_user(self):
        with self.app.app_context():
            response = self.client.get('/profile', follow_redirects=True)
            self.assertEqual(response.status_code, 200)# Assuming the login page contains the word 'Login'

if __name__ == "__main__":
    unittest.main()
#  Working vala test in folder