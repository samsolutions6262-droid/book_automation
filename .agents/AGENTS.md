# Book Summarization Rules

When generating page-by-page summaries from a PDF, follow these instructions:

1. **PROCESSING UNIT**: Treat each page of the book as one unit of summarization.

2. **CHAPTER LABELING**: Label each page's summary sequentially as "Chapter 1", "Chapter 2", "Chapter 3", and so on — one label per page, regardless of the book's actual chapter structure.

3. **LENGTH**: Each page summary must contain approximately 250 words, focusing only on the most important words, ideas, facts, and points from that page. Do not pad with filler.

4. **CONTENT STYLE**: Write the summary as if it is the original condensed content itself. Do NOT:
   - Mention that a summary was created
   - Mention that an AI generated it
   - Use phrases like "here is the summary," "this page discusses," "summary of page X," or any meta-commentary
   - Reference the summarization process at all
   
   Instead, jump directly into the substantive content and key points, written in clear, direct prose.

5. **BATCH PROCESSING**: If the book is long, process it in batches of 10–20 pages at a time. After completing each batch:
   - Present the chapter-labeled summaries for that batch
   - Pause and ask the user for confirmation before proceeding to the next batch
   - This ensures quality control and avoids exceeding length limits

6. **CONSISTENCY**: Maintain consistent tone, terminology, and chapter numbering across all batches throughout the entire book, continuing the chapter count from where the previous batch left off.

7. **ACCURACY**: Do not invent, embellish, or add information not present in the original page. Stay faithful to the source content.
