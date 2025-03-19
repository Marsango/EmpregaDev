jobs_names: list[str] = ["Programador",
                         "Jr",
                         "Estágio",
                         "Internship",
                         "Intern",
                         "Developer",
                         "Desenvolvedor",
                         "Estagiário",
                         "Python",
                         "Software",
                         "backend",
                         "back-end",
                         "Fullstack",
                         "RPA",
                         "Engineer",
                         "Software",
                         "Sistemas",
                         "Systems",
                         "Analista",
                         "Systems Analyst",
                         "Software Analyst",
                         "Entry Level",
                         "Programmer",
                         "Django",
                         "Scraping",
                         "Engenheiro",
                         "Júnior",
                         "Back end",
                         "Pessoa"
                         ]  # word for job searching
forbidden_words: list[str] = ["Arquitetura", "Marketing", "Design", "Direito", "Atendimento", "Suporte", "Artes",
                              "Fiscal", "Customer Service", "Customer Success", "Jurídico", "Comercial", "Midia",
                              "Acadêmico",
                              "Contábil", "Contabilidade", "Negócios", "Social Media", "Comunicação",
                              "Experiência do Cliente",
                              "Conteúdo", "Tutor", "Educacional", "Ouvidoria", "Professor", "Sales", "Business",
                              "Vendas",
                              "Educação", "Engenharia Civil", "Engenheiro Civil", "Matemática", "Letras", "Redação",
                              "Gerente",
                              "Cobrança", "Advogado", "Vendedor", "Pedagógico", "Negócios", "Editor", "Editora",
                              "Crédito",
                              "Clima", "Cultura", "Financeiros", "Financeiro", "Mentoria", "Comunidades", "Moderação",
                              "Pré-Vendas", "CRM", "Gestão", "Contratos", "Gestao", "Customer", "Compras", "Produção",
                              "Content", "Consultor", "Nutricionista", "Media", "RH"]

remote: bool = True #only remote jobs = True, all jobs = False
use_cookies: bool = True #use cookies for login, need to configure cookies.json
LINKEDIN_EMAIL: str = "" #linkedin email
LINKEDIN_PASSWORD: str = "" #linkedin password
api_key_telegram: str = "YOUR_API_KEY_HERE"
channel_id: str = "YOUR_CHANNEL_ID_HERE"