import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

# 1. 환경 변수 로드 (.env 파일 기본 로드)
load_dotenv()
TOKEN = os.getenv('token')

# 2. 봇 클래스 설정
class MyBot(commands.Bot):
    def __init__(self):
        # 서버 관리용이므로 모든 인텐트 활성화
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    # 슬래시 명령어 동기화를 위한 setup_hook
    async def setup_hook(self):
        try:
            # 작성된 슬래시 명령어를 디스코드 서버에 등록
            synced = await self.tree.sync()
            print(f"동기화 완료: {len(synced)}개의 슬래시 명령어")
        except Exception as e:
            print(f"동기화 에러: {e}")

bot = MyBot()

# [이벤트] 봇이 준비되었을 때
@bot.event
async def on_ready():
    print(f'로그인 완료: {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="/명령어 확인"))

# [슬래시 명령어] 핑 테스트
@bot.tree.command(name="핑", description="봇의 상태를 확인합니다.")
async def ping(interaction: discord.Interaction):
    # 슬래시 명령어는 ctx 대신 interaction을 사용합니다.
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"https://tenor.com/view/kamen-rider-revice-kamen-rider-live-kamen-rider-jeanne-kamen-rider-demons-kamen-rider-gif-25000168 (지연 시간: {latency}ms)")

# [슬래시 명령어] 메시지 청소
@bot.tree.command(name="청소", description="메시지를 대량으로 삭제합니다.")
@app_commands.describe(수량="삭제할 메시지의 개수를 입력하세요.")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, 수량: int):
    # 먼저 응답을 보내기 전에 '생각 중...' 상태를 만듦 (삭제 작업이 길어질 수 있음)
    await interaction.response.defer(ephemeral=True) 
    
    deleted = await interaction.channel.purge(limit=수량)
    await interaction.followup.send(f"✅ {len(deleted)}개의 메시지를 삭제했습니다.")

# [에러 처리] 권한이 없는 사용자가 명령어를 사용했을 때
@clear.error
async def clear_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ 이 명령어를 사용할 권한(메시지 관리)이 없습니다.", ephemeral=True)

# 3. 봇 실행
if TOKEN:
    bot.run(TOKEN)
else:
    print("에러: .env 파일에서 'token'을 찾을 수 없습니다.")