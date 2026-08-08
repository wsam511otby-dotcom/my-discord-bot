import discord
from discord.ext import commands
import asyncio
import datetime
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="", intents=intents)

warnings = {}

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

@bot.command(name="تفو")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, duration: str = None):
    await member.ban(reason=f"Banned by {ctx.author}")

    if duration:
        units = {"m": 60, "h": 3600, "d": 86400}

        try:
            amount = int(duration[:-1])
            unit = duration[-1]

            if unit in units:
                await ctx.send(f"✅ تم تبنيد {member.mention} لمدة {duration}")

                await asyncio.sleep(amount * units[unit])

                guild = ctx.guild
                user = await bot.fetch_user(member.id)
                await guild.unban(user)

                await ctx.send(f"✅ انتهى الباند وتم فك الحظر عن {user}")

            else:
                await ctx.send("❌ استخدم m أو h أو d")

        except:
            await ctx.send("❌ مثال: تفو @user 7d")

    else:
        await ctx.send(f"✅ تم تبنيد {member.mention}")

@bot.command(name="برا")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
    await member.kick(reason=f"Kicked by {ctx.author}")
    await ctx.send(f"👢 تم طرد {member.mention}")@bot.command(name="إنذار")
@commands.has_permissions(moderate_members=True)
async def warn(ctx, member: discord.Member, *, reason="بدون سبب"):
    if member.id not in warnings:
        warnings[member.id] = []

    warnings[member.id].append(reason)

    await ctx.send(
        f"⚠️ تم إعطاء {member.mention} إنذار.\n"
        f"السبب: {reason}\n"
        f"عدد الإنذارات: {len(warnings[member.id])}"
    )


@bot.command(name="غفوه")
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, duration: str):
    units = {"m": 60, "h": 3600, "d": 86400}

    try:
        amount = int(duration[:-1])
        unit = duration[-1]

        if unit not in units:
            await ctx.send("❌ استخدم m أو h أو d")
            return

        until = discord.utils.utcnow() + datetime.timedelta(seconds=amount * units[unit])

        await member.timeout(until, reason=f"Timeout by {ctx.author}")

        await ctx.send(f"😴 تم إعطاء {member.mention} غفوه لمدة {duration}")

    except:
        await ctx.send("❌ مثال: غفوه @user 10m")


@bot.command(name="امسح")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🗑️ تم حذف {amount} رسالة")
    await asyncio.sleep(3)
    await msg.delete()


TOKENMTUzNTM2ODE1NjEwMzU3MzYwNg.GIuO9O.4uNworGd_-alU1chyZX1owNoAyN5rE8K9gbHYU
