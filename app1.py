import os
import streamlit as st
import requests
from groq import Groq
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Define the EnhancedResearchAgent class for interacting with SerpApi
class EnhancedResearchAgent:
    def __init__(self):
        # Backend API key setup for SerpApi
        self.api_key = "5402a7bfd62fcf4fa0b44ea525ce9b7093938358b0c62f86757ee96f82b6815e"  # Replace with your actual API key
        self.base_url = "https://serpapi.com/search"

    def search(self, query, num_results=10):
        """
        Perform a search query using SerpApi.
        """
        params = {
            "q": query,
            "api_key": self.api_key,
            "num": num_results,
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data: {e}")
            return None

    def gather_data(self, industry):
        """
        Gather data about AI and ML applications in a specific industry.
        """
        queries = {
            "trusted_reports": f"AI and digital transformation {industry} McKinsey Deloitte Nexocode report",
            "specific_use_cases": f"AI applications in {industry} manufacturing or operations",
            "industry_trends": f"Emerging trends in AI adoption in {industry} (2024)",
        }

        results = {}
        for key, query in queries.items():
            results[key] = self.search(query)
        return results

    def generate_summary(self, data):
        """
        Generate a summary with actionable insights.
        """
        summary = []
        for key, result in data.items():
            if not result:
                summary.append(f"No results found for {key}.")
                continue
            summary.append(f"### {key.replace('_', ' ').title()} ###")
            for i, item in enumerate(result.get("organic_results", []), start=1):
                title = item.get("title", "No Title")
                link = item.get("link", "No Link")
                snippet = item.get("snippet", "No Snippet")
                summary.append(f"{i}. **{title}**\n   {snippet}\n   [Read more]({link})\n")
        return "\n".join(summary)

    @staticmethod
    def generate_pdf(content, filename="summary.pdf"):
        """
        Generate a PDF from the summary content.
        """
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setFont("Helvetica", 10)
        width, height = letter
        y = height - 30
        line_height = 12

        for line in content.split("\n"):
            if y <= 30:  # Create a new page if content overflows
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = height - 30
            pdf.drawString(30, y, line)
            y -= line_height

        pdf.save()
        buffer.seek(0)
        return buffer
    
    @staticmethod
    def save_use_cases_to_file(use_cases, filename="use_cases.txt"):
        """
        Save generated use cases to a text file.
        """
        with open(filename, "w", encoding="utf-8") as file:
            file.write(use_cases)

# Groq Client for Generating Use Cases
class GroqUseCaseAgent:
    def __init__(self):
        # Groq API key setup
        self.client = Groq(api_key="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")

    def generate_use_case(self, research_summary):
        """
        Use Groq API to generate use cases based on the research summary.
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"Generate AI use cases based on the following research summary:\n\n{research_summary}",
                    }
                ],
                model="llama3-8b-8192",  # Choose the model you prefer
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            st.error(f"Error generating use cases with Groq: {e}")
            return None

# Streamlit App
def main():
    st.title("AI-Driven Research and Use Case Generation Tool")
    st.subheader("Generate AI-driven use cases for companies and industries")
    
    # Input fields
    company_name = st.text_input("Enter the Company Name:")
    industry = st.text_input("Enter the Industry:")
    
    if st.button("Analyze"):
        if not company_name or not industry:
            st.error("Please provide all required inputs.")
        else:
            # Gather research data using SerpApi
            st.info("Gathering data... This may take a while.")
            agent = EnhancedResearchAgent()
            research_data = agent.gather_data(industry)
            
            # Generate a research summary
            st.header("Research Summary")
            summary_report = agent.generate_summary(research_data)
            st.markdown(summary_report)
            
            # Generate use cases based on the research summary using Groq
            groq_agent = GroqUseCaseAgent()
            use_cases = groq_agent.generate_use_case(summary_report)
            
            # Display generated use cases
            if use_cases:
                st.header("Generated Use Cases")
                st.markdown(use_cases)

                # Save the use cases to a text file
                filename = f"{company_name}_use_cases.txt"
                agent.save_use_cases_to_file(use_cases, filename)
                st.success(f"Use cases saved to {filename}")

            # Generate PDF of the research summary
            pdf_buffer = agent.generate_pdf(summary_report)

            # Option to download PDF
            st.download_button(
                label="Download Research Summary as PDF",
                data=pdf_buffer,
                file_name=f"{company_name}_research_summary.pdf",
                mime="application/pdf"
            )

    # Button to open another app or page
    if st.button("Download Dataset Links"):
        st.write("Opening app2.py...")
        os.system("streamlit run app2.py")

if __name__ == "__main__":
    main()
