## https://discordpy.readthedocs.io/en/stable/intro.html
## https://www.youtube.com/watch?v=jh1CtQW4DTo
## to stop running code its CTRL + C
## thanks to the api docs link here: https://python-tradingview-ta.readthedocs.io/en/latest/faq.html
from typing import List
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button
from discord.ui.item import Item
from tradingview_ta import TA_Handler, Interval, Exchange
from dislash import InteractionClient, ActionRow, Button, ButtonStyle


tesla = TA_Handler(
    symbol="TSLA",
    screener="america",
    exchange="NASDAQ",
    interval=Interval.INTERVAL_1_DAY
)


token = "SHHHH"
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.command()
async def test(ctx):
    analysis_summary = tesla.get_analysis().summary
    await ctx.send(analysis_summary)


@bot.event
async def on_ready():
    print("Successfully logged in!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")


intervals = ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"]


@bot.tree.command(name="analyze_stock", description="Analyze any stock on the go!")
@app_commands.describe(
    stock_symbol="The symbol of the stock to analyze",
    screener="The screener to use (e.g., 'america')",
    exchange="The exchange to use (e.g., 'NASDAQ')",
    interval="The interval to use (e.g., '1d', '1h')"
)
async def analyze_stock(
    interaction: discord.Interaction,
    stock_symbol: str,
    screener: str,
    exchange: str,
    interval: str
):
    
    if interval not in intervals:
        await interaction.response.send_message(f"Invalid interval '{interval}'. Valid intervals are: {', '.join(intervals)}")
        return

    handler = TA_Handler(
        symbol=stock_symbol,
        screener=screener,
        exchange=exchange,
        interval=interval
    )
    analysis = handler.get_analysis()
    analysis_summary = analysis.summary

   
    embed = discord.Embed(
        title=f"Stock Analysis for {stock_symbol}",
        color=discord.Color.blue()
    )
    embed.add_field(name="Summary", value=analysis_summary, inline=False)
    embed.add_field(name="Screener", value=screener, inline=True)
    embed.add_field(name="Exchange", value=exchange, inline=True)
    embed.add_field(name="Interval", value=interval, inline=True)
    embed.set_footer(text="Powered by TradingView TA")

    
    button = discord.ui.Button(
        label="Show Graph",
        style=discord.ButtonStyle.link,
        url=f"https://www.tradingview.com/chart/ZJgB05OV/?symbol={exchange}%3A{stock_symbol}"
    )

    
    view = discord.ui.View()
    view.add_item(button)

    
    await interaction.response.send_message(embed=embed, view=view)


@bot.event
async def on_ready():
    print("Successfully logged in!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")

bot.run(token)





## https://www.tradingview.com/chart/ZJgB05OV/?symbol={exchange}%3A{stock_symbol}

