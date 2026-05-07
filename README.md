# Research Scout Agent

## Teknologier
- Python
- Autogen
- MistralAI
- OpenAlex API
- requests
- python-dotenv

## Installation

### Klon projektet:
```bash
git clone https://github.com/AdnanOmerbasic/research-scout-agent.git
cd research-scout-agent
```
### Opret og aktiver miljø
```bash
python -m venv venv
source venv/Scripts/activate
```

### Installer nødvendige dependencies
```bash
pip install -r requirements.txt
```

### Konfigurer MISTRALAI API key
Generer nøglen via deres hjemmeside
Brug nøglen og sæt den som en env variabel

Opret en .env fil i roden af projektet

```bash
MISTRAL_API_KEY=din_api_key_her
```


## Kør agenten
```bash
python -m research_scout_agent.agent.research_scout_agent
```

## Tool
Research scout agenten bruger et custom tool "search_paper" med OpenAlex til at søge efter papers baseret på:
- topic
- year_from
- year_to
- min_citations
- max_citations
- max_papers

Det returnerer
- title
- authors
- publication year
- citation count
- url
- doi
- citation count source

## Workflow
Brugeren skriver en prompt om et research paper
Agenten udtrækker topic, year constraint og citation constraint
Agenten kalder search_paper tool
Tool'et bruger OpenAlex API
Tool'et returnerer metadata som title, authors, publication year, citation count, url, doi og abstract
Agenten vælger et paper med bedst match ud fra de returnerede resultater
Agenten returnerer enten et svar eller siger "No matching paper was found"

LLM'en:
- Forstår brugerens prompt
- Udtrækker topic, year constraint og citation constraint
- Vælger det mest relevante paper
- Returnerer det endelige svar

Koden:
- Kalder OpenAlex API
- Laver filtrering
- Parser resultatet
- Returnerer metadata som title, authors, publication year, citation count, url, doi og abstract


## Evaluering
Jeg evaluerede agenten med 10 test prompts og har brugt en systematisk tilgang 
AI agenter kan evalueres ved at teste dem på et fast sæt opgaver og vurdere, om de løser opgaven korrekt,
bruger deres tools rigtigt, følger prompts og undgår hallucinationer. 
Jeg valgte af den grund en manuel test evaluering med 10 prompts, hvor jeg vurderede agentens svar ud fra faste kriterier 
som relevans, year constraint, citation constraint, source, hallucinationer og forklaring. 

Agenten blev testet med forskellige typer prompts og blev vurderet ud fra kriterierne nedenfor

For hver prompt vurderede jeg om 
- Den fandt et relevant paper
- Overholdt year og citation constraint
- Gav gyldig source 
- Den undgik at hallucinere selv
- Sluttede af med en kort forklaring

Jeg lavede evalueringen manuelt for at se om agenten bruger tool'et korrekt og følger brugerens constraints 

Test prompts jeg anvendte:
1. Find a research paper about LLM agents for software engineering that was published after 2022 and has at least 100 citations. Explain why the paper is relevant and provide the source of the citation count.

2. Find a paper about retrieval-augmented generation published before 2021 with more than 500 citations. 
Summarize its contribution in 5-7 sentences.

3. Find a recent paper about AI agents using tools and explain whether it would be useful for someone building autonomous software agents.

4. Find a paper about Python programming published before 2021 with more than 500 citations.

5. Find a paper about DevOps published after 2018 with at least 500 citations.

6. Find a paper about software testing published after 2020 with at least 100 citations. Explain why it is relevant for software quality.

7. Find a paper about machine learning published after 2019 with at least 1000 citations.

8. Find a paper about secure software development published after 2020 with at least 50 citations.

9. Find a paper about DevSecOps published after 2020 with less than 200 citations.

10. Find a paper about agile software development published in 2001 with at least 100 citations.

### Evaluerings resultater
Prompt 1. Fandt MetaGPT fra 2023 med 134 citations 

Prompt 2. Fandt ikke noget match

Prompt 3. Fandt et nyeligt paper om AI agents - Den kunne have været mere relevant

Prompt 4. Fandt SciPy paper fra 2020 med mange citations 

Prompt 5. Fandt ikke noget match 

prompt 6. Agenten lavede en fejl her og brugte max_citations i stedet for min_citations i en test kørelse - Failure

Prompt 7. Fandt Physics-informed machine learning med over 1000 citations

Prompt 8. Fandt SSDF paper fra 2022 med 69 citations 

Prompt 9. Fandt en DevSecOps paper men var dog under 200 citations - Lille failure, format fejl

Prompt 10. Fandt Agile Manifesto fra 2001 med over 100 citations

Agenten løste de fleste prompts fint og gjorde egentlig det den skulle, der var lige nogle failures eller limitations

Limitations:
Agenten læste "at least 100 citations" forkert og kaldte tool'et med max_citations i stedet for min_citations
Agenten gav også svag relevans tilbage i prompt 3 - Kunne i hvert fald have været bedre

## Refleksion

### Hvad fungerede godt
- Agenten brugte OpenAlex som kilde i stedet for kun at stole på LLM'ens viden
- Agenten kunne i de fleste tilfælde forstå brugerens prompt, udtrække topic, year constraint og citation constraint
og bruge værdierne i tool kaldet


### Hvad var upålideligt 
- LLM'ens forståelse af citation constraints --> I en test blev at least 100 citations forstået forkert
som max_citations=100 i stedet for min_citations. Det gjorde at agenten returnerede et paper som ikke opfyldte 
citation kravet der var blevet givet
- Små fejl med formattering i nogle tilfælder - Alle felter var ikke altid blevet vist lige tydeligt
- Relevansen i et tilfælde var svag
- Typisk kaldte agenten kun et tool pr. prompt, men i nogle "No matching paper was found" kunne den 
finde på at kalde tool'et igen, hvilket er en limitation

### Hallucinationer og forkerte svar
- LLM'en hallucinerede ikke hele papers, fordi agenten var prompted til kun at bruge papers som kom fra tool'et
- For at forhindre forkerte svar blev agenten prompted til at ikke opfinde metadata selv

### Hvad jeg vil forbedre med mere tid
- Jeg ville gøre output formattet er mere fast, så final answer altid indeholder alle krævede krav


## Gruppe
- Adnan