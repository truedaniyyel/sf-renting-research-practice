# SF Renting Research Practice

![Python](https://img.shields.io/badge/Python-3.14%2B-blue)
![Selenium](https://img.shields.io/badge/Selenium-Automation-green)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-Scraping-yellow)

This tool scrapes real estate listings from a Zillow-clone portal and automatically puts them into a Google Form.

## Key Features
* **Data Cleaning** Automatically parses raw HTML strings, stripping newlines, pipe symbols (`|`), and messy suffixes (`+ 1bd`, `/mo`) before storage.

## Tech Stack
* **Extraction:** Python `requests` & `BeautifulSoup4`
* **Automation:** Selenium WebDriver (Chrome)
* **Target:** Google Forms

## Process Architecture
```mermaid
graph TD
    Start([Start Script]) -->|HTTP GET| Website[Zillow Clone]
    
    subgraph Scraping_Phase [Phase 1: Extraction & Cleaning]
        direction TB
        Website -->|Raw HTML| Soup[BeautifulSoup Parser]
        Soup -->|Select| Cards[.StyledPropertyCard]
        Cards -->|Iterate| Extractor{Extract Data}
        Extractor -->|Clean| Address[Address String]
        Extractor -->|Clean| Price[Price String]
        Extractor -->|Clean| Link[Href Link]
        Address & Price & Link --> Dict[Dictionary Object]
        Dict --> List[(Clean Data List)]
    end

    subgraph Automation_Phase [Phase 2: Data Entry]
        direction TB
        List -->|Loop| Driver[Selenium WebDriver]
        Driver -->|Open| Form[Google Form]
        Form -->|Input| Fields[Fill Inputs]
        Fields -->|Click| Submit[Submit Button]
        Submit -->|Click| LoopLink[Submit Another Response]
        LoopLink -.-> Fields
    end
```

## How to Run Locally


### 1. Clone the repository
```bash
git clone [https://github.com/truedaniyyel/sf-renting-research-practice.git](https://github.com/truedaniyyel/sf-renting-research-practice.git)
cd sf-renting-research-practice
```

### 2. Install Dependencies
This project uses uv for modern package management.
```bash
uv sync
```

### 3. Configuration
1. Create a Google Form with 3 Short Answer questions:
   * Address
   * Price
   * Link
2. Create a `.env` file in the root directory and add your Google Form URL:
```env
GOOGLE_FORM_URL=YOUR_GOOGLE_FORM_LINK_HERE
```

### 4. Run the Bot
The script will open a Chrome window, scrape the data in the background, and begin filling the form automatically.
```bash
python main.py
```