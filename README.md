# 🌙 AI Dream Analyzer

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)

**AI Dream Analyzer** is an AI-powered application that interprets and analyzes dreams using advanced natural language processing models.

<img width="960" alt="Screenshot 2025-03-15 174621" src="https://github.com/user-attachments/assets/605bca5f-2f88-4ada-9f99-e32092d5d449" />
<img width="960" alt="Screenshot 2025-03-15 175110" src="https://github.com/user-attachments/assets/ab56de09-eb63-4b3c-b1a5-f5878fe6cc5e" />
<img width="959" alt="Screenshot 2025-03-15 175146" src="https://github.com/user-attachments/assets/bbdf968f-2c61-468f-980f-cd77cee4f8b2" />
<img width="959" alt="Screenshot 2025-03-15 175233" src="https://github.com/user-attachments/assets/78610830-32fe-46ca-ba59-ba4168cac83d" />


---

## ✨ Features

- 💤 AI-driven dream interpretation
- 🎭 Sentiment and emotional analysis
- 🧠 Contextual meaning extraction
- 🎨 Simple and intuitive Streamlit interface
- 📄 Download dream reports

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAi API key (for dream analysis)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/talharauf15/AI-Dream-Analyzer.git
cd AI-Dream-Analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Configure API Key Securely

Before running the app, store your OpenAI API key securely:
1. Create a `.streamlit/secrets.toml` file:
   ```toml
   [secrets]
   OPENAI_API_KEY = "your-api-key-here"
   ```
2. **Do not push `secrets.toml` to GitHub!** Add it to `.gitignore` to keep it private.

### Usage

Run the application locally:
```bash
python -m streamlit run app.py
```

## 🛠️ How to Use

1. Open the app in your browser.
2. Enter your dream description.
3. Click "Analyze Dream" to generate insights.
4. View AI-powered analysis and interpretations.
5. Download or share the dream report.

## 📚 Tech Stack

- **Python** (Core language)
- **Streamlit** (Frontend UI)
- **OpenAI API** (Dream interpretation)
- **NLTK & SpaCy** (Natural Language Processing)

## 🌟 Roadmap

- [ ] Add multilingual support
- [ ] Improve accuracy with larger AI models
- [ ] Integrate dream symbolism database
- [ ] Provide personalized dream recommendations

## 🤝 Contributing

Contributions are welcome! Follow these steps:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -m 'Add NewFeature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- OpenAI for NLP capabilities
- Streamlit for interactive UI framework

## ⚠️ Disclaimer

- AI-based dream interpretations are experimental and for entertainment purposes.
- The accuracy of dream analysis depends on AI model capabilities and input quality.

---

📄 **License**  
MIT License - See [LICENSE](LICENSE) for details.


