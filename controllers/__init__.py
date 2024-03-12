from flask_restx import Api
from .student import api as ns1
from .admin import api as ns2

api = Api(
    version="1.0",
    title="Attendance API",
    description="A simple Attendance API using face recognition",
)


api.add_namespace(ns1)
api.add_namespace(ns2)