"""
Script para popular o banco de dados com dados de exemplo
Execute este script após configurar o Supabase para ter dados iniciais
"""

import pandas as pd
from datetime import datetime, timedelta
import random
import numpy as np

# Dados de exemplo para vendas
def generate_sample_vendas(num_vendas=100):
    """Gera dados de exemplo para vendas"""
    
    # Nomes de clientes realistas
    nomes_clientes = [
        "Maria Silva", "João Santos", "Ana Costa", "Pedro Oliveira", "Lucia Rodrigues",
        "Carlos Almeida", "Fernanda Lima", "Ricardo Ferreira", "Juliana Souza", "Roberto Martins",
        "Patricia Dias", "Marcos Pereira", "Camila Barbosa", "Eduardo Nascimento", "Renata Gomes",
        "Felipe Cardoso", "Mariana Torres", "Gustavo Ribeiro", "Tatiana Melo", "Bruno Carvalho",
        "Isabela Araujo", "Leonardo Castro", "Vanessa Moreira", "Rodrigo Teixeira", "Cristina Vieira",
        "Thiago Correia", "Amanda Lopes", "Diego Monteiro", "Priscila Campos", "Fabio Neves",
        "Stephanie Rocha", "Alexandre Freitas", "Bianca Santana", "Mateus Cunha", "Larissa Mendes",
        "Vinicius Duarte", "Gabriela Xavier", "Igor Fonseca", "Caroline Ramos", "Daniel Miranda"
    ]
    
    produtos = [
        "Curso High Ticket", "Mentoria Individual", "Consultoria Premium", 
        "Workshop Intensivo", "Treinamento VIP", "Curso Avançado"
    ]
    
    meios_pagamento = ["PIX", "Cartão à vista", "Cartão parcelado", "Boleto", "Transferência"]
    vendedores = ["Ana", "Fernando"]
    status_vendas = ["confirmada", "pendente", "cancelada"]
    
    vendas = []
    
    for i in range(num_vendas):
        # Data aleatória nos últimos 90 dias
        dias_atras = random.randint(0, 90)
        data_venda = datetime.now() - timedelta(days=dias_atras)
        
        # Valor baseado no produto com variação
        produto = random.choice(produtos)
        if produto == "Curso High Ticket":
            valor_base = 1997.0
        elif produto == "Mentoria Individual":
            valor_base = 2997.0
        elif produto == "Consultoria Premium":
            valor_base = 4997.0
        else:
            valor_base = random.uniform(800, 1500)
        
        # Adicionar variação de ±20%
        valor = valor_base * random.uniform(0.8, 1.2)
        
        cliente_nome = random.choice(nomes_clientes)
        instagram_handle = f"@{cliente_nome.lower().replace(' ', '')}{random.randint(10, 99)}"
        
        venda = {
            'cliente_nome': cliente_nome,
            'cliente_instagram': instagram_handle,
            'cliente_email': f"{cliente_nome.lower().replace(' ', '.')}@email.com",
            'cliente_telefone': f"(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
            'produto': produto,
            'valor': round(valor, 2),
            'vendedor': random.choice(vendedores),
            'data_venda': data_venda.strftime('%Y-%m-%d'),
            'status': random.choice(status_vendas),
            'meio_pagamento': random.choice(meios_pagamento),
            'comissao_pct': 0.30,
            'observacoes': f"Venda realizada via Instagram. Cliente interessado em {produto}.",
            'created_at': data_venda.isoformat()
        }
        
        vendas.append(venda)
    
    return pd.DataFrame(vendas)

