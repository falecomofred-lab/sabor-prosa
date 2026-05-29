import subprocess
import os
from anthropic import Anthropic
from ..config import get_settings

settings = get_settings()

class VideoService:
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async def gerar_video(self, produto_nome: str, produto_desc: str, foto_path: str) -> dict:
        try:
            roteiro = await self._gerar_roteiro(produto_nome, produto_desc)
            legenda = roteiro.split('\n')[0][:80].replace("'", "").replace('"', '')
            video_path = self._criar_video_com_ffmpeg(foto_path, legenda, produto_nome)
            return {"sucesso": True, "video_url": video_path, "roteiro": roteiro, "legenda": legenda}
        except Exception as e:
            return {"sucesso": False, "erro": str(e)}
    
    async def _gerar_roteiro(self, nome: str, desc: str) -> str:
        prompt = f"Crie um roteiro de 15 segundos para video de produto de empório.\nProduto: {nome}\nDescrição: {desc}\n\nFormato:\n- Frase de abertura impactante (5 palavras)\n- Destaque do produto (1 frase)\n- Chamada para ação (3 palavras)\n- Hashtags: 3 hashtags relevantes"
        message = self.client.messages.create(model=settings.AI_MODEL, max_tokens=200, messages=[{"role": "user", "content": prompt}])
        return message.content[0].text
    
    def _criar_video_com_ffmpeg(self, foto_path: str, legenda: str, nome: str) -> str:
        output_dir = "static/videos"
        os.makedirs(output_dir, exist_ok=True)
        safe_name = nome.replace(' ', '_')[:30]
        output_path = f"{output_dir}/{safe_name}.mp4"
        foto = foto_path.strip() if foto_path and os.path.exists(foto_path.strip()) else "app/static/placeholder.jpg"
        cmd = ["ffmpeg", "-y", "-loop", "1", "-i", foto, "-vf", f"drawtext=text='{legenda}':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=h-th-20,fade=t=in:d=0.5,fade=t=out:d=0.5", "-t", "8", "-c:v", "libx264", "-pix_fmt", "yuv420p", output_path]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return f"/static/videos/{safe_name}.mp4"
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e}")
            return None
