import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# 1. 환경 변수 로드 (.env 파일 경로 지정)
load_dotenv('.env')
TOKEN = os.getenv('token')

# 2. 봇의 권한(Intents) 설정
# 서버 관리용 봇은 모든 권한을 주는 것이 편하지만, 보안상 필요한 것만 켜는 것이 좋습니다.
# 여기서는 모든 권한(all)을 활성화합니다.
intents = discord.Intents.all()

# 3. 봇 객체 생성 (명령어 접두사 설정, 예: !)
bot = commands.Bot(command_prefix='!', intents=intents)

# [이벤트] 봇이 준비되었을 때 실행
@bot.event
async def on_ready():
    print(f'로그인 완료: {bot.user.name}(ID: {bot.user.id})')
    print('------')
    # 상태 메시지 설정 (선택 사항)
    await bot.change_presence(activity=discord.Game(name="변신 중"))

# [명령어] 기본적인 테스트용 명령어 (!핑)
@bot.command()
async def 핑(ctx):
    await ctx.send(f'https://tenor.com/view/kamen-rider-revice-kamen-rider-live-kamen-rider-jeanne-kamen-rider-demons-kamen-rider-gif-25000168 {round(bot.latency * 1000)}ms')

# [명령어] 서버 관리 예시: 메시지 삭제 (!청소 10)
@bot.command(name="청소")
@commands.has_permissions(manage_messages=True) # 메시지 관리 권한이 있는 사람만 사용 가능
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'{amount}개의 메시지를 삭제했습니다.', delete_after=3)

# 에러 처리 (권한 부족 등)
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("이 명령어를 사용할 권한이 없습니다.")

# 4. 봇 실행
if TOKEN:
    bot.run(TOKEN)
else:
    print("토큰을 찾을 수 없습니다. data.env 파일을 확인하세요.")