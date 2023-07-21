# AliceBob: improve vocabulary through the Alias game

This repo contains demo for Rasa LLM Challenge competition

## Motivation

A good vocabulary is requirement for language skill. One popular and effective way to develop vocabulary is flash cards. But it's boring and easy to exploit memorizing word description instead of actual meaning. 

Word games are interactive, practice oriented and much more difficult. So it's better for learning purpose. The downside is that games requires partners. 

The goal of my project is to develop assistant that available to help learners to expand their vocabulary through popular word game Alias. Chatbot can play both sides: guess and explain words. Assistant is available as telegram bot. But you have to provide openai API token to use it.

## How it works

The game has two players. Player A explains a given word and player B should guess this word. You can play both sides. The second player (called Bob) is powered by openai's ChatGPT. Alice (manage games) will ask your language level to adapt game's difficulty. 

In this demo the words and topics are selected randomly according to student level. You can also ask Bob to explain the meaning of the word or construction he uses. Bob does not correct spelling or language levels, but you can ask him to do this.

## How to run

1. install required packages (requirements.txt)

2. [connect](https://rasa.com/docs/rasa/connectors/telegram) to telegram and [setup](https://rasa.com/docs/rasa/messaging-and-voice-channels/#testing-channels-on-your-local-machine) ngrok

3. [train](https://rasa.com/docs/rasa/command-line-interface#rasa-train) model

4. set variables

    ```
    export OPENAI_API_BASE="<API_PATH>"
    export OPENAI_API_KEY="<API_KEY>"
    ```

5. [run](https://rasa.com/docs/rasa/command-line-interface#rasa-run) server & actions