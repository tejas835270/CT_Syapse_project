# Store URLs in variable


class Routing_Service():
    # routing-service url and version
    url = "https://127.0.0.1:444/"
    version = "v1"

    # Health endpoints
    health_alive = "/health/alive"
    health_ready = "/health/ready"

    # routes endpoints
    routes = '/routes'


class Mtb_Endpoints:
    GET_MTB_PATIENTS = "/api/v1/patients"

    # CHRONICLE_PATIENTS = "/api/v1/flatstore-patient/flatstore_patients"


class Flatstore_Endpoints:
    FLATSTORE_PATIENTS = "/v1/flatstore_patients"


class Oncology_Endpoints:
    CHRONICLE_PATIENTS = "/api/v1/flatstore-patient/flatstore_patients"
