from .models import Source, SessionLocal

SEED_SOURCES = [
    {
        "title": "Patents Act, 1970 — Section 3(p)",
        "jurisdiction": "India",
        "source_type": "Statute",
        "authority": "Government of India / IP India",
        "url": "https://www.ipindia.gov.in/",
        "section": "Section 3(p)",
        "version": "Current source should be verified before legal use",
        "effective_date": "",
        "text": "Patents law includes exclusions concerning inventions that are in effect traditional knowledge or an aggregation or duplication of known properties of traditionally known components.",
    },
    {
        "title": "IP India Public Search and E-Services",
        "jurisdiction": "India",
        "source_type": "Official registry portal",
        "authority": "Office of the Controller General of Patents, Designs & Trade Marks",
        "url": "https://ipindia.gov.in/pages/e-services",
        "section": "",
        "version": "Live portal",
        "effective_date": "",
        "text": "Official portal provides public search and status/e-filing facilities for patents, trademarks, designs and geographical indications.",
    },
    {
        "title": "Biological Diversity Act / ABS e-Filing",
        "jurisdiction": "India",
        "source_type": "Regulatory portal",
        "authority": "National Biodiversity Authority",
        "url": "https://absefiling.nic.in/NBA/login/auth",
        "section": "",
        "version": "2024 Rules portal",
        "effective_date": "2024",
        "text": "The NBA ABS e-filing portal states that the Biological Diversity (Amendment) Act, 2023 came into force on 1 April 2024 and the Biological Diversity Rules, 2024 came into force on 21 December 2024.",
    },
    {
        "title": "WIPO Treaty on IP, Genetic Resources and Associated Traditional Knowledge",
        "jurisdiction": "International",
        "source_type": "Treaty",
        "authority": "WIPO",
        "url": "https://www.wipo.int/en/web/treaties/ip/gratk/index",
        "section": "Treaty",
        "version": "Adopted 24 May 2024",
        "effective_date": "",
        "text": "The 2024 WIPO Treaty establishes a patent disclosure requirement concerning the country of origin or source of genetic resources and disclosure concerning Indigenous Peoples or local communities providing associated traditional knowledge, subject to the Treaty's conditions and entry into force.",
    },
    {
        "title": "WIPO GRATK Treaty Resource Center",
        "jurisdiction": "International",
        "source_type": "Official resource center",
        "authority": "WIPO",
        "url": "https://www.wipo.int/en/web/traditional-knowledge/wipo-treaty-on-ip-gr-and-associated-tk",
        "section": "",
        "version": "Continuously updated",
        "effective_date": "",
        "text": "WIPO provides treaty text, explanatory materials, FAQs and resources on genetic resources and associated traditional knowledge.",
    },
]

def seed_sources():
    db = SessionLocal()
    try:
        if db.query(Source).count() == 0:
            for s in SEED_SOURCES:
                db.add(Source(**s))
            db.commit()
    finally:
        db.close()
