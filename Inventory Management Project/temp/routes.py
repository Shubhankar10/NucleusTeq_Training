

    @app.route('/users', methods=['GET', 'POST'])
    def handle_users():
        if request.method == 'GET':
            users = User.query.all()
        elif request.method == 'POST':
            print("Users Post Succesfull")
            isAdmin_str = request.form.get('isAdmin', 'off')  # Default value if checkbox is unchecked
            isAdmin = 0 if isAdmin_str == 'off' else 1
            fullName = request.form['fullName']
            email = request.form['email']
            password = request.form['password']

            new_user = User(isAdmin=isAdmin, FullName=fullName, Email=email, Password=password)
            db.session.add(new_user)
            db.session.commit()
        
            users = User.query.all()
        return render_template('users.html', users=users)

    @app.route('/items', methods=['GET', 'POST'])
    def handle_items():
        users = User.query.all()  # Retrieve all users
        
        if request.method == 'POST':
            print("Items Post Successful")
            
            # Retrieve form data
            serialNumber = request.form['serialNumber']
            itemName = request.form['itemName']
            quantity = request.form['quantity']
            category = request.form['category']
            billNumber = request.form['billNumber']
            dateOfPurchase = request.form['dateOfPurchase']
            warranty = request.form['warranty']
            assignedTo = request.form['assignedTo']
            
            # Create new item and add to the database
            new_item = Items(
                ItemName=itemName, 
                Quantity=quantity, 
                Category=category,
                BillNumber=billNumber, 
                DateOfPurchase=dateOfPurchase, 
                Warranty=warranty, 
                AssignedTo=assignedTo
            )
            db.session.add(new_item)
            db.session.commit()

        return render_template('admin.html', users=users)  # Ensure 'users' variable matches with the one in the template


