"""
Minimal Flask API for SafeHome remote access (SRS web use cases).
Provides login, arm/disarm, status, intrusion logs, and camera list metadata.
"""
from flask import Flask, request, jsonify


def create_app(system):
    app = Flask(__name__)

    def require_auth():
        pwd1 = request.headers.get("X-Password-1") or request.args.get("p1")
        pwd2 = request.headers.get("X-Password-2") or request.args.get("p2")
        if not pwd1 or not pwd2:
            return False
        return system.login("admin", f"{pwd1}:{pwd2}", "WEB")

    @app.route("/api/login", methods=["POST"])
    def login():
        data = request.get_json(silent=True) or {}
        pwd1 = data.get("password1")
        pwd2 = data.get("password2")
        if not pwd1 or not pwd2:
            return jsonify({"success": False, "error": "password1/password2 required"}), 400
        ok = system.login("admin", f"{pwd1}:{pwd2}", "WEB")
        return jsonify({"success": ok})

    @app.route("/api/status", methods=["GET"])
    def status():
        if not require_auth():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        return jsonify(system.get_system_status())

    @app.route("/api/arm", methods=["POST"])
    def arm():
        if not require_auth():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        data = request.get_json(silent=True) or {}
        mode = data.get("mode", "AWAY").upper()
        from safehome.configuration.safehome_mode import SafeHomeMode
        try:
            mode_enum = SafeHomeMode[mode]
        except KeyError:
            return jsonify({"success": False, "error": "Invalid mode"}), 400
        ok = system.arm_system(mode_enum)
        return jsonify({"success": ok})

    @app.route("/api/disarm", methods=["POST"])
    def disarm():
        if not require_auth():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        system.disarm_system()
        return jsonify({"success": True})

    @app.route("/api/cameras", methods=["GET"])
    def cameras():
        if not require_auth():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        cams = system.camera_controller.get_all_camera_statuses()
        return jsonify({"success": True, "cameras": cams})

    @app.route("/api/logs/intrusions", methods=["GET"])
    def intrusions():
        if not require_auth():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        limit = int(request.args.get("limit", 50))
        logs = system.config.storage.get_unseen_logs(limit=limit, event_type="ALARM")
        return jsonify({"success": True, "logs": logs, "count": len(logs)})

    @app.route("/api/logs/mark_seen", methods=["POST"])
    def mark_seen():
        if not require_auth():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        data = request.get_json(silent=True) or {}
        log_ids = data.get("log_ids", [])
        system.config.storage.mark_logs_seen(log_ids)
        return jsonify({"success": True, "marked": len(log_ids)})

    return app


def run_api(system, host="0.0.0.0", port=5000):
    app = create_app(system)
    app.run(host=host, port=port)
