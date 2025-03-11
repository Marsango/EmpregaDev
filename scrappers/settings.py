jobs_names: list[str] = ["Programador",
                         "Jr",
                         "Estágio",
                         "Desenvolvedor",
                         "Estagiário",
                         "Python",
                         "Software",
                         "backend",
                         "back-end",
                         "Fullstack",
                         "Engineer",
                         "Software",
                         "Sistemas",
                         "Analista",
                         "Django",
                         "Scraping",
                         "Engenheiro",
                         "Júnior",
                         "Back end",
                         "Pessoa"
                         ] #word for job searching
forbidden_words: list[str] = ["Arquitetura", "Marketing", "Design", "Direito", "Atendimento", "Suporte", "Artes",
                   "Fiscal", "Customer Service", "Customer Success", "Jurídico", "Comercial",
                   "Contábil", "Contabilidade", "Negócios", "Social Media", "Comunicação",
                   "Educação", "Engenharia Civil", "Engenheiro Civil", "Matemática", "Letras", "Redação",
                    "Cobrança", "Advogado"]

remote: bool = True #only remote jobs = True, all jobs = False
use_cookies: bool = True #use cookies for login, need to configure cookies.json
LINKEDIN_EMAIL: str = "" #linkedin email
LINKEDIN_PASSWORD: str = "" #linkedin password
api_key_telegram: str = "YOUR_API_KEY_HERE"
channel_id: str = "YOUR_CHANNEL_ID_HERE"