import qrcode
from PIL import Image
import os
from io import BytesIO

class QRCodeService:
    
    @staticmethod
    def gerar_qrcode_personalizado(
        url: str,
        logo_path: str = "app/static/logo.png",
        cor_fundo: str = "#F5E6D3",
        cor_qr: str = "#1A120B",
        tamanho: int = 400
    ) -> str:
        """Gera QR Code com a logo do Sabor e Prosa no centro."""
        
        # Criar QR Code
        qr = qrcode.QRCode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Criar imagem do QR Code
        qr_img = qr.make_image(fill_color=cor_qr, back_color=cor_fundo).convert('RGBA')
        qr_img = qr_img.resize((tamanho, tamanho))
        
        # Adicionar logo no centro
        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert('RGBA')
            logo_size = tamanho // 4
            logo = logo.resize((logo_size, logo_size))
            
            # Criar fundo branco circular para a logo
            pos = ((tamanho - logo_size) // 2, (tamanho - logo_size) // 2)
            qr_img.paste(logo, pos, logo)
        
        # Salvar
        output_dir = "app/static/qrcodes"
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"qrcode_{hash(url) % 100000}.png"
        filepath = f"{output_dir}/{filename}"
        qr_img.save(filepath)
        
        return f"/static/qrcodes/{filename}"
    
    @staticmethod
    def gerar_qrcode_para_impressao(
        url: str,
        titulo: str = "Sabor e Prosa Empório",
        subtitulo: str = "Escaneie e cadastre-se!",
        logo_path: str = "app/static/logo.png"
    ) -> str:
        """Gera QR Code em formato A4 pronto para impressão."""
        
        from PIL import ImageDraw, ImageFont
        
        # Criar QR Code
        qr = qrcode.QRCode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="#1A120B", back_color="#F5E6D3").convert('RGBA')
        qr_img = qr_img.resize((350, 350))
        
        # Criar tela A4 (794 x 1123 pixels @ 96dpi)
        a4 = Image.new('RGBA', (794, 1123), '#F5E6D3')
        
        # Adicionar logo
        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert('RGBA')
            logo = logo.resize((120, 120))
            a4.paste(logo, (337, 80), logo)
        
        # Adicionar QR Code
        a4.paste(qr_img, (222, 300))
        
        # Adicionar textos
        draw = ImageDraw.Draw(a4)
        try:
            font_grande = ImageFont.truetype("arial.ttf", 40)
        except:
            font_grande = ImageFont.load_default()
        
        draw.text((397, 250), titulo, fill='#1A120B', anchor='mm', font=font_grande)
        draw.text((397, 700), subtitulo, fill='#8B6B4A', anchor='mm', font=font_grande)
        draw.text((397, 1050), 'Desenvolvido por venure.com.br', fill='#8B6B4A', anchor='mm')
        
        # Salvar
        output_dir = "app/static/qrcodes"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"cartaz_{hash(url) % 100000}.png"
        filepath = f"{output_dir}/{filename}"
        a4.save(filepath)
        
        return f"/static/qrcodes/{filename}"
