import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict
import ollama
from supervised.cache import papers

class OllamaSummarizer:
    def __init__(self, model_name: str = "dolphin-mistral:latest"):
        self.model_name = model_name

    async def generate_summary(self, text: str) -> str:
        prompt_template = (
            "Please provide a one sentence summary of the following academic paper abstract. "
            "15 words or less in an ELI5 manner.\n\n{text}\n\nSummary:"
        )
        prompt = prompt_template.format(text=text)

        try:
            with ThreadPoolExecutor() as executor:
                response = await asyncio.get_event_loop().run_in_executor(
                    executor,
                    lambda: ollama.chat(
                        model=self.model_name,
                        messages=[{"role": "user", "content": prompt}],
                    ),
                )
            return response["message"]["content"]
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return ""

    async def batch_summarize(self, texts: List[str]) -> List[str]:
        tasks = [self.generate_summary(text) for text in texts]
        return await asyncio.gather(*tasks)

    async def summarize_papers(self, papers: List[Dict]) -> List[Dict]:
        summaries = await self.batch_summarize([paper["abstract"] for paper in papers])
        
        summarized_papers = []
        for paper, summary in zip(papers, summaries):
            paper_copy = paper.copy()
            paper_copy["summary"] = summary
            summarized_papers.append(paper_copy)
        
        return summarized_papers

async def main():
    summarizer = OllamaSummarizer(model_name="llama2:latest")
    recent_papers = papers["recent_papers"]
    summarized_papers = await summarizer.summarize_papers(recent_papers)
    
    for paper in summarized_papers:
        print(f"Title: {paper['title']}")
        print(f"Summary: {paper['summary']}\n")

if __name__ == "__main__":
    asyncio.run(main())