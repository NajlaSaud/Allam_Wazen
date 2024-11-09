from flask import Flask, render_template, request
from Bait_Analysis.utils import clean
from Bait_Analysis.BaitAnalyzer import BaitAnalysis
import re
import json

# Initiate Flask Server
app = Flask(__name__)

# analyzer object
analysis = BaitAnalysis()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_text():
    # Get poet text
    arabic_text = request.form['arabic_text']

    if arabic_text:
        # Prepare baits list
        baits_list = process_baits_string(arabic_text)

        # Analyze baits
        bait_analysis = analysis.analyze(baits=baits_list)

        # Process analysis json: replace '[]' with '{}'
        analysis_json = process_analysis_json(str(bait_analysis))

        # Extract meter
        meter = extract_meter(analysis_json)

        # Extract qafiah
        qafiah = extract_qafiah(analysis_json)

        # Process analysis list
        analysis_list = process_analysis_list(analysis_json)

        # Get notes
        # notes = get_notes(analysis_list, baits_list, meter, qafiah)

        return render_template('index.html', meter=meter, qafiah=qafiah, analysis=analysis_list)

    return render_template('index.html')


def process_baits_string(input):
    lines = input.strip().split("\n")
    baits = []
    for i in range(len(lines) // 2):
        bait = " # ".join(lines[i * 2: (i + 1) * 2])
        bait = clean(bait)
        baits.append(bait)
    return baits


def process_analysis_json(json_string):
    # Replace single quotes with double quotes and parentheses with square brackets
    analysis_json = json_string.replace("'", '"').replace("(", "[").replace(")", "]")

    # Convert String to JSON
    analysis_json = json.loads(analysis_json)
    return analysis_json


def extract_meter(analysis_json):
    return analysis_json["meter"]


def extract_qafiah(analysis_json):
    return analysis_json["qafiyah"][1]


def process_analysis_list(analysis_json):
    analysis_list = []

    # Iterate over the analysis_json
    for i in range(0, len(analysis_json['arudi_style']), 2):
        # Extract the two parts (shatr1 and shatr2)
        shatr1 = {
            'diacritized': analysis_json['diacritized'][i // 2].split(' # ')[0],  # First part before the '#'
            'arudi_style': analysis_json['arudi_style'][i][0],  # Arudi style for shatr1
            'closest_pattern': analysis_json['closest_patterns'][i][2],  # Closest pattern for shatr1
            'patterns_mismatches': get_stylized_pattern_mismatches(analysis_json['patterns_mismatches'][i]).strip(),
            # Pattern mismatches for shatr1
            'notes': get_shatr_notes(analysis_json['arudi_style'][i][0], analysis_json['patterns_mismatches'][i])
            # Notes about shatr1
        }
        shatr2 = {
            'diacritized': analysis_json['diacritized'][i // 2].split(' # ')[1],  # Second part after the '#'
            'arudi_style': analysis_json['arudi_style'][i + 1][0],  # Arudi style for shatr2
            'closest_pattern': analysis_json['closest_patterns'][i + 1][2],  # Closest pattern for shatr2
            'patterns_mismatches': get_stylized_pattern_mismatches(analysis_json['patterns_mismatches'][i + 1]).strip(),
            # Pattern mismatches for shatr2
            'notes': get_shatr_notes(analysis_json['arudi_style'][i + 1][0],
                                     analysis_json['patterns_mismatches'][i + 1])  # Notes about shatr2
        }

        # Append the shatr1 and shatr2 into analysis_list
        analysis_list.append({
            'shatr1': shatr1,
            'shatr2': shatr2
        })

    return analysis_list


def get_shatr_notes(arudi_style, pattern_mismatches):
    mismatches = find_mismatches_right_to_left(arudi_style, pattern_mismatches)
    formatted_errors = [
        f"{mismatch['error']} في كلمة {mismatch['word']}. \n\n"
        for mismatch in mismatches
    ]
    return " ".join(formatted_errors)


# Function to identify mismatched words from right to left
def find_mismatches_right_to_left(arudi_style, pattern_mismatch):
    print(pattern_mismatch)
    # Define the mapping for mismatch interpretation
    mismatch_meanings = {
        'G': 'الوزن صحيح',
        'R': 'كسر في الوزن لزيادة حرف',
        'B': 'كسر في الوزن لنقص حرف',
        'Y': 'كسر في الوزن لاختلاف الحركة'
    }
    errors = []
    # Clean up the text by removing short vowels and Shadda for proper alignment
    clean_text = re.sub(r'[ًٌٍَُِّْ]', '', arudi_style)  # Remove short vowels and Shadda
    words = clean_text.split()

    pattern_mismatch_list = []

    # Track the character index starting from the right
    char_index = 0

    # Loop through words to extract corresponding pattern
    for word in words:
        word_start_index = char_index
        word_end_index = word_start_index + (len(word) * 2)
        pattern_mismatch_list.append(pattern_mismatch[word_start_index:word_end_index])
        char_index = word_end_index

    # Loop through pattern mismatch list to find index of mismatch
    for index, pattern in enumerate(pattern_mismatch_list):
        if 'R' in pattern:
            error_message = mismatch_meanings['R']
            err_word = words[index]
            errors.append({"error": error_message, "word": err_word})
        elif 'B' in pattern:
            error_message = mismatch_meanings['B']
            err_word = words[index]
            errors.append({"error": error_message, "word": err_word})
        elif 'Y' in pattern:
            error_message = mismatch_meanings['Y']
            err_word = words[index]
            errors.append({"error": error_message, "word": err_word})
    return errors


def get_stylized_pattern_mismatches(pattern_mismatches):
    # Define the mapping
    mappings = {
        'G1': ('/', 'black'), 'G0': ('0', 'black'),
        'R1': ('/', '#C55A11'), 'R0': ('0', '#C55A11'),
        'Y1': ('/', '#8EC000'), 'Y0': ('0', '#8EC000'),
        'B1': ('↑', '#FF9900'),
        'B0': ('↑', '#FF9900')
    }

    # Generate HTML output for patterns_mismatches
    html_output = ""
    for i in range(0, len(pattern_mismatches), 2):
        code = pattern_mismatches[i:i + 2]
        if code in mappings:
            symbol, color = mappings[code]
            html_output += f'<span style="color: {color};">{symbol}</span> '

    return html_output


if __name__ == '__main__':
    app.run(debug=True)
