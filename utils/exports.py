import pandas as pd
import io
import base64
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

class ExportManager:
    """Gerenciador de exports em diferentes formatos"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    def export_to_csv(self, data, filename_prefix="export"):
        """Exporta dados para CSV"""
        if isinstance(data, dict):
            # Se for dict, converter para DataFrame
            df = pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            df = data
        else:
            raise ValueError("Dados devem ser DataFrame ou dict")
        
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8')
        csv_content = csv_buffer.getvalue()
        
        filename = f"{filename_prefix}_{self.timestamp}.csv"
        return csv_content, filename, "text/csv"
    
    def export_to_excel(self, data_dict, filename_prefix="export"):
        """Exporta múltiplas planilhas para Excel"""
        excel_buffer = io.BytesIO()
        
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            for sheet_name, data in data_dict.items():
                if isinstance(data, dict):
                    df = pd.DataFrame(data)
                elif isinstance(data, pd.DataFrame):
                    df = data
                else:
                    continue
                
                # Limitar nome da aba a 31 caracteres
                sheet_name = sheet_name[:31]
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        excel_content = excel_buffer.getvalue()
        filename = f"{filename_prefix}_{self.timestamp}.xlsx"
        return excel_content, filename, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    def create_sales_report_pdf(self, vendas_df, periodo=""):
        """Cria relatório de vendas em PDF"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=HexColor('#9D4EDD'),
            alignment=1  # Centro
        )
        
        # Elementos do PDF
        elements = []
        
        # Título
        title = Paragraph(f"Relatório de Vendas - {periodo}", title_style)
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        # Resumo executivo
        if not vendas_df.empty:
            total_vendas = len(vendas_df)
            total_faturamento = vendas_df['valor'].sum()
            ticket_medio = vendas_df['valor'].mean()
            
            resumo_data = [
                ['Métrica', 'Valor'],
                ['Total de Vendas', f"{total_vendas}"],
                ['Faturamento Total', f"R$ {total_faturamento:,.2f}"],
                ['Ticket Médio', f"R$ {ticket_medio:,.2f}"]
            ]
            
            resumo_table = Table(resumo_data, colWidths=[3*inch, 2*inch])
            resumo_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#9D4EDD')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F5F5F5')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(resumo_table)
            elements.append(Spacer(1, 30))
            
            # Tabela de vendas
            vendas_para_pdf = vendas_df.head(20).copy()  # Limitar a 20 vendas
            vendas_para_pdf['valor'] = vendas_para_pdf['valor'].apply(lambda x: f"R$ {x:,.2f}")
            vendas_para_pdf['data_venda'] = pd.to_datetime(vendas_para_pdf['data_venda']).dt.strftime('%d/%m/%Y')
            
            # Preparar dados da tabela
            table_data = [['Cliente', 'Vendedor', 'Valor', 'Data']]
            
            for _, row in vendas_para_pdf.iterrows():
                table_data.append([
                    row['cliente_nome'][:20],  # Limitar tamanho
                    row['vendedor'],
                    row['valor'],
                    row['data_venda']
                ])
            
            vendas_table = Table(table_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            vendas_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#06FFA5')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F9F9F9')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9)
            ]))
            
            elements.append(Paragraph("Detalhamento das Vendas", styles['Heading2']))
            elements.append(Spacer(1, 12))
            elements.append(vendas_table)
        
        else:
            elements.append(Paragraph("Nenhuma venda encontrada no período.", styles['Normal']))
        
        # Rodapé
        elements.append(Spacer(1, 30))
        footer_text = f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')} | Instagram Sales Dashboard"
        footer = Paragraph(footer_text, styles['Normal'])
        elements.append(footer)
        
        # Gerar PDF
        doc.build(elements)
        pdf_content = buffer.getvalue()
        buffer.close()
        
        filename = f"relatorio_vendas_{self.timestamp}.pdf"
        return pdf_content, filename, "application/pdf"
    
    def create_leads_report_pdf(self, leads_df, periodo=""):
        """Cria relatório de leads em PDF"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=HexColor('#0EA5E9'),
            alignment=1
        )
        
        elements = []
        
        # Título
        title = Paragraph(f"Relatório de Leads - {periodo}", title_style)
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        if not leads_df.empty:
            # Estatísticas de leads
            total_leads = len(leads_df)
            score_medio = leads_df['score'].mean()
            conversao = len(leads_df[leads_df['status'] == 'fechado']) / total_leads * 100
            
            stats_data = [
                ['Métrica', 'Valor'],
                ['Total de Leads', f"{total_leads}"],
                ['Score Médio', f"{score_medio:.1f}/10"],
                ['Taxa de Conversão', f"{conversao:.1f}%"]
            ]
            
            stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#0EA5E9')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F0F8FF')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(stats_table)
            elements.append(Spacer(1, 30))
            
            # Funil de leads
            funil_data = [['Status', 'Quantidade', 'Percentual']]
            status_counts = leads_df['status'].value_counts()
            
            for status, count in status_counts.items():
                pct = (count / total_leads * 100)
                funil_data.append([status.title(), f"{count}", f"{pct:.1f}%"])
            
            funil_table = Table(funil_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
            funil_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#06FFA5')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F0FFF0')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(Paragraph("Funil de Conversão", styles['Heading2']))
            elements.append(Spacer(1, 12))
            elements.append(funil_table)
        
        else:
            elements.append(Paragraph("Nenhum lead encontrado no período.", styles['Normal']))
        
        # Rodapé
        elements.append(Spacer(1, 30))
        footer_text = f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')} | Instagram Sales Dashboard"
        footer = Paragraph(footer_text, styles['Normal'])
        elements.append(footer)
        
        doc.build(elements)
        pdf_content = buffer.getvalue()
        buffer.close()
        
        filename = f"relatorio_leads_{self.timestamp}.pdf"
        return pdf_content, filename, "application/pdf"
    
    def export_financial_report(self, vendas_df, custos_data=None):
        """Cria relatório financeiro completo"""
        
        # Calcular métricas financeiras
        if not vendas_df.empty:
            vendas_confirmadas = vendas_df[vendas_df['status'] == 'confirmada']
            receita_total = vendas_confirmadas['valor'].sum()
            total_vendas = len(vendas_confirmadas)
            ticket_medio = vendas_confirmadas['valor'].mean()
            
            # Custos simulados se não fornecidos
            if custos_data is None:
                custos_data = {
                    'Marketing': 15000.00,
                    'Operacional': 8000.00,
                    'Pessoal': 25000.00,
                    'Outros': 5000.00
                }
            
            custo_total = sum(custos_data.values())
            lucro_bruto = receita_total - custo_total
            margem_lucro = (lucro_bruto / receita_total * 100) if receita_total > 0 else 0
            roi = (lucro_bruto / custo_total * 100) if custo_total > 0 else 0
            
            # Criar DRE
            dre_data = {
                'Item': [
                    'Receita Bruta',
                    '(-) Custos Totais',
                    '= Lucro Bruto',
                    'Margem de Lucro (%)',
                    'ROI (%)'
                ],
                'Valor': [
                    f"R$ {receita_total:,.2f}",
                    f"R$ {custo_total:,.2f}",
                    f"R$ {lucro_bruto:,.2f}",
                    f"{margem_lucro:.1f}%",
                    f"{roi:.1f}%"
                ]
            }
            
            # Dados por vendedor
            vendas_por_vendedor = vendas_confirmadas.groupby('vendedor').agg({
                'valor': ['sum', 'count', 'mean']
            }).round(2)
            
            vendas_por_vendedor.columns = ['Total', 'Quantidade', 'Ticket_Medio']
            vendas_por_vendedor = vendas_por_vendedor.reset_index()
            
        else:
            dre_data = {'Item': ['Sem dados'], 'Valor': ['R$ 0,00']}
            vendas_por_vendedor = pd.DataFrame()
        
        # Criar Excel com múltiplas abas
        excel_data = {
            'DRE': dre_data,
            'Vendas_Vendedor': vendas_por_vendedor,
            'Custos': custos_data if isinstance(custos_data, dict) else {},
            'Vendas_Detalhadas': vendas_df.head(100) if not vendas_df.empty else {}
        }
        
        return self.export_to_excel(excel_data, "relatorio_financeiro")
    
    def import_csv_data(self, uploaded_file, data_type="vendas"):
        """Importa dados de CSV"""
        try:
            df = pd.read_csv(uploaded_file)
            
            # Validação básica baseada no tipo
            if data_type == "vendas":
                required_columns = ['cliente_nome', 'valor', 'vendedor', 'data_venda']
            elif data_type == "leads":
                required_columns = ['nome', 'telefone', 'vendedor', 'status']
            else:
                required_columns = []
            
            # Verificar colunas obrigatórias
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return None, f"Colunas obrigatórias faltando: {', '.join(missing_columns)}"
            
            # Validações específicas
            if data_type == "vendas":
                # Validar valores numéricos
                if not pd.api.types.is_numeric_dtype(df['valor']):
                    try:
                        df['valor'] = pd.to_numeric(df['valor'].str.replace(',', '.'), errors='coerce')
                    except:
                        return None, "Coluna 'valor' deve conter apenas números"
                
                # Validar datas
                try:
                    df['data_venda'] = pd.to_datetime(df['data_venda'])
                except:
                    return None, "Coluna 'data_venda' deve estar no formato de data válido"
            
            return df, f"✅ {len(df)} registros importados com sucesso!"
            
        except Exception as e:
            return None, f"Erro ao processar arquivo: {str(e)}"
    
    def create_dashboard_snapshot(self, metrics_data):
        """Cria snapshot do dashboard em PDF"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'DashboardTitle',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=30,
            textColor=HexColor('#9D4EDD'),
            alignment=1
        )
        
        elements = []
        
        # Título
        title = Paragraph(f"Dashboard Snapshot - {datetime.now().strftime('%d/%m/%Y %H:%M')}", title_style)
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        # Métricas principais
        if metrics_data:
            metrics_table_data = [['Métrica', 'Valor', 'Status']]
            
            for metric in metrics_data:
                status_icon = "📈" if metric.get('trend', 'up') == 'up' else "📉"
                metrics_table_data.append([
                    metric.get('name', ''),
                    metric.get('value', ''),
                    status_icon
                ])
            
            metrics_table = Table(metrics_table_data, colWidths=[2.5*inch, 2*inch, 1*inch])
            metrics_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#9D4EDD')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F5F0FF')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(metrics_table)
        
        # Rodapé
        elements.append(Spacer(1, 50))
        footer_text = "Este é um snapshot automático do dashboard. Para dados em tempo real, acesse o sistema."
        footer = Paragraph(footer_text, styles['Normal'])
        elements.append(footer)
        
        doc.build(elements)
        pdf_content = buffer.getvalue()
        buffer.close()
        
        filename = f"dashboard_snapshot_{self.timestamp}.pdf"
        return pdf_content, filename, "application/pdf"