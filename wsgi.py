from app import app

if __name__ == "__main__":
    # Pour les serveurs qui utilisent wsgi au lieu de Procfile
    from waitress import serve
    import os
    
    port = int(os.environ.get("PORT", 8080))
    serve(app, host="0.0.0.0", port=port) 