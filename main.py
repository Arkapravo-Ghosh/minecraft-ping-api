from fastapi import FastAPI, Request, Response
from mcstatus import JavaServer, BedrockServer


app = FastAPI()


@app.get("/java")
async def java_route(req: Request, res: Response):
    try:
        query_params = req.query_params
        try:
            server_ip = query_params["ip"]
            server_port = query_params["port"] if "port" in query_params else 25565
        except KeyError:
            res.status_code = 400
            return {
                "status": "error",
                "message": "Please provide the IP address and port number",
            }
        java_server = JavaServer.lookup(f"{server_ip}:{server_port}")
        ping = java_server.ping()
        status = java_server.status()
        response = {
            "status": "online",
            "description": str(status.description),
            "ping": ping,
            "players": status.players.online,
            "max_players": status.players.max,
            "version": getattr(status.version, "name", None),
            "protocol": getattr(status.version, "protocol", None),
        }
        return response
    except TimeoutError:
        res.status_code = 504
        return {"status": "offline"}
    except Exception as error:
        print(f"An error occurred: {error}")
        res.status_code = 500
        return {
            "status": "error",
            "message": "Internal server error",
        }


@app.get("/bedrock")
async def bedrock_route(req: Request, res: Response):
    try:
        query_params = req.query_params
        try:
            server_ip = query_params["ip"]
            server_port = query_params["port"] if "port" in query_params else 19132
        except KeyError:
            res.status_code = 400
            return {
                "status": "error",
                "message": "Please provide the IP address and port number",
            }
        bedrock_server = BedrockServer.lookup(f"{server_ip}:{server_port}")
        status = bedrock_server.status()
        response = {
            "status": "online",
            "description": str(status.description),
            "players": status.players.online,
            "max_players": status.players.max,
            "version": getattr(status.version, "name", None),
            "protocol": getattr(status.version, "protocol", None),
        }
        return response
    except TimeoutError:
        res.status_code = 504
        return {"status": "offline"}
    except Exception as error:
        print(f"An error occurred: {error}")
        res.status_code = 500
        return {
            "status": "error",
            "message": "Internal server error",
        }
