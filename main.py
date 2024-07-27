from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from mcstatus import JavaServer, BedrockServer


app = FastAPI()


@app.get("/java")
def java_route(req: Request, res: Response):
    try:
        query_params = req.query_params
        try:
            server_ip = query_params["ip"]
            server_port = query_params["port"] if "port" in query_params else 25565
        except KeyError:
            response: JSONResponse = {
                "status": "error",
                "message": "Please provide the IP address and port number",
            }
            res.status_code = 400
            return response
        java_server = JavaServer.lookup(f"{server_ip}:{server_port}")
        ping = java_server.ping()
        status = java_server.status()
        response: JSONResponse = {
            "status": "online",
            "description": status.description,
            "ping": ping,
            "players": status.players.online,
            "max_players": status.players.max,
            "version": status.version.name,
            "protocol": status.version.protocol,
        }
        return response
    except TimeoutError:
        response: JSONResponse = {"status": "offline"}
        return response
    except Exception as error:
        print(f"An error occurred: ", error)
        response: JSONResponse = {
            "status": "error",
            "message": "Internal server error",
        }
        return response


@app.get("/bedrock")
def bedrock_route(req: Request, res: Response):
    try:
        query_params = req.query_params
        try:
            server_ip = query_params["ip"]
            server_port = query_params["port"] if "port" in query_params else 19132
        except KeyError:
            response: JSONResponse = {
                "status": "error",
                "message": "Please provide the IP address and port number",
            }
            res.status_code = 400
            return response
        bedrock_server = BedrockServer.lookup(f"{server_ip}:{server_port}")
        status = bedrock_server.status()
        response: JSONResponse = {
            "status": "online",
            "description": status.description,
            "players": status.players.online,
            "max_players": status.players.max,
            "version": status.version.name,
            "protocol": status.version.protocol,
        }
        return response
    except TimeoutError:
        response: JSONResponse = {"status": "offline"}
        return response
    except Exception as error:
        print(f"An error occurred: ", error)
        response: JSONResponse = {
            "status": "error",
            "message": "Internal server error",
        }
        return response
