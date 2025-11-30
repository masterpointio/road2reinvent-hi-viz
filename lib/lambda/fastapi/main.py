from mangum import Mangum
from app import app

handler = Mangum(app, api_gateway_base_path="/api")
