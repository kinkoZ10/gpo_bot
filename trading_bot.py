import discord
from discord.ext import commands
import re
import random

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Item Aliases - Shortcuts for item names
ALIASES = {
    "sks": "soul king scarf",
    "skg": "soul king guitar",
    "db": "dark blade",
    "we": "world ender",
    "hws": "hollow's great sword",
    "tbg": "true baal's guard"
}

# Boss Wiki Data
BOSS_DATA = {
    "res baal": {
        "name": "Resurrected Ba'al",
        "drops": [
            {"item": "Hollow's Halberd", "chance": "5%"},
            {"item": "Resurrected Ba'al's Outfit", "chance": "5%"},
            {"item": "Resurrected Ba'al's Head", "chance": "0.5%"}
        ]
    },
    "kizaru": {
        "name": "Radiant Admiral (Kizaru)",
        "drops": [
            {"item": "Radiant Admiral's Outfit", "chance": "1%"},
            {"item": "Radiant Shades", "chance": "5%"},
            {"item": "Radiant Admiral's Cape", "chance": "1%"},
            {"item": "Pika Grip", "chance": "1%"}
        ]
    },
    "true baal": {
        "name": "True Demon Ba'al",
        "drops": [
            {"item": "True Ba'al's Guard", "chance": "2%"},
            {"item": "Hollow's Great Sword", "chance": "2%"},
            {"item": "True Ba'al's Snake Head", "chance": "5%"},
            {"item": "True Ba'al's Snake Fire", "chance": "20%"},
            {"item": "True Ba'al's Horns", "chance": "5%"},
            {"item": "Hollow's World Ender", "chance": "0.5%"},
            {"item": "Prestige World Ender", "chance": "0.001%"},
            {"item": "Endbringer Wings", "chance": "1%"},
            {"item": "Endbringer Armor", "chance": "1%"}
        ]
    },
    "whitebeard": {
        "name": "Captain Zhen (Whitebeard)",
        "drops": [
            {"item": "Bisento", "chance": "15%"},
            {"item": "Captain Zhen's Cape", "chance": "25%"}
        ]
    },
    "law": {
        "name": "Law",
        "drops": [
            {"item": "Law's Cap", "chance": "5%"},
            {"item": "Law's Outfit", "chance": "15%"},
            {"item": "Law's Cape", "chance": "15%"},
            {"item": "Ope Scramble", "chance": "1%"},
            {"item": "Kikoku", "chance": "0.5%"}
        ]
    },
    "mihawk": {
        "name": "Hawk Eye (Mihawk)",
        "drops": [
            {"item": "Mihawk's Hat", "chance": "1%"},
            {"item": "Hawk Eye's Outfit", "chance": "1%"},
            {"item": "Triple Strongest Slash Scroll", "chance": "1%"},
            {"item": "Dark Blade", "chance": "0.5%"},
            {"item": "Legendary Fruit Chest Blue-print", "chance": "1%"}
        ]
    },
    "juzo": {
        "name": "Juzo the Diamondback",
        "drops": [
            {"item": "Kira Kira no Mi", "chance": "5%"},
            {"item": "Turtleback Helmet", "chance": "1%"},
            {"item": "Turtleback Armor", "chance": "1%"},
            {"item": "Mythical Fruit Chest", "chance": "~0.5%"}
        ]
    },
    "brook": {
        "name": "Soul King (Brook)",
        "drops": [
            {"item": "Soul King's Outfit (Normal)", "chance": "1%"},
            {"item": "Soul King's Shades (Normal)", "chance": "~5%"},
            {"item": "Soul King's Violin (Normal)", "chance": "~5%"},
            {"item": "Soul Cane (Normal)", "chance": "1%"},
            {"item": "Soul King's Shades (Rockstar)", "chance": "~5%"},
            {"item": "Soul King's Outfit (Rockstar)", "chance": "~7%"},
            {"item": "Soul King's Top Hat (Rockstar)", "chance": "1%"},
            {"item": "Soul King's Rockstar Outfit (Rockstar)", "chance": "~5%"},
            {"item": "Soul King's Scarf (Rockstar)", "chance": "0.5%"},
            {"item": "Soul Cane (Rockstar)", "chance": "1%"}
        ]
    },
    "roger": {
        "name": "Roger",
        "drops": [
            {"item": "Roger Hat", "chance": "1%"},
            {"item": "Roger Fit", "chance": "1%"},
            {"item": "Roger's Ace", "chance": "0.5%"}
        ]
    }
}

