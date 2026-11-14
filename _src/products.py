# Product catalogue for getvibetoolsai.com
# Prices checked in the Gumroad dashboard on 14 Nov 2026.
# To change a price or add a product: edit this file, run `python3 _src/build.py`, commit.

STORE = "https://vibetoolsai.gumroad.com/l/"

COLLECTIONS = [
    {
        "id": "kept-kindly",
        "lang": "en",
        "tab": "Family & legacy",
        "color": "plum",
        "title": "Kept Kindly planners",
        "intro": "Printable planners and spreadsheets that help families in the US and Canada "
                 "write down what matters before it is needed, and handle what comes after a death.",
        "products": [
            {"slug": "before-after-legacy-bundle", "name": "Before & After Legacy Bundle",
             "price": "$32", "was": "$42", "formats": ["3 planners", "PDF Letter + A4", "XLSX"],
             "text": "All three Kept Kindly planners together: the Legacy Planner, the After Death Checklist "
                     "and the Executor Checklist & Expense Log.", "featured": True},
            {"slug": "kept-kindly-legacy-planner", "name": "Kept Kindly Legacy Planner",
             "price": "$14", "formats": ["46 pages", "PDF Letter + A4", "25-sheet XLSX"],
             "text": "An end-of-life planner and life admin binder: contacts, accounts, insurance, "
                     "property, wishes and where the important papers are kept."},
            {"slug": "after-death-checklist", "name": "After Death Checklist for Family",
             "price": "$12", "formats": ["21 pages", "PDF Letter + A4", "12-sheet XLSX"],
             "text": "What to do in the first days and weeks after a death, with time-sensitive tasks "
                     "marked and space to note who is handling what."},
            {"slug": "executor-checklist", "name": "Executor Checklist & Expense Log",
             "price": "$16", "formats": ["27 pages", "PDF Letter + A4", "19-sheet XLSX"],
             "text": "An estate settlement tracker for executors: tasks, assets, debts, income and "
                     "an expense log with running totals."},
        ],
    },
    {
        "id": "ai-prompts",
        "lang": "en",
        "tab": "AI for your job",
        "color": "blue",
        "title": "ChatGPT prompt packs for professionals",
        "intro": "Copy-paste prompts written around a real working week. Each works in ChatGPT, "
                 "Claude, Gemini or Copilot: replace the brackets and get a usable first draft.",
        "products": [
            {"slug": "realtor-ai-playbook", "name": "45 ChatGPT Prompts for Real Estate Agents",
             "price": "$12", "formats": ["PDF"],
             "text": "Listings, leads, follow-ups and closings, written with Fair Housing in mind."},
            {"slug": "realtor-mini-25", "name": "25 Prompts for Real Estate Agents (Mini Pack)",
             "price": "$7", "formats": ["PDF"],
             "text": "The 25 prompts an agent uses every week: listings, client emails and follow-ups."},
            {"slug": "loan-officer-ai-playbook", "name": "45 ChatGPT Prompts for Loan Officers",
             "price": "$14", "formats": ["PDF"],
             "text": "Realtor partnerships, borrower updates, compliant marketing and follow-up."},
            {"slug": "local-business-ai-playbook", "name": "45 ChatGPT Prompts for Local Service Businesses",
             "price": "$14", "formats": ["PDF"],
             "text": "Google Business Profile posts, review replies, offers, email and social."},
            {"slug": "teacher-ai-planner", "name": "45 ChatGPT Prompts for Teachers",
             "price": "$9", "formats": ["PDF"],
             "text": "Lesson plans, differentiation, rubrics, parent emails and IEP-friendly adaptations."},
        ],
        "free": [
            {"slug": "listing-prompts-free", "name": "5 Listing Prompts That Sell"},
            {"slug": "free-realtor-prompts", "name": "7 Free Prompts for Realtors"},
            {"slug": "free-loan-officer-prompts", "name": "7 Free Prompts for Loan Officers"},
            {"slug": "free-small-business-prompts", "name": "7 Free Prompts for Small Business"},
            {"slug": "free-teacher-prompts", "name": "7 Free Prompts for Teachers"},
            {"slug": "oytvfx", "name": "5 AI Processes for Your First Week in Business"},
        ],
    },
    {
        "id": "freelancer-money",
        "lang": "en",
        "tab": "Freelancer money",
        "color": "green",
        "title": "Tax and profit sheets for freelancers",
        "intro": "Spreadsheets for self-employed people and Etsy or Shopify sellers who want to know "
                 "what they earned and what to set aside for tax.",
        "products": [
            {"slug": "freelancer-tax-profit-tracker", "name": "Freelancer Tax & Profit Tracker",
             "price": "$14", "formats": ["Excel", "Google Sheets"],
             "text": "Income, expenses, profit and a tax set-aside in one workbook."},
        ],
        "free": [
            {"slug": "free-tax-set-aside-calculator", "name": "Quarterly Tax Set-Aside Calculator"},
        ],
    },
    # ---------- Polish ----------
    {
        "id": "ksef",
        "lang": "pl",
        "tab": "KSeF i JDG",
        "color": "red",
        "title": "KSeF dla JDG i małej firmy",
        "intro": "Arkusze, przewodniki i prompty, które pomagają przejść na e-faktury przed "
                 "1 stycznia 2027 i ułożyć comiesięczną współpracę z biurem rachunkowym.",
        "products": [
            {"slug": "fzjwvr", "name": "KSeF dla małej firmy i JDG: przejście krok po kroku",
             "price": "49 zł", "formats": ["Pakiet ZIP"],
             "text": "Przewodnik po zmianach od 1.01.2027 z planem przejścia na e-faktury.", "featured": True},
            {"slug": "zestaw-wdrozeniowy-ksef", "name": "Zestaw wdrożeniowy KSeF dla freelancera i JDG",
             "price": "59 zł", "formats": ["Arkusz", "Przewodnik"],
             "text": "Jeden arkusz na faktury z numerem KSeF, odrzucenia, pobrane koszty i dostępy."},
            {"slug": "teczka-ksiegowy-ksef", "name": "Teczka „Księgowy + KSeF” dla JDG",
             "price": "39 zł", "formats": ["Arkusz", "PDF"],
             "text": "Comiesięczne zamknięcie z biurem rachunkowym w jednym miejscu."},
            {"slug": "ksef-toolkit-jdg", "name": "KSeF Toolkit: 30 promptów AI dla JDG",
             "price": "39 zł", "formats": ["PDF"],
             "text": "Maile, przypomnienia, FAQ dla klientów, checklisty i wiadomości do dostawców."},
        ],
        "free": [
            {"slug": "free-ksef-licznik-10k", "name": "Licznik limitu 10 000 zł + checklista KSeF 2027"},
        ],
    },
    {
        "id": "ai-firma",
        "lang": "pl",
        "tab": "AI w firmie",
        "color": "blue",
        "title": "AI w małej firmie i nieruchomościach",
        "intro": "Gotowe procesy i prompty do ChatGPT i Claude dla właścicieli małych firm "
                 "i agentów nieruchomości.",
        "products": [
            {"slug": "ai-w-malej-firmie", "name": "AI w małej firmie. 50 gotowych procesów",
             "price": "79 zł", "formats": ["PDF", "DOCX", "Prompty"],
             "text": "Oferty, odpowiedzi klientom, posty i porządek w dokumentach, krok po kroku."},
            {"slug": "agent-nieruchomosci-25-promptow", "name": "25 promptów ChatGPT dla agenta nieruchomości",
             "price": "29 zł", "formats": ["PDF"],
             "text": "Ogłoszenia, e-maile i follow-upy do leadów z portali."},
        ],
        "free": [
            {"slug": "hwdanj", "name": "5 procesów AI na pierwszy tydzień w firmie"},
            {"slug": "ogloszenie-ktore-sprzedaje", "name": "5 promptów na ogłoszenie, które sprzedaje"},
        ],
    },
    {
        "id": "sport",
        "lang": "pl",
        "tab": "Jedzenie i sport",
        "color": "green",
        "title": "Jedzenie dla trenujących",
        "intro": "Ebooki z przepisami ze zwykłych produktów, z policzonym makro.",
        "products": [
            {"slug": "paliwo-w-15-minut", "name": "Paliwo w 15 minut",
             "price": "39 zł", "formats": ["Ebook"],
             "text": "101 szybkich posiłków przed i po treningu, w wersji na redukcję i na masę."},
            {"slug": "zdrowe-sniadania-sportowiec", "name": "Zdrowe śniadania dla sportowca",
             "price": "39 zł", "formats": ["Ebook"],
             "text": "30 śniadań dopasowanych do tego, ile czasu zostało do treningu."},
        ],
    },
]
