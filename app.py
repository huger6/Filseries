from threading import Timer
from app import create_app, open_browser

app = create_app()

if __name__ == "__main__":
    # Open browser after 2 seconds
    Timer(2, open_browser).start()

    # Run application
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