# Watashi Ruby Values Dictionary
VALUES = {
    "ito": 80,
    "paw": 50,
    "kage": 50,
    "gura": 150,
    "goro": 100,
    "yami": 50,
    "zushi": 150,
    "hie": 150,
    "suna": 500,
    "yuki": 100,
    "mera": 200,
    "magu": 500,
    "guro": 100,
    "smoke": 100,
    "pika": 2000,
    "kira": 100,
    "ope": 1200,
    "tori": 4000,
    "buddha": 1400,
    "ptero": 3200,
    "venom": 6500,
    "mochi": 7500,
    "1m peli": 500,
    "mc": 9500,
    "ase": 32000,
    "baal ase": 35000,
    "blo ase": 37000,
    "chromatic ase": 120000,
    "hoverboard": 500,
    "coffin boat": 600,
    "striker": 600,
    "sunken anchor": 400,
    "boneshiver": 400,
    "ace": 1000,
    "yoru": 4200,
    "kikoku": 9500,
    "soul king guitar": 1800,
    "soul king scarf": 27000,
    "roger fit": 700,
    "roger hat": 150,
    "mihawk hat": 100,
    "mihawk fit": 300,
    "candy cane": 77000,
    "cc": 77000,
    "og santa hat": 3000,
    "flowers": 13000,
    "baal head": 1500,
    "jscythe": 600,
    "jfit": 48000,
    "elo hammer": 1200,
    "cupid wings": 1700,
    "festival shield": 500,
    "res baal head": 1000,
    "stark guns": 2000,
    "coyote outfit": 4500,
    "world ender": 15000,
    "isoh": 2500,
    "toji fit": 700,
    "yukio": 16000,
    "blood scythe": 200,
    "nfs": 5500,
    "bless exalted outfit": 2000,
    "blessed cupid scarf": 2750,
    "exalted cupid wings": 1500,
    "blessed exalted wings": 22000,
    "mega pow": 4000,
    "anomalized mega pow": 94000,
    "blo crimson hammer": 1500,
    "kumawaka head": 1400,
    "bunyo": 7500,
    "swordfish rapier": 500,
    "nfhs": 1200,
    "hollow wender": 3200,
    "hwe": 3200,
    "endbringer set": 1400,
    "odm rod": 3000,
    "titan aura": 60000,
    "df rod": 30000,
    "pteranodon": 3200,
    "mega paw": 4000,
    "mp": 4000,
    "lc": 700,
    "legendary chest": 700
}

def parse_items(item_string):
    """Parse item string and return list of (item_name, quantity, value)"""
    items = []
    item_string = item_string.lower().strip()
    
    # Replace common separators with spaces
    item_string = item_string.replace(',', ' ')
    
    # Split into tokens
    tokens = item_string.split()
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        # Check if token is a number (quantity)
        if token.isdigit():
            quantity = int(token)
            i += 1
            
            # Skip 'x' if present
            if i < len(tokens) and tokens[i].lower() == 'x':
                i += 1
            
            # Now get the item name (might be multi-word)
            if i >= len(tokens):
                break
                
            # Try to build item name
            item_name = ""
            matched = False
            
            # Try progressively longer names
            for j in range(i, len(tokens)):
                if tokens[j].isdigit():
                    break
                item_name = " ".join(tokens[i:j+1])
                
                # Check if it's an alias first
                if item_name in ALIASES:
                    item_name = ALIASES[item_name]
                    matched = True
                    i = j + 1
                    break
                
                # Check if it's a regular item
                if item_name in VALUES:
                    matched = True
                    i = j + 1
                    break
            
            if matched:
                value = VALUES[item_name]
                items.append((item_name, quantity, value))
            else:
                # Couldn't find item, skip
                i += 1
                
        else:
            # No quantity specified, try to match item name
            item_name = ""
            matched = False
            
            # Try progressively longer names
            for j in range(i, len(tokens)):
                if tokens[j].isdigit():
                    break
                item_name = " ".join(tokens[i:j+1])
                
                # Check if it's an alias first
                if item_name in ALIASES:
                    item_name = ALIASES[item_name]
                    matched = True
                    i = j + 1
                    break
                
                # Check if it's a regular item
                if item_name in VALUES:
                    matched = True
                    i = j + 1
                    break
            
            if matched:
                value = VALUES[item_name]
                items.append((item_name, 1, value))
            else:
                # Couldn't match, skip this token
                i += 1
    
    return items

def calculate_total(items):
    """Calculate total value of items"""
    return sum(quantity * value for _, quantity, value in items)

