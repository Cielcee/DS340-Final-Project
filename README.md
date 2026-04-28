# DS340-Final-Project
## The Terrier Jukebox
A generative text-based comedy RPG where you play as a college exchange student navigating the absurdities of life. Use your wit to survive social blunders, awkward language barriers, and bizarre part-time jobs.
### What the project does
The project uses an LLM (Gemini 3 Flash, for the most part) to support a generative text-based game similar to the video game series Choice of Games. Powered by the Google Gemini API and built with Streamlit, it acts as a "Game Master" that expands pre-written comedy skits into immersive RPG scenes narrated in the second person.
The game features:
- **Dynamic Storytelling**: Uses gemini-3-flash-preview to generate narratives based on your choices.
- **Humor Evaluation:** A built-in LLM "comedy writer" grades your responses on a binary scale (0 or 1) using few-shot prompting logic.
- **Branching Narratives:** Your cumulative humor score determines whether you reach a Good, Neutral, or Bad ending.
- **NPC Interaction:** Non-player characters react dynamically—either laughing with you or feeling awkward—based on how funny your input is.
### Why the project is useful
The premise behind the project is to explore natural language processing (NLP) in LLMs. Since we were both interested in video games and comedy, we thought it'd be a good idea to see if a given LLM could both (1) determine what's funny versus what's not and (2) how to tell stories in context. The result of this endeavor gives us an idea of how far LLMs have come as well as how far they have to go (if they really want to get good at natural language processing, especially with ideas like "sense of humor"). It serves as a practical example of:
- **Streamlit Integration:** Moving from a static Jupyter Notebook to a polished web-based UI.
- **Few-Shot Prompting:** Teaching an AI to evaluate subjective concepts like "humor" using specific examples.
- **State Management:** Utilizing st.session_state to maintain game history and score across multiple rounds of interaction.
### How users can get started with the project
To run the game locally, follow these steps:

**Prerequisites**
- Python installed on your system.
- A Gemini API Key.

**Installation & Execution**
1. Download the files: Ensure app.py is in your working directory.
2. Open your Terminal or PowerShell.
3. Navigate to your directory:
   
   `cd path/to/your/folder`
5. Install dependencies:
   
   `pip install streamlit google-genai`
7. Set your API Key:
   
   Windows (PowerShell): `$env:GEMINI_API_KEY = "your_api_key"`

   Mac/Linux: `export GEMINI_API_KEY="your_api_key"`
5. Run the app:
  `streamlit run app.py`
6. Exit: Press Ctrl + C in the CLI to stop the session.

### Support
Where to get help if you run into issues:
- API Hiccups: The game includes built-in error handling for API timeouts or 503 Server Errors. If the app freezes or throws an error during a turn, simply wait a few seconds and try submitting your response again.

- Streamlit UI Issues: For questions regarding the web framework, page rendering, or UI components, check out the official Streamlit Documentation.

- Environment Variables: Ensure your CLI session hasn't refreshed. If you close your terminal, you will need to re-export your GEMINI_API_KEY before running the app again.

### Contributing and Maintainers
Contributors names and contact info:

Tony Wu, tonyjwu@bu.edu

Yuwei(Celia) Gao, celiag@bu.edu

