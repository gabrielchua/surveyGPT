# surveyGPT

surveyGPT is a Streamlit application that integrates the power of GPT (by OpenAI) with data from CSV files. It allows users to upload their dataset and then query it with natural language, receiving insightful and human-like responses about their data.

## Features

- **Upload CSV Files**: Users can easily upload their datasets in the form of .csv files.
- **Chat Interface**: The application uses a chat-like interface for a more interactive and intuitive user experience.
- **Data Preview**: Once a file is uploaded, users can preview the first five rows of their dataset.
- **Natural Language Queries**: Powered by GPT, users can make queries about their dataset using natural language and receive relevant responses.

## Prerequisites

- Python
- Streamlit
- Pandas
- OpenAI's GPT

## Getting Started

1. **API Key**: Make sure you have an OpenAI API key. Store this key securely in `st.secrets` as `"openai_key"`.
2. **Install Dependencies**: Before running the application, make sure to install the necessary libraries.
    ```
    pip install streamlit pandas openai
    ```

3. **Run the Application**:
    ```
    streamlit run [filename].py
    ```

## How to Use

1. Start the application using the command mentioned above.
2. Upload your CSV file using the file uploader on the left sidebar.
3. Preview your dataset by expanding the "Preview Dataset" section.
4. Input your query in the chat input box. For example, if you have sales data, you might ask "Which product had the highest sales in January?".
5. Wait for the response from the assistant and continue the conversation as needed.

## Known Limitations

- The application currently supports only CSV files.
- The underlying model used is `gpt-3.5-turbo`. Adjustments or custom integrations may be necessary for other models or different use-cases.
- Ensure you handle API usage and costs efficiently as the OpenAI API isn't free.

## Feedback and Contributions

Your feedback is highly appreciated! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.