def format_items(items):
    """Format items for display"""
    if not items:
        return "Nothing"
    
    formatted = []
    for item_name, quantity, value in items:
        if quantity > 1:
            formatted.append(f"{quantity}x {item_name.title()} ({value * quantity})")
        else:
            formatted.append(f"{item_name.title()} ({value})")
    
    return " + ".join(formatted)

@bot.event
async def on_ready():
    print(f'{bot.user} is now online!')
    print(f'Connected to {len(bot.guilds)} servers')

@bot.command(name='trade')
async def trade(ctx, *, trade_string: str):
    """
    Compare trade values
    Usage: !trade [your items] for [their items]
    Example: !trade 2mc yoru for tori mochi
    """
    try:
        # Split by "for"
        if " for " not in trade_string.lower():
            await ctx.send("❌ Please use format: `!trade [your items] for [their items]`")
            return
        
        parts = re.split(r'\s+for\s+', trade_string, flags=re.IGNORECASE)
        if len(parts) != 2:
            await ctx.send("❌ Invalid format. Use: `!trade [your items] for [their items]`")
            return
        
        your_items_str, their_items_str = parts
        
        # Parse items
        your_items = parse_items(your_items_str)
        their_items = parse_items(their_items_str)
        
        if not your_items:
            await ctx.send("❌ Couldn't find any valid items in your trade!")
            return
        if not their_items:
            await ctx.send("❌ Couldn't find any valid items in their trade!")
            return
        
        # Calculate totals
        your_total = calculate_total(your_items)
        their_total = calculate_total(their_items)
        
        # Calculate deficit/profit
        net_value = their_total - your_total
        percentage = (net_value / your_total * 100) if your_total > 0 else 0
        
        # Determine result
        if net_value > 0:
            result_emoji = "✅"
            result_text = "You are winning!!!"
            summary_emoji = "▲"
            summary_text = f"Net Profit: +{net_value:,} • +{percentage:.2f}%"
        elif net_value < 0:
            result_emoji = "❌"
            result_text = "You are losing!!!"
            summary_emoji = "▼"
            summary_text = f"Net Deficit: {net_value:,} • {percentage:.2f}%"
        else:
            result_emoji = "⚖️"
            result_text = "Fair trade!"
            summary_emoji = "="
            summary_text = "Net: 0 • 0.00%"
        
        # Create embed
        embed = discord.Embed(
            title="🔻 Trade Comparison",
            color=discord.Color.red() if net_value < 0 else discord.Color.green() if net_value > 0 else discord.Color.blue()
        )
        
        embed.add_field(
            name="💰 Your Trade",
            value=format_items(your_items),
            inline=False
        )
        
        embed.add_field(
            name="🎁 Their Trade",
            value=format_items(their_items),
            inline=False
        )
        
        embed.add_field(
            name="Your Total",
            value=f"❌ {your_total:,}",
            inline=True
        )
        
        embed.add_field(
            name="Their Total",
            value=f"✅ {their_total:,}",
            inline=True
        )
        
        embed.add_field(
            name="Summary",
            value=f"{summary_emoji} {summary_text}",
            inline=False
        )
        
        embed.add_field(
            name="Result",
            value=f"{result_emoji} **{result_text}**",
            inline=False
        )
        
        embed.set_footer(text="Watashi Ruby Values • Based on current list")
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Error processing trade: {str(e)}")
        print(f"Error: {e}")

@bot.command(name='value')
async def value(ctx, *, item_name: str):
    """
    Check the value of an item
    Usage: !value [item name]
    Example: !value yoru
    """
    item_name = item_name.lower().strip()
    
    if item_name in VALUES:
        embed = discord.Embed(
            title="💎 Item Value",
            color=discord.Color.blue()
        )
        embed.add_field(
            name=item_name.title(),
            value=f"**{VALUES[item_name]:,}** value",
            inline=False
        )
        await ctx.send(embed=embed)
    else:
        # Try to find similar items
        suggestions = [item for item in VALUES.keys() if item_name in item]
        if suggestions:
            suggestion_text = ", ".join([f"`{s}`" for s in suggestions[:5]])
            await ctx.send(f"❌ Item not found. Did you mean: {suggestion_text}?")
        else:
            await ctx.send(f"❌ Item `{item_name}` not found in value list!")

