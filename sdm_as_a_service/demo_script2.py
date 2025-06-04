import webbrowser # Used to open URLs in a web browser
import sys # Used for sys.exit() to cleanly exit the script

def run_browser_demo(urls):
    """
    Runs a demo that opens a list of URLs in the default web browser,
    pausing for user input between each URL.

    Args:
        urls (list): A list of strings, where each string is a URL to open.
    """
    print("--- Starting Web Browser Demo ---")
    print("Each URL will open in your default web browser.")
    print("Press Enter to open the next URL, or type 'exit' to quit.")

    for i, url in enumerate(urls):
        print(f"\n{'='*50}")
        print(f"Opening URL {i+1}/{len(urls)}: {url}")
        print(f"{'='*50}")

        try:
            # Open the URL in a new browser tab/window
            webbrowser.open_new_tab(url)
            print(f"Successfully opened '{url}' in your browser.")
        except Exception as e:
            print(f"Error opening URL '{url}': {e}")
            print("Please ensure you have a default web browser configured.")

        # Ask for text input between calls, unless it's the very last URL
        if i < len(urls) - 1:
            user_input = input("\n[Demo Paused] Enter text to open the next URL (or type 'exit' to quit): ").strip().lower()
            if user_input == 'exit':
                print("\nExiting demo as requested.")
                sys.exit(0) # Cleanly exit the script
        else:
            print("\n--- All URLs opened. Demo complete! ---")

# --- Configuration Section ---
# IMPORTANT: Replace these example URLs with your actual web page or public API URLs.
# These URLs will be opened in your default web browser.
my_web_urls = [
    "http://0.0.0.0:8000/validate-url?url=https://raw.githubusercontent.com/smart-data-models/dataModel.Weather/refs/heads/master/WeatherObserved/examples/example.json",
    "http://0.0.0.0:8000/validate-url?url=https://smart-data-models.github.io/dataModel.Weather/WeatherObserved/examples/example-normalized.jsonld",
    "http://0.0.0.0:8000/subjects",
    "http://0.0.0.0:8000/datamodels/dataModel.Weather",          #
    "http://0.0.0.0:8000/datamodels/mySubject",
    "http://0.0.0.0:8000/datamodels/dataModel.Weather/WeatherObserved/attributes",
    "http://0.0.0.0:8000/datamodels/dataModel.Weather/WeatherObserved/example",
    "http://0.0.0.0:8000/search/datamodels/Weather/40",
    "http://0.0.0.0:8000/search/datamodels/Weather/80",
    "http://0.0.0.0:8000/datamodels/exact-match/WeatherObserved",
    "http://0.0.0.0:8000/subjects/exact-match/dataModel.Weather",
    "http://0.0.0.0:8000/datamodels/WeatherObserved/contexts",
]


# --- Run the Demo ---
if __name__ == "__main__":
    run_browser_demo(my_web_urls)
