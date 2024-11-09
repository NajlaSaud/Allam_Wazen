
# Wazen Project

Wazen is a Flask-based web application designed for Arabic poetry analysis. This tool helps analyze the meter (بحر) and rhyme (قافية) of Arabic poetry, providing feedback on rhythm and highlighting any mismatches. The project includes functionalities for diacritization and other aspects of Arabic poetry analysis, utilizing a collection of scripts and modules within the `Bait_Analysis` and `Bohour` packages.

## Project Structure

```
Wazen
│
├── Bait_Analysis
│   ├── __init__.py
│   ├── BaitAnalyzer.py           # Core class for analyzing Arabic poetry lines
│   ├── config.json               # Configuration file
│   ├── GPTDiacritizer.py         # Script for diacritizing Arabic text
│   ├── MeterClassifier.py        # Script for classifying meter of poetry lines
│   ├── utils.py                  # Utility functions for text processing
│   └── variables.env             # Environment variables
│
├── Dataset                       # Folder to store datasets
│
├── static
│   └── images                    # Static images folder
│       └── wazen_logo.png        # Logo image
│
├── templates
│   └── index.html                # HTML template for the front-end
│
├── venv                          # Virtual environment
├── app.py                        # Flask application entry point
└── README.md                     # Project documentation (this file)
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Wazen.git
   cd Wazen
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables:**
   Configure environment variables in `variables.env`:
   ```
   OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"
   DEPLOYMENT_ID="YOUR_DEPLOYMENT_ID_HERE"
   IBM_API_KEY="YOUR_KEY_HERE"
   IBM_PROJECT_ID="YOUR_PROJECT_ID_HERE"
   USER_ACCESS_TOKEN="YOUR_USER_ACCESS_TOKEN"
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

The application will be available at `http://127.0.0.1:5000`.

## Usage

1. **Homepage:** Navigate to `http://127.0.0.1:5000` to access the main interface.

2. **Analyze Poetry:** Enter Arabic poetry text to analyze its meter and rhyme structure. The application will process the input, diacritize it, classify the meter, and check for pattern mismatches.

3. **Results:** The output displays the identified meter, rhyme, and any mismatches found in the structure, providing useful feedback on the analyzed text.

## Main Components

- **`BaitAnalyzer.py`:** Core module for analyzing poetry lines (baits).
- **`MeterClassifier.py`:** Classifies the meter of poetry lines.
- **`GPTDiacritizer.py`:** Provides diacritization for the Arabic text.
- **`utils.py`:** Contains helper functions for text cleaning and processing.
- **`app.py`:** Flask server that handles HTTP requests, processes the text, and renders the results on the front-end.

## Example Workflow

1. **Input:** User submits Arabic poetry text.
2. **Processing:** 
   - Text is cleaned and split into baits (lines).
   - Each bait is diacritized and analyzed for meter and rhyme.
3. **Output:** The application displays the meter, rhyme structure, and any detected mismatches or errors.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

This project utilizes multiple open-source libraries and packages for Arabic text processing and meter analysis. Special thanks to contributors and the open-source community for making these tools available.
