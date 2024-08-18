# AI Voice Assistant Headstarter Hackathon

This project is a Flask-based AI voice assistant that utilizes various libraries and APIs to recognize speech commands, perform actions, and provide responses. It incorporates text-to-speech, speech recognition, and various external services to enhance functionality.
# Demo
https://www.loom.com/share/e0d017c7e8ba4701bd898e033406b62d?sid=9c9a19f2-a12d-4579-a956-c35d605153f1

## Features

- **Speech Recognition**: Recognizes and processes voice commands using Google Speech Recognition.
- **Text-to-Speech**: Converts text responses into spoken words using Microsoft SAPI and other methods.
- **Email Handling**: Opens the default email client and pre-fills recipient, subject, and body fields.
- **Weather Information**: Fetches and provides weather information for the user's location.
- **Location Information**: Retrieves and announces the user's current city.
- **News Headlines**: Retrieves and reads out the latest news headlines.
- **Text Messaging**: Sends SMS messages using Twilio's API.
- **Sound Playback**: Plays a custom sound that simulates water waves.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   Make sure the `requirements.txt` file includes:
   ```
   Flask
   SpeechRecognition
   pyttsx3
   requests
   google-generativeai
   sounddevice
   scipy
   gtts
   twilio
   pywin32
   python-dotenv
   numpy
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the project root and add the following environment variables:

   ```
   GEMINI_API_KEY=your_gemini_api_key
   NEWS_API=your_news_api_key
   WEATHER_API_KEY=your_weather_api_key
   LOCATION_TOKEN=your_location_token
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   AUTH_TOKEN=your_twilio_auth_token
   ```

## Usage

1. **Run the Application**

   ```bash
   python app.py
   ```

2. **Access the Assistant**

   Open your web browser and navigate to `http://127.0.0.1:5000` to interact with the voice assistant.

## Some Commands

- **Greet**: "hi", "hello", "hey"
- **Goodbye**: "goodbye", "bye"
- **Weather**: "weather", "temperature"
- **Location**: "location", "where am I"
- **Time**: "time", "current time"
- **Send Email**: "email"
- **Play Sound**: "play music", "play sound"
- **Get News**: "news", "headline"
- **Send SMS**: "send text", "text message"

## Dependencies

- Flask: Web framework for building the web application.
- SpeechRecognition: Recognizes speech and converts it to text.
- pyttsx3: Text-to-speech conversion library.
- Requests: HTTP library for making API calls.
- Google Generative AI: AI model for generating content (ensure compatibility with provided API key).
- Sounddevice and SciPy: For generating and playing sounds.
- gTTS: Google Text-to-Speech library.
- Twilio: For sending SMS messages.
- pywin32: For Windows-specific COM interface and text-to-speech.
- SQLite: Database for storing interactions.

## Troubleshooting

- **Audio Issues**: Ensure you have the necessary audio drivers and libraries installed.
- **API Keys**: Double-check that all API keys and tokens are correctly set in the `.env` file.
- **Database Issues**: Ensure the SQLite database file can be accessed and written to.

## Contributing

Feel free to submit issues, feature requests, or pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
