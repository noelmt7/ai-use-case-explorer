import re
import streamlit as st

# Define use case keywords
use_case_keywords = {
    "Quality Control": ["defects", "inspection", "computer vision", "machine learning", "quality"],
    "Predictive Maintenance": ["sensor data", "predictive", "maintenance", "machine learning", "downtime"],
    "Supply Chain Optimization": ["supplier", "inventory", "logistics", "costs", "performance"],
    "Autonomous Vehicle Development": ["autonomous", "driving systems", "navigate", "traffic", "safety"],
    "Vehicle Design": ["generative AI", "design", "optimize", "fuel efficiency", "emissions"],
    "Real-time Traffic Prediction": ["traffic prediction", "optimize", "congestion", "safety"],
    "Personalized Driving Experiences": ["infotainment", "preferences", "personalized", "driving experience"],
    "Advanced Driver-Assistance Systems (ADAS)": ["lane departure", "adaptive cruise", "automatic emergency braking", "sensors"],
    "EV Charging Optimization": ["EV charging", "energy consumption", "efficiency"],
    "Cybersecurity": ["cyber threats", "security", "threat detection", "response systems"],
    "Electronic Logging Devices (ELDs)": ["logging", "compliance", "driver hours", "inspection"],
    "Automotive Seat Adjustment": ["seat adjustment", "comfort", "fatigue", "performance"],
    "Vehicle-to-Everything (V2X) Communication": ["V2X", "communication", "safety", "infrastructure"],
    "Predictive Analytics": ["predictive analytics", "vehicle data", "maintenance", "reliability"],
    "Human-Machine Interface (HMI) Optimization": ["HMI", "interface", "preferences", "driving experience"],
}

# Function to filter relevant use cases
def filter_use_cases(text, keywords_dict):
    filtered_lines = []
    for line in text.splitlines():
        for keywords in keywords_dict.values():
            if any(re.search(rf'\b{keyword}\b', line, re.IGNORECASE) for keyword in keywords):
                # Extract the first 3-4 relevant words/phrases from the line
                words = line.split()
                filtered_line = " ".join(words[:4])  # Keep only the first 3-4 words
                
                # Clean the filtered line by removing ** and ""
                filtered_line = re.sub(r'\*\*|\\"|\\"', '', filtered_line)
                
                filtered_lines.append(filtered_line)
                break
    return filtered_lines

# Function to search GitHub repositories
def search_github_repos(query):
    important_keywords = extract_important_keywords(query)
    github_results = get_github_repos(important_keywords)
    search_results = [f"GitHub Repositories for '{important_keywords}':"]
    search_results.extend(github_results)
    return search_results

def extract_important_keywords(query):
    query = query.lower()
    query = re.sub(r"(based on the research|on the research|research|ai-powered)", "", query)
    query = " ".join(query.split())
    return query

def get_github_repos(query):
    github_repos = [
        f"[Repo 1: {query} on GitHub](https://github.com/search?q={query.replace(' ', '+')})"
    ]
    return github_repos

# Save results to a markdown file
def save_results_to_file(results, filename="dataset_links.md"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("# Relevant Dataset Links\n\n")
        for result in results:
            file.write(f"- {result}\n")

# Streamlit App
def main():
    st.title("AI Use Case Filter and Dataset Finder")
    
    # File upload
    uploaded_file = st.file_uploader("Upload the use cases file (text format):", type=["txt"])
    
    if uploaded_file:
        # Read the uploaded file
        use_cases = uploaded_file.read().decode("utf-8")
        st.subheader("Uploaded Use Cases")
        st.text_area("Original Use Cases", use_cases, height=200)
        
        # Automatically filter use cases to get 3-4 word results
        filtered_use_cases = filter_use_cases(use_cases, use_case_keywords)
        st.subheader("Filtered Use Cases (3-4 words)")
        if filtered_use_cases:
            for line in filtered_use_cases:
                st.write(f"- {line}")
        else:
            st.write("No relevant use cases found.")
        
        # Search datasets using filtered text
        if st.button("Search for Datasets"):
            st.info("Searching for datasets...")
            search_results = []
            for line in filtered_use_cases:
                search_results.extend(search_github_repos(line.strip()))
            
            st.subheader("Search Results")
            for result in search_results:
                st.markdown(f"- {result}")
            
            # Save results to a file
            save_results_to_file(search_results)
            st.success("Dataset links saved to `dataset_links.md`")
            
            # Allow downloading the markdown file
            with open("dataset_links.md", "r", encoding="utf-8") as file:
                markdown_content = file.read()
            st.download_button(
                label="Download Dataset Links",
                data=markdown_content,
                file_name="dataset_links.md",
                mime="text/markdown"
            )

if __name__ == "__main__":
    main()