@bot.command(name='list')
async def list_values(ctx):
    """Show all available items"""
    items_text = ", ".join([f"`{item}`" for item in sorted(VALUES.keys())[:50]])
    embed = discord.Embed(
        title="📋 Available Items (First 50)",
        description=items_text,
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Total items: {len(VALUES)} | Use !value [item] to check value")
    await ctx.send(embed=embed)

@bot.command(name='wiki')
async def wiki(ctx, *, boss_name: str):
    """
    Show boss information and drops
    Usage: !wiki [boss name]
    Example: !wiki kraken
    """
    boss_name = boss_name.lower().strip()
    
    if boss_name in BOSS_DATA:
        boss = BOSS_DATA[boss_name]
        
        embed = discord.Embed(
            title=f"📖 {boss['name']}",
            color=discord.Color.purple()
        )
        
        # Add drops
        drops_text = ""
        for drop in boss['drops']:
            drops_text += f"• **{drop['item']}** - {drop['chance']}\n"
        
        embed.add_field(
            name="💎 Drops",
            value=drops_text if drops_text else "No drops listed",
            inline=False
        )
        
        embed.set_footer(text="GPO Boss Wiki")
        
        await ctx.send(embed=embed)
    else:
        # Try to find similar boss names
        suggestions = [boss for boss in BOSS_DATA.keys() if boss_name in boss]
        if suggestions:
            suggestion_text = ", ".join([f"`{s}`" for s in suggestions])
            await ctx.send(f"❌ Boss not found. Did you mean: {suggestion_text}?")
        else:
            await ctx.send(f"❌ Boss `{boss_name}` not found! Use `!bosslist` to see all bosses.")

@bot.command(name='bosslist')
async def bosslist(ctx):
    """Show all available bosses"""
    bosses_text = ", ".join([f"`{boss}`" for boss in sorted(BOSS_DATA.keys())])
    embed = discord.Embed(
        title="📋 Available Bosses",
        description=bosses_text if bosses_text else "No bosses added yet",
        color=discord.Color.purple()
    )
    embed.set_footer(text="Use !wiki [boss name] to see boss info")
    await ctx.send(embed=embed)

@bot.command(name='search')
async def search(ctx, *, query: str):
    """
    Search for items by name or value range
    Usage: 
    - !search fruit (search by name)
    - !search <5000 (items under 5000)
    - !search >10000 (items over 10000)
    - !search 1000-5000 (items between 1000-5000)
    """
    query = query.strip()
    results = []
    
    # Check if it's a value range query
    if query.startswith('<'):
        # Less than
        try:
            max_value = int(query[1:].strip())
            results = [(item, value) for item, value in VALUES.items() if value < max_value]
            title = f"Items Under {max_value:,}"
        except:
            await ctx.send("❌ Invalid format. Use: `!search <5000`")
            return
            
    elif query.startswith('>'):
        # Greater than
        try:
            min_value = int(query[1:].strip())
            results = [(item, value) for item, value in VALUES.items() if value > min_value]
            title = f"Items Over {min_value:,}"
        except:
            await ctx.send("❌ Invalid format. Use: `!search >10000`")
            return
            
    elif '-' in query and query.replace('-', '').replace(' ', '').isdigit():
        # Range
        try:
            parts = query.split('-')
            min_value = int(parts[0].strip())
            max_value = int(parts[1].strip())
            results = [(item, value) for item, value in VALUES.items() if min_value <= value <= max_value]
            title = f"Items Between {min_value:,} - {max_value:,}"
        except:
            await ctx.send("❌ Invalid format. Use: `!search 1000-5000`")
            return
    else:
        # Name search
        query_lower = query.lower()
        results = [(item, value) for item, value in VALUES.items() if query_lower in item]
        title = f"Items Matching '{query}'"
    
    if not results:
        await ctx.send(f"❌ No items found for: `{query}`")
        return
    
    # Sort by value
    results.sort(key=lambda x: x[1], reverse=True)
    
    # Limit to 25 items for display
    if len(results) > 25:
        results = results[:25]
        footer_text = f"Showing top 25 of {len(results)} results"
    else:
        footer_text = f"Found {len(results)} items"
    
    # Format results
    items_text = ""
    for item, value in results:
        items_text += f"**{item.title()}** - {value:,}\n"
    
    embed = discord.Embed(
        title=f"🔍 {title}",
        description=items_text,
        color=discord.Color.blue()
    )
    embed.set_footer(text=footer_text)
    
    await ctx.send(embed=embed)

@bot.command(name='calc')
async def calculator(ctx, *, items: str):
    """
    Calculate total value of multiple items
    Usage: !calc 3mc + 2yoru + tori
    Also works with: !calc 3mc 2yoru tori
    """
    # Replace + with space for easier parsing
    items = items.replace('+', ' ')
    
    # Parse items
    parsed_items = parse_items(items)
    
    if not parsed_items:
        await ctx.send("❌ Couldn't find any valid items!")
        return
    
    # Calculate total
    total = calculate_total(parsed_items)
    
    # Format output
    items_list = ""
    for item_name, quantity, value in parsed_items:
        if quantity > 1:
            items_list += f"• {quantity}x **{item_name.title()}** ({value:,} each) = {value * quantity:,}\n"
        else:
            items_list += f"• **{item_name.title()}** = {value:,}\n"
    
    embed = discord.Embed(
        title="🧮 Value Calculator",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="Items",
        value=items_list,
        inline=False
    )
    
    embed.add_field(
        name="💰 Total Value",
        value=f"**{total:,}**",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='fair')
async def fair_trade(ctx, *, item_name: str):
    """
    Suggest fair trades for an item
    Usage: !fair yoru
    """
    item_name = item_name.lower().strip()
    
    if item_name not in VALUES:
        await ctx.send(f"❌ Item `{item_name}` not found!")
        return
    
    item_value = VALUES[item_name]
    
    # Find items with similar value (within 20% range)
    margin = item_value * 0.20
    min_val = item_value - margin
    max_val = item_value + margin
    
    similar_items = [(item, value) for item, value in VALUES.items() 
                     if min_val <= value <= max_val and item != item_name]
    
    # Sort by how close they are to the target value
    similar_items.sort(key=lambda x: abs(x[1] - item_value))
    
    # Get exact matches and close matches
    exact_matches = [item for item in similar_items if item[1] == item_value]
    close_matches = [item for item in similar_items if item[1] != item_value][:10]
    
    embed = discord.Embed(
        title=f"🤝 Fair Trades for {item_name.title()}",
        description=f"Value: **{item_value:,}**",
        color=discord.Color.gold()
    )
    
    # Exact value matches
    if exact_matches:
        exact_text = ""
        for item, value in exact_matches[:5]:
            exact_text += f"• **{item.title()}** ({value:,}) - Perfect match\n"
        embed.add_field(
            name="⚖️ Exact Value Matches",
            value=exact_text,
            inline=False
        )
    
    # Close matches
    if close_matches:
        close_text = ""
        for item, value in close_matches[:8]:
            diff = value - item_value
            if diff > 0:
                close_text += f"• **{item.title()}** ({value:,}) - You gain +{diff:,}\n"
            else:
                close_text += f"• **{item.title()}** ({value:,}) - You lose {diff:,}\n"
        embed.add_field(
            name="📊 Close Matches",
            value=close_text,
            inline=False
        )
    
    # Suggest combinations for higher value items
    if item_value > 5000:
        combinations = []
        for item1, val1 in VALUES.items():
            if val1 < item_value:
                needed = item_value - val1
                margin_small = needed * 0.15
                for item2, val2 in VALUES.items():
                    if item1 != item2 and abs(val2 - needed) <= margin_small:
                        total = val1 + val2
                        diff = total - item_value
                        combinations.append((item1, val1, item2, val2, total, diff))
        
        # Sort by closest to target value
        combinations.sort(key=lambda x: abs(x[5]))
        
        if combinations[:3]:
            combo_text = ""
            for item1, val1, item2, val2, total, diff in combinations[:3]:
                if diff >= 0:
                    combo_text += f"• **{item1.title()}** ({val1:,}) + **{item2.title()}** ({val2:,}) = {total:,} (+{diff:,})\n"
                else:
                    combo_text += f"• **{item1.title()}** ({val1:,}) + **{item2.title()}** ({val2:,}) = {total:,} ({diff:,})\n"
            
            embed.add_field(
                name="💡 Combo Suggestions",
                value=combo_text,
                inline=False
            )
    
    embed.set_footer(text="These are fair trades based on Watashi Ruby values")
    
    await ctx.send(embed=embed)

@bot.command(name='drop')
async def drop_simulator(ctx, *, boss_name: str):
    """
    Simulate a boss drop
    Usage: !drop [boss name]
    Example: !drop mihawk
    """
    boss_name = boss_name.lower().strip()
    
    if boss_name not in BOSS_DATA:
        await ctx.send(f"❌ Boss `{boss_name}` not found! Use `!bosslist` to see all bosses.")
        return
    
    boss = BOSS_DATA[boss_name]
    
    # Simulate drops
    dropped_items = []
    
    for drop in boss['drops']:
        # Parse the percentage (handle formats like "5%", "~5%", "0.5%", "0.001%")
        chance_str = drop['chance'].replace('~', '').replace('%', '').strip()
        
        try:
            chance = float(chance_str)
            
            # Roll the dice
            roll = random.uniform(0, 100)
            
            if roll <= chance:
                dropped_items.append(drop['item'])
        except:
            # If parsing fails, skip this drop
            continue
    
    # Create embed
    if dropped_items:
        # Got drops!
        embed = discord.Embed(
            title=f"🎉 {boss['name']} Drop Result",
            description=f"{ctx.author.mention} defeated **{boss['name']}**!",
            color=discord.Color.green()
        )
        
        drops_text = ""
        for item in dropped_items:
            drops_text += f"✨ **{item}**\n"
        
        embed.add_field(
            name="💎 You got:",
            value=drops_text,
            inline=False
        )
        
        embed.set_footer(text="🍀 Lucky drop!")
    else:
        # Nothing dropped
        embed = discord.Embed(
            title=f"💔 {boss['name']} Drop Result",
            description=f"{ctx.author.mention} defeated **{boss['name']}**...",
            color=discord.Color.red()
        )
        
        embed.add_field(
            name="💎 You got:",
            value="**Nothing**",
            inline=False
        )
        
        embed.set_footer(text="Better luck next time!")
    
    await ctx.send(embed=embed)

@bot.command(name='setvalue')
@commands.has_permissions(administrator=True)
async def set_value(ctx, item_name: str, value: int):
    """
    Set or update an item's value (Admin only)
    Usage: !setvalue [item name] [value]
    Example: !setvalue yoru 4500
    """
    item_name = item_name.lower().strip()
    
    old_value = VALUES.get(item_name, None)
    VALUES[item_name] = value
    
    embed = discord.Embed(
        title="✅ Value Updated",
        color=discord.Color.green()
    )
    
    if old_value:
        embed.add_field(
            name=item_name.title(),
            value=f"Old value: {old_value:,}\nNew value: {value:,}\nChange: {value - old_value:+,}",
            inline=False
        )
    else:
        embed.add_field(
            name=item_name.title(),
            value=f"Added with value: {value:,}",
            inline=False
        )
    
    embed.set_footer(text=f"Updated by {ctx.author.name}")
    await ctx.send(embed=embed)

@set_value.error
async def set_value_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need Administrator permissions to use this command!")

@bot.command(name='removeitem')
@commands.has_permissions(administrator=True)
async def remove_item(ctx, *, item_name: str):
    """
    Remove an item from the value list (Admin only)
    Usage: !removeitem [item name]
    Example: !removeitem old item
    """
    item_name = item_name.lower().strip()
    
    if item_name in VALUES:
        old_value = VALUES[item_name]
        del VALUES[item_name]
        
        embed = discord.Embed(
            title="🗑️ Item Removed",
            description=f"**{item_name.title()}** ({old_value:,}) has been removed from the value list.",
            color=discord.Color.orange()
        )
        embed.set_footer(text=f"Removed by {ctx.author.name}")
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"❌ Item `{item_name}` not found in value list!")

