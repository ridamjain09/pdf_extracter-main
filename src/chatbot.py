from sentence_transformers import SentenceTransformer
import pinecone
import openai
from src.logger import logger

class InsuranceChatbot:
    def __init__(self, data_file):
        # Initialize model and Pinecone
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        pinecone.init(api_key="your-pinecone-api-key")
        self.index = pinecone.Index("document-index")

        # Load the text data
        with open(data_file, 'r') as file:
            self.data = file.read()
        
        logger.info("Chatbot initialized with data.")
    
    def store_data_in_vector_db(self):
        # Split data into sections
        sections = self.data.split("\n\n")
        for section in sections:
            embedding = self.model.encode(section)
            self.index.upsert([(section, embedding)])
        logger.info("Stored data in vector DB.")

    def ask_question(self, question):
        # Encode the question and search Pinecone for relevant sections
        query_embedding = self.model.encode(question)
        result = self.index.query([query_embedding], top_k=3)
        
        # Use OpenAI to generate a response based on the retrieved sections
        openai.api_key = "your-openai-api-key"
        relevant_sections = " ".join([match['metadata']['text'] for match in result['matches']])
        prompt = f"Use the following information to answer the user's question:\n\n{relevant_sections}\n\nUser's query: {question}"
        
        response = openai.Completion.create(
            engine="text-davinci-003", prompt=prompt, max_tokens=150
        )
        return response.choices[0].text.strip()

if __name__ == "__main__":
    bot = InsuranceChatbot('./data/cleaned_policy.txt')
    bot.store_data_in_vector_db()
    print(bot.ask_question("What is the model number of the device?"))
