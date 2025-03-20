# NeuroTech Hackathon - Focus EEG

An advanced brain-computer interface application that leverages the Muse portable EEG headset to detect, classify, and monitor attention states in real-time. This system enables users to understand their focus patterns, receive immediate feedback on cognitive states, and improve their attention through data-driven insights.

![Muse Headset](https://github.com/jknudstrup/focus-eeg/blob/master/assets/muse.jpg?raw=true)

## Project Overview

Focus EEG uses machine learning to differentiate between attentive and non-attentive mental states. By recording brainwave data through the Muse EEG headset, the application processes the signals in real-time to deliver instantaneous classification of your cognitive state. This enables users to identify when their attention wanes, recognize patterns in their focus, and develop strategies to maintain concentration during important tasks.

## Core Features

- **Real-time EEG Monitoring**: Continuous collection and processing of brainwave data
- **ML-Based Classification**: Advanced algorithms to identify attentive vs. non-attentive states
- **Live Prediction Stream**: Immediate feedback on current cognitive state
- **Custom Model Training**: Personalized classifier for improved accuracy
- **Comprehensive Signal Processing**: Robust preprocessing of EEG data
- **Interactive Data Labeling**: Simple system for generating training data
- **Focus Analytics**: Detailed patterns of attention over time

## Technical Architecture

The application consists of several interconnected components:

1. **Data Acquisition**: Uses the Muse headset and SDK to collect raw EEG signals
2. **Signal Preprocessing**: Filters and processes raw brainwave data 
3. **Feature Extraction**: Identifies relevant patterns in the EEG signals
4. **Classification**: Applies machine learning to categorize cognitive states
5. **Feedback System**: Delivers real-time information on attention levels

## Prerequisites

### Hardware Requirements
- **Muse EEG Headset**: Any version compatible with Muse SDK
- **MacOS Computer**: Primary development platform (adaptable to other OS with modifications)

### Software Requirements
- **Python 3.x**: Core programming language
- **Muse SDK**: For headset communication
- **pyliblo**: OSC server functionality
- **Python Dependencies**: NumPy, SciPy, scikit-learn, etc.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/neurotechhackathon.git
cd neurotechhackathon
```

2. Install the Muse SDK:
   - Follow the [official guide](https://sites.google.com/a/interaxon.ca/muse-developer-site/developer-getting-started-guide)
   - Ensure proper driver installation for your headset model

3. Set up Python environment and dependencies:
```bash
python -m venv openai-env
source openai-env/bin/activate  # On Windows: openai-env\Scripts\activate
pip install numpy scipy scikit-learn matplotlib pyliblo
```

## Project Structure

```
focus-eeg-master/
├── assets/                 # Project images and documentation resources
├── openai-env/            # Python virtual environment
├── preprocessing/         # Signal processing and data preparation scripts
├── settings.py           # Configuration and path settings
├── train.py              # Machine learning model training
├── classifier_osc_server.py # Real-time classification server
├── build_frame.py        # Data frame construction utilities
└── nvidia_hackathon.py   # Main application script
```

## Usage Guide

### Step 1: Data Collection

```bash
# Start Muse data streaming
muse-io --device Muse --osc osc.udp://localhost:5001,osc.udp://localhost:5002

# Record EEG data to CSV
muse-player -i /muse/elements/delta_absolute /muse/elements/theta_absolute /muse/elements/alpha_absolute /muse/elements/beta_absolute /muse/elements/is_good /muse/elements/blink /muse/elements/jaw_clench -l udp:5002 -C Recordings/Unlabeled/$(date +%s).csv
```

### Step 2: Training Data Labeling

1. Execute the labeling script:
```bash
python labeler.py
```

2. Engage in attention-demanding tasks (reading, studying, problem-solving)
3. Press any key when you notice your attention wandering
4. Press Esc to end the labeling session

### Step 3: Model Training

```bash
python train.py
```
This processes your labeled data and creates a personalized classification model.

### Step 4: Real-time Attention Monitoring

1. Launch the classification server:
```bash
python classifier_osc_server.py
```

2. Continue with normal activities while wearing the Muse headset
3. The system will monitor in real-time:
   - Current attention level
   - Transitions between focus states
   - Duration of attentive/non-attentive periods

### Step 5: Data Analysis

- View real-time attention levels in the terminal
- Review session data to identify patterns
- Use insights to improve focus strategies

## Attention Model

The project uses a sophisticated cognitive model based on brainwave patterns:

![Attention Model](https://github.com/jknudstrup/focus-eeg/blob/master/assets/attention.png?raw=true)

## System Workflow

![Workflow](https://github.com/jknudstrup/focus-eeg/blob/master/assets/flowchart.png?raw=true)

## Best Practices

### Headset Setup
- Ensure proper electrode contact with scalp
- Verify signal quality indicators before recording
- Minimize electrical interference in your environment
- Position headset according to manufacturer guidelines

### Data Collection
- Maintain consistent testing environment
- Label attention states accurately during training
- Collect sufficient samples of both cognitive states
- Record data during various activities and times of day

### Model Training
- Use minimum 10 minutes of data per attention state
- Validate classifier accuracy before relying on predictions
- Retrain periodically as your attention patterns evolve
- Include diverse activities in your training data

### Attention Monitoring
- Start in a distraction-free environment
- Take regular breaks to prevent mental fatigue
- Note external factors that affect your attention
- Use the focus analytics to identify optimal working periods

## Technical Details

### Signal Processing
The system processes four primary brainwave frequency bands:
- **Delta** (0.5-4 Hz): Associated with deep sleep
- **Theta** (4-8 Hz): Related to drowsiness and meditation
- **Alpha** (8-13 Hz): Present during relaxed wakefulness
- **Beta** (13-30 Hz): Dominant during active thinking

### Classification Algorithm
- Uses supervised machine learning trained on labeled data
- Extracts time and frequency domain features from EEG signals
- Applies normalization and dimensionality reduction
- Classifies using ensemble methods for robust predictions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Interaxon for the Muse SDK and hardware
- Original focus-eeg project contributors
- NeuroTech community for inspiration and support

## Support

For questions or issues:
1. Open an issue in the GitHub repository
2. Check existing documentation in the project
3. Review closed issues for similar problems and solutions

## Future Development

- Mobile application for portable monitoring
- Extended classification of multiple cognitive states
- Advanced visualization of attention patterns
- Integration with productivity applications
- Long-term attention tracking and analysis
- Biofeedback training modules

---
*This project was developed as part of a NeuroTech Hackathon and is intended for research and educational purposes.* 