@remove_item.error
async def remove_item_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need Administrator permissions to use this command!")

@bot.command(name='bulk')
async def bulk_trade(ctx, *, item_name: str):
    """
    Show all fair trade options for an item
    Usage: !bulk [item name]
    Example: !bulk mc
    """
    item_name = item_name.lower().strip()
    
    if item_name not in VALUES:
        await ctx.send(f"❌ Item `{item_name}` not found!")
        return
    
    item_value = VALUES[item_name]
    
    # Find all possible trades
    # 1. Single item trades (within 10% range)
    margin = item_value * 0.10
    single_trades = [(item, value) for item, value in VALUES.items() 
                     if abs(value - item_value) <= margin and item != item_name]
    single_trades.sort(key=lambda x: abs(x[1] - item_value))
    
    # 2. Two item combinations (within 15% range of target)
    combo_margin = item_value * 0.15
    two_item_combos = []
    
    items_list = list(VALUES.items())
    for i, (item1, val1) in enumerate(items_list):
        if val1 >= item_value:
            continue
        for item2, val2 in items_list[i+1:]:
            if item1 == item_name or item2 == item_name:
                continue
            total = val1 + val2
            if abs(total - item_value) <= combo_margin:
                diff = total - item_value
                two_item_combos.append((item1, val1, item2, val2, total, diff))
    
    two_item_combos.sort(key=lambda x: abs(x[5]))
    
    # Create embed
    embed = discord.Embed(
        title=f"📊 Bulk Trade Options for {item_name.title()}",
        description=f"Value: **{item_value:,}**",
        color=discord.Color.blue()
    )
    
    # Single item trades
    if single_trades[:8]:
        single_text = ""
        for item, value in single_trades[:8]:
            diff = value - item_value
            if diff == 0:
                single_text += f"• **{item.title()}** ({value:,}) - Perfect match ⚖️\n"
            elif diff > 0:
                single_text += f"• **{item.title()}** ({value:,}) - You gain +{diff:,} ✅\n"
            else:
                single_text += f"• **{item.title()}** ({value:,}) - You lose {diff:,} ❌\n"
        
        embed.add_field(
            name="1️⃣ Single Item Trades",
            value=single_text,
            inline=False
        )
    
    # Two item combos
    if two_item_combos[:6]:
        combo_text = ""
        for item1, val1, item2, val2, total, diff in two_item_combos[:6]:
            if diff >= 0:
                combo_text += f"• **{item1.title()}** ({val1:,}) + **{item2.title()}** ({val2:,}) = {total:,} (+{diff:,}) ✅\n"
            else:
                combo_text += f"• **{item1.title()}** ({val1:,}) + **{item2.title()}** ({val2:,}) = {total:,} ({diff:,}) ❌\n"
        
        embed.add_field(
            name="2️⃣ Two Item Combos",
            value=combo_text,
            inline=False
        )
    
    if not single_trades and not two_item_combos:
        embed.add_field(
            name="No Results",
            value="No close trade matches found for this item.",
            inline=False
        )
    
    embed.set_footer(text=f"Showing best trade options • Use !trade to check specific trades")
    
    await ctx.send(embed=embed)

