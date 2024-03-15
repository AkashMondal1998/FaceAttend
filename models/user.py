from .extensions import flask_bcrypt, mysql


class User:
    """User model"""

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def add_user(self):
        """Add user to the database"""

        cur = mysql.connection.cursor()

        # check if the user is already registered
        cur.execute("SELECT * FROM users WHERE email = %s", (self.email,))
        if cur.rowcount != 0:
            return False

        # hash the password
        password_hash = flask_bcrypt.generate_password_hash(self.password)

        cur.execute(
            "INSERT INTO users (email,password) VALUES(%s,%s)",
            (self.email, password_hash),
        )
        mysql.connection.commit()

        return True

    def check_user(self):
        """Check the details provided by the user"""

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT password FROM users WHERE email = %s",
            (self.email,),
        )
        password_hash = cur.fetchone()

        # if there is no password associated with the email provided
        if not password_hash:
            return False

        # if the password given is wrong
        if not flask_bcrypt.check_password_hash(password_hash[0], self.password):
            return False

        return True
