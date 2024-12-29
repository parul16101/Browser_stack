This project automates the process of scraping articles from the **Opinion** section of the El País website. It performs the following tasks:

1. **Fetch and Display Articles**:
   - Scrape the first five articles from the Opinion section.
   - Print their titles and content in Spanish.
   - Download and save cover images, if available.

2. **Translate Article Headers**:
   - Translate article titles to English using the Google Translate API.
   - Print translated headers.

3. **Analyze Translated Headers**:
   - Identify words repeated more than twice across all translated headers.
   - Print each repeated word along with the count of occurrences.

4. **Cross-Browser Testing**:
   - Verify the solution locally.
   - Execute the script on **BrowserStack** across five parallel threads, testing various browser and device combinations.