@bot.command(name='addalias')
@commands.has_permissions(administrator=True)
async def add_alias(ctx, shortcut: str, *, item_name: str):
    """
    Add a shortcut/alias for an item name (Admin only)
    Usage: !addalias [shortcut] [full item name]
    Example: !addalias sks soul king scarf
    """
    shortcut = shortcut.lower().strip()
    item_name = item_name.lower().strip()
    
    # Check if the item exists
    if item_name not in VALUES:
        await ctx.send(f"❌ Item `{item_name}` not found in value list! Add the item first with `!setvalue`")
        return
    
    # Add alias
    ALIASES[shortcut] = item_name
    
    embed = discord.Embed(
        title="✅ Alias Added",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="Shortcut",
        value=f"`{shortcut}`",
        inline=True
    )
    
    embed.add_field(
        name="Full Name",
        value=f"`{item_name}`",
        inline=True
    )
    
    embed.add_field(
        name="Value",
        value=f"{VALUES[item_name]:,}",
        inline=True
    )
    
    embed.set_footer(text=f"Added by {ctx.author.name} • Users can now use !value {shortcut}")
    await ctx.send(embed=embed)

@add_alias.error
async def add_alias_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need Administrator permissions to use this command!")

@bot.command(name='removealias')
@commands.has_permissions(administrator=True)
async def remove_alias(ctx, shortcut: str):
    """
    Remove an alias/shortcut (Admin only)
    Usage: !removealias [shortcut]
    Example: !removealias sks
    """
    shortcut = shortcut.lower().strip()
    
    if shortcut in ALIASES:
        item_name = ALIASES[shortcut]
        del ALIASES[shortcut]
        
        embed = discord.Embed(
            title="🗑️ Alias Removed",
            description=f"Shortcut `{shortcut}` (for **{item_name}**) has been removed.",
            color=discord.Color.orange()
        )
        embed.set_footer(text=f"Removed by {ctx.author.name}")
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"❌ Alias `{shortcut}` not found!")

