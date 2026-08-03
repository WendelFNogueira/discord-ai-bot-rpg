# Discord RPG Bot

## Overview
This project is a Python-based Discord bot designed for tabletop RPG sessions with friends. The bot acts as a merchant, providing information about items, weapons, armor, potions, and more upon request. It integrates AI models for local or server-based execution and uses Stable Diffusion for generating images, maps, and other visual assets. The bot also includes dice rolling commands and has the potential to monitor gameplay rules and validate player actions.

## Features

### Merchant Simulation
- Retrieves information about items from a local wiki storage (Tormenta20).
- Parses and processes HTML content to extract relevant details.
- Provides item attributes, values, and descriptions to players.

### AI Integration
- Utilizes the Ollama server to run AI models locally or on a server.
- Generates responses based on prompts, such as filling out character sheets.

### Image Generation
- Integrates Stable Diffusion to create images, maps, and other visual assets for RPG sessions.

### Dice Rolling
- Includes commands for rolling dice, supporting various RPG mechanics.

### Music Playback
- Plays music from YouTube links in voice channels.
- Supports queueing, skipping, and stopping songs.

### Future Improvements
- Add commands to fetch specific gameplay rules.
- Accept audio input to "listen" during sessions and respond to queries.
- Validate player actions by checking dice rolls and mana costs against character sheets.

## Setup

### Prerequisites
- Python 3.10 or higher
- Discord bot token
- Stable Diffusion model files
- Ollama server for AI integration

### Installation
1. Clone the repository:
   ```cmd
   git clone <repository-url>
   ```
2. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
3. Configure the bot:
   - Add your Discord bot token to `config.py`.
   - Set the Ollama server URL in `config.py`.

### Running the Bot
Start the bot with the following command:
```cmd
python main.py
```

## Commands

### General
- `/ajuda`: Lists all available commands and their functionalities.

### Merchant
- `/preencher_ficha <data>`: Guides players on how to fill out their character sheets based on the Tormenta20 book.

### Music
- `/play <URL>`: Plays a song from a YouTube URL.
- `/skip`: Skips the current song.
- `/stop`: Stops playback and disconnects the bot.

### Dice Rolling
- Commands for rolling dice (e.g., `/roll d20`).

## File Structure
- `main.py`: Entry point for the bot.
- `commands/`: Contains command modules (e.g., merchant, music, dice rolling).
- `utils/`: Utility scripts for tasks like extracting wiki text.
- `data/`: Stores local data such as the Tormenta20 wiki content.
- `stable-diffusion-model/`: Contains model files for image generation.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests to improve the bot.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Architectural Decisions

### Why This Architecture?
The bot's architecture was designed to be modular and extensible, ensuring that new features and commands can be added with minimal impact on existing functionality. Key decisions include:

- **Command-Based Structure**: Each feature is implemented as a separate command module under the `commands/` directory. This keeps the code organized and allows for easy debugging and testing of individual features.
- **Event-Driven Design**: The bot leverages Discord's event-driven API to respond to user interactions efficiently.
- **Integration with External Tools**: The use of Stable Diffusion and Ollama ensures that the bot can handle advanced tasks like image generation and AI-driven responses locally or on a server.
- **Local Data Storage**: Storing the Tormenta20 wiki content locally in the `data/` directory ensures quick access to information without relying on external APIs during gameplay.

### Testing and Validation
- **Manual Testing**: Each command is manually tested in a controlled Discord server to ensure it behaves as expected.
- **Error Handling**: The bot includes error handling for external integrations (e.g., Stable Diffusion, Ollama) to provide meaningful feedback to users in case of issues.
- **Future Plans for Automated Testing**: The project aims to include unit tests for critical components, such as the `utils/extract_wiki_text.py` script and command modules, to ensure reliability and prevent regressions.

### Scalability
The modular design allows the bot to scale easily. For example:
- New commands can be added by creating additional modules in the `commands/` directory.
- The bot can be deployed on a server to handle larger Discord communities.

### Security Considerations
- **Token Management**: The bot token and other sensitive information are stored in `config.py`, which should be excluded from version control.
- **Rate Limiting**: The bot respects Discord's rate limits to avoid being banned.
- **Input Validation**: Commands validate user input to prevent unexpected behavior or crashes.

### AI Models Used

This project integrates two key AI models to enhance its functionality:

- **Ollama (Mistral Model)**:
  - **Purpose**: Used for generating text-based responses, such as guiding players on how to fill out character sheets.
  - **Reason for Choice**: The Mistral model is lightweight and efficient, making it suitable for local execution or server deployment. It provides high-quality natural language generation, which is essential for creating immersive RPG experiences.

- **Stable Diffusion**:
  - **Purpose**: Used for generating images, maps, and other visual assets to enrich RPG sessions.
  - **Reason for Choice**: Stable Diffusion is a state-of-the-art model for image generation. It is open-source, highly customizable, and capable of running on local hardware, making it ideal for generating unique and context-specific visuals during gameplay.