def generate_sample_leads(num_leads=200):
    """Gera dados de exemplo para leads"""
    
    # Nomes de leads realistas
    nomes_leads = [
        "Carlos Eduardo", "Mariana Santos", "Felipe Costa", "Gabriela Oliveira", "Lucas Rodrigues",
        "Beatriz Almeida", "Rafael Lima", "Camila Ferreira", "Gustavo Souza", "Isabella Martins",
        "Thiago Dias", "Larissa Pereira", "Vitor Barbosa", "Natalia Nascimento", "Bruno Gomes",
        "Amanda Cardoso", "Diego Torres", "Stephanie Ribeiro", "Mateus Melo", "Bruna Carvalho",
        "Leonardo Araujo", "Caroline Castro", "Rodrigo Moreira", "Vanessa Teixeira", "Alexandre Vieira",
        "Priscila Correia", "Igor Lopes", "Bianca Monteiro", "Daniel Campos", "Tatiana Neves",
        "Fabio Rocha", "Cristina Freitas", "Vinicius Santana", "Juliana Cunha", "Pedro Mendes",
        "Ana Clara", "João Victor", "Maria Fernanda", "Paulo Ricardo", "Leticia Duarte"
    ]
    
    status_leads = ["novo", "contatado", "interessado", "negociacao", "fechado", "perdido"]
    origens = ["Instagram", "WhatsApp", "Indicação", "Site", "Evento", "Anúncio Facebook", "Google Ads"]
    vendedores = ["Ana", "Fernando"]
    
    leads = []
    
    for i in range(num_leads):
        # Data aleatória nos últimos 60 dias
        dias_atras = random.randint(0, 60)
        data_criacao = datetime.now() - timedelta(days=dias_atras)
        
        # Última interação (pode ser mais recente que criação)
        dias_ultima_interacao = random.randint(0, min(dias_atras, 10))
        ultima_interacao = datetime.now() - timedelta(days=dias_ultima_interacao)
        
        nome = random.choice(nomes_leads)
        instagram_handle = f"@{nome.lower().replace(' ', '')}{random.randint(100, 999)}"
        
        # Score baseado no status (leads mais avançados têm scores maiores)
        status = random.choice(status_leads)
        if status in ["fechado", "negociacao"]:
            score = random.randint(8, 10)
        elif status in ["interessado"]:
            score = random.randint(6, 8)
        elif status in ["contatado"]:
            score = random.randint(4, 7)
        else:  # novo, perdido
            score = random.randint(1, 5)
        
        lead = {
            'nome': nome,
            'instagram': instagram_handle,
            'telefone': f"(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
            'email': f"{nome.lower().replace(' ', '.')}@email.com",
            'status': status,
            'origem': random.choice(origens),
            'vendedor': random.choice(vendedores),
            'nota': f"Lead captado via {random.choice(origens)}. Demonstrou interesse em curso de vendas.",
            'score': score,
            'ultima_interacao': ultima_interacao.strftime('%Y-%m-%d'),
            'valor_estimado': round(random.uniform(1500, 3000), 2),
            'created_at': data_criacao.isoformat()
        }
        
        leads.append(lead)
    
    return pd.DataFrame(leads)

def generate_sample_custos(num_custos=50):
    """Gera dados de exemplo para custos"""
    
    categorias_custos = {
        "Anúncios": [
            "Facebook Ads - Janeiro", "Google Ads - Janeiro", "Instagram Ads", 
            "LinkedIn Ads", "TikTok Ads", "YouTube Ads"
        ],
        "Ferramentas": [
            "Supabase Pro", "Streamlit Cloud", "Zoom Pro", "Canva Pro",
            "Hotmart", "RD Station", "MailChimp", "Notion Pro"
        ],
        "Salários": [
            "Salário Ana", "Salário Fernando", "Freelancer Design",
            "Copywriter", "Editor de Vídeo", "Social Media"
        ],
        "Operacional": [
            "Energia Elétrica", "Internet", "Telefone", "Material Escritório",
            "Hospedagem Site", "Domínio", "SSL Certificate", "Backup Cloud"
        ],
        "Treinamento": [
            "Curso Marketing Digital", "Mentoria Vendas", "Workshop Copywriting",
            "Treinamento Equipe", "Certificação Google", "Curso Funil de Vendas"
        ]
    }
    
    custos = []
    
    for i in range(num_custos):
        # Data aleatória nos últimos 90 dias
        dias_atras = random.randint(0, 90)
        data_custo = datetime.now() - timedelta(days=dias_atras)
        
        categoria = random.choice(list(categorias_custos.keys()))
        descricao = random.choice(categorias_custos[categoria])
        
        # Valor baseado na categoria
        if categoria == "Anúncios":
            valor = random.uniform(1000, 8000)
        elif categoria == "Salários":
            valor = random.uniform(3000, 15000)
        elif categoria == "Ferramentas":
            valor = random.uniform(50, 500)
        elif categoria == "Operacional":
            valor = random.uniform(100, 1000)
        else:  # Treinamento
            valor = random.uniform(200, 2000)
        
        custo = {
            'descricao': descricao,
            'categoria': categoria,
            'valor': round(valor, 2),
            'data_custo': data_custo.strftime('%Y-%m-%d'),
            'responsavel': random.choice(["Ana", "Fernando", "Empresa"]),
            'recorrente': random.choice([True, False]) if categoria in ["Ferramentas", "Operacional"] else False,
            'created_at': data_custo.isoformat()
        }
        
        custos.append(custo)
    
    return pd.DataFrame(custos)

