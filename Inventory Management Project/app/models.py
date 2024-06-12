
from . import db


class User(db.Model):
    UID = db.Column(db.Integer, primary_key=True)
    isAdmin = db.Column(db.Boolean)
    FullName = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    Password = db.Column(db.String(255))

    assigned_items = db.relationship('Items', backref='user', lazy=True)

    def serialize(self):
        return {
            'UID': self.UID,
            'isAdmin': self.isAdmin,
            'FullName': self.FullName,
            'Email': self.Email
        }

class Items(db.Model):
    SerialNumber = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ItemName = db.Column(db.String(100), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    Category = db.Column(db.String(100), nullable=False)
    BillNumber = db.Column(db.String(20), nullable=False)
    DateOfPurchase = db.Column(db.String(20), nullable=False)
    Warranty = db.Column(db.String(50), nullable=False)
    AssignedTo = db.Column(db.Integer, db.ForeignKey('user.UID'), nullable=True, default=None)

    def serialize(self):
        return {
            'SerialNumber': self.SerialNumber,
            'ItemName': self.ItemName,
            'Quantity': self.Quantity,
            'Category': self.Category,
            'BillNumber': self.BillNumber,
            'DateOfPurchase': self.DateOfPurchase,
            'Warranty': self.Warranty,
            'AssignedTo': self.AssignedTo
        }

