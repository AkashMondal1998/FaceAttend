from flask_restx import Api
from .student import api as ns1
from .user import api as ns2
from .admin import api as ns3

api = Api(
    version="0.1",
    title="Attendance API",
    description="A simple Attendance API using face recognition",
)


api.add_namespace(ns1)
api.add_namespace(ns2)
api.add_namespace(ns3)