@remove_alias.error
async def remove_alias_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need Administrator permissions to use this command!")

@bot.command(name='aliases')
async def list_aliases(ctx):
    """
    Show all available aliases/shortcuts
    Usage: !aliases
    """
    if not ALIASES:
        await ctx.send("No aliases have been added yet!")
        return
    
    embed = discord.Embed(
        title="🏷️ Item Aliases & Shortcuts",
        description="Use these shortcuts instead of full item names!",
        color=discord.Color.blue()
    )
    
    # Sort aliases alphabetically
    sorted_aliases = sorted(ALIASES.items())
    
    aliases_text = ""
    for shortcut, item_name in sorted_aliases:
        value = VALUES.get(item_name, "???")
        aliases_text += f"`{shortcut}` → **{item_name.title()}** ({value:,})\n"
    
    embed.add_field(
        name="Available Shortcuts",
        value=aliases_text,
        inline=False
    )
    
    embed.set_footer(text=f"Total aliases: {len(ALIASES)} • Example: !value sks")
    
    await ctx.send(embed=embed)

@bot.command(name='announce')
@commands.has_permissions(administrator=True)
async def announce(ctx, channel: discord.TextChannel, *, message: str):
    """
    Send an announcement through the bot to a specific channel (Admin only)
    Usage: !announce [#channel] [message]
    Example: !announce #announcements Server maintenance tonight!
    """
    try:
        # Create embed for announcement
        embed = discord.Embed(
            description=message,
            color=discord.Color.blue(),
            timestamp=ctx.message.created_at
        )
        
        # Send to target channel
        await channel.send(embed=embed)
        
        # Confirm to admin
        await ctx.send(f"✅ Announcement sent to {channel.mention}!")
        
        # Delete the command message for cleanliness
        try:
            await ctx.message.delete()
        except:
            pass
            
    except discord.Forbidden:
        await ctx.send(f"❌ I don't have permission to send messages in {channel.mention}!")
    except Exception as e:
        await ctx.send(f"❌ Error sending announcement: {str(e)}")