def generate_sample_activity_logs(num_logs=100):
    """Gera dados de exemplo para logs de atividade"""
    
    actions = [
        "Login", "Logout", "Nova Venda", "Venda Editada", "Venda Removida",
        "Novo Lead", "Lead Atualizado", "Lead Convertido", "Export Realizado",
        "Configuração Alterada", "Meta Atingida", "Relatório Gerado",
        "Follow-up Realizado", "WhatsApp Enviado", "E-mail Enviado"
    ]
    
    users = ["ana", "fernando"]
    
    logs = []
    
    for i in range(num_logs):
        # Data aleatória nos últimos 30 dias
        dias_atras = random.randint(0, 30)
        timestamp = datetime.now() - timedelta(
            days=dias_atras,
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        action = random.choice(actions)
        user = random.choice(users)
        
        # Detalhes baseados na ação
        if action == "Nova Venda":
            details = f"Venda de R$ {random.uniform(1000, 3000):,.2f} adicionada"
        elif action == "Novo Lead":
            details = f"Lead com score {random.randint(1, 10)} adicionado"
        elif action == "Export Realizado":
            details = f"Export de {random.choice(['vendas', 'leads', 'relatório'])} em CSV"
        elif action == "Meta Atingida":
            details = f"Meta mensal de R$ {random.uniform(30000, 60000):,.2f} atingida"
        else:
            details = f"Ação executada por {user}"
        
        log = {
            'user_id': user,
            'action': action,
            'details': details,
            'timestamp': timestamp.isoformat()
        }
        
        logs.append(log)
    
    return pd.DataFrame(logs)

def save_sample_data():
    """Salva todos os dados de exemplo em arquivos CSV"""
    
    print("Gerando dados de exemplo...")
    
    # Gerar dados
    vendas_df = generate_sample_vendas(100)
    leads_df = generate_sample_leads(200)
    custos_df = generate_sample_custos(50)
    logs_df = generate_sample_activity_logs(100)
    
    # Salvar em CSV
    vendas_df.to_csv('data/sample_vendas.csv', index=False, encoding='utf-8')
    leads_df.to_csv('data/sample_leads.csv', index=False, encoding='utf-8')
    custos_df.to_csv('data/sample_custos.csv', index=False, encoding='utf-8')
    logs_df.to_csv('data/sample_activity_logs.csv', index=False, encoding='utf-8')
    
    print("Dados de exemplo salvos em:")
    print("   - data/sample_vendas.csv (100 registros)")
    print("   - data/sample_leads.csv (200 registros)")
    print("   - data/sample_custos.csv (50 registros)")
    print("   - data/sample_activity_logs.csv (100 registros)")
    print("\nResumo dos dados gerados:")
    print(f"   - Vendas: R$ {vendas_df['valor'].sum():,.2f} em faturamento")
    print(f"   - Leads: {len(leads_df)} leads com score medio {leads_df['score'].mean():.1f}")
    print(f"   - Custos: R$ {custos_df['valor'].sum():,.2f} em custos totais")
    print(f"   - Logs: {len(logs_df)} atividades registradas")

if __name__ == "__main__":
    save_sample_data()