@announce.error
async def announce_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need Administrator permissions to use this command!")
    elif isinstance(error, commands.ChannelNotFound):
        await ctx.send("❌ Channel not found! Make sure to mention the channel like #announcements")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Usage: `!announce #channel Your message here`")

@bot.command(name='say')
@commands.has_permissions(administrator=True)
async def say(ctx, *, message: str):
    """
    Make the bot say something in the current channel (Admin only)
    Usage: !say [message]
    Example: !say Hello everyone!
    """
    try:
        # Send the message
        await ctx.send(message)
        
        # Delete the command message
        try:
            await ctx.message.delete()
        except:
            pass
            
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need Administrator permissions to use this command!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Usage: `!say Your message here`")

@bot.command(name='embed')
@commands.has_permissions(administrator=True)
async def custom_embed(ctx, title: str, *, description: str):
    """
    Send a custom embed message (Admin only)
    Usage: !embed [title] [description]
    Example: !embed "Important Update" This is the announcement text
    """
    try:
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.gold(),
            timestamp=ctx.message.created_at
        )
        
        await ctx.send(embed=embed)
        
        # Delete command message
        try:
            await ctx.message.delete()
        except:
            pass
            
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@custom_embed.error
async def embed_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need Administrator permissions to use this command!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('❌ Usage: `!embed "Title Here" Description text here`')

@bot.command(name='commands')
async def commands_list(ctx):
    """Show help information"""
    embed = discord.Embed(
        title="🤖 WatashiRuby Trading Bot Commands",
        description="Compare trade values using Watashi Ruby values",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="!trade [your items] for [their items]",
        value="Compare a trade\nExample: `!trade 2mc yoru for tori mochi`",
        inline=False
    )
    
    embed.add_field(
        name="!value [item name]",
        value="Check an item's value\nExample: `!value yoru` or `!value sks`",
        inline=False
    )
    
    embed.add_field(
        name="!calc [items]",
        value="Calculate total value\nExample: `!calc 3mc + 2yoru + tori`",
        inline=False
    )
    
    embed.add_field(
        name="!search [query]",
        value="Search items\nExamples: `!search fruit`, `!search <5000`, `!search 1000-5000`",
        inline=False
    )
    
    embed.add_field(
        name="!fair [item]",
        value="Find fair trades for an item\nExample: `!fair yoru`",
        inline=False
    )
    
    embed.add_field(
        name="!bulk [item]",
        value="Show all trade options for an item\nExample: `!bulk mc`",
        inline=False
    )
    
    embed.add_field(
        name="!aliases",
        value="Show all item shortcuts\nExample: Use `sks` instead of `soul king scarf`",
        inline=False
    )
    
    embed.add_field(
        name="!wiki [boss name]",
        value="Show boss info and drops\nExample: `!wiki mihawk`",
        inline=False
    )
    
    embed.add_field(
        name="!drop [boss name]",
        value="Simulate a boss drop\nExample: `!drop mihawk`",
        inline=False
    )
    
    embed.add_field(
        name="!list",
        value="Show available items",
        inline=False
    )
    
    embed.add_field(
        name="!bosslist",
        value="Show all available bosses",
        inline=False
    )
    
    # Admin commands
    if ctx.author.guild_permissions.administrator:
        embed.add_field(
            name="🔧 Admin Commands",
            value=(
                "`!setvalue [item] [value]` - Update item value\n"
                "`!removeitem [item]` - Remove item from list\n"
                "`!addalias [shortcut] [item]` - Add item shortcut\n"
                "`!removealias [shortcut]` - Remove shortcut\n"
                "`!announce #channel [message]` - Send announcement\n"
                "`!say [message]` - Bot says message in current channel\n"
                "`!embed \"title\" [description]` - Send custom embed"
            ),
            inline=False
        )
    
    await ctx.send(embed=embed)

# Run the bot
# REPLACE 'YOUR_BOT_TOKEN_HERE' with your actual bot token
bot.run(

