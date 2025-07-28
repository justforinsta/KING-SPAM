import streamlit as st
import asyncio
import random
from telethon import TelegramClient, events

# --- Streamlit UI ---
st.set_page_config(page_title="Telegram Bot Controller")
st.title("🤖 Telegram Bot Controller")
st.markdown("Enter your **Bot Token**, **Target User IDs**, and choose a mode to control your Telegram bot.")

# User Inputs
bot_token = st.text_input("🤖 Bot Token", type="password")
api_id = st.text_input("📱 API ID", value="21111775")  # 👈 Your API ID is here now
api_hash = "18ab225e7244bfc9a1119e6b2f065a48"  # Replace if needed with your API hash

target_ids = st.text_area("🎯 Target User IDs", help="Comma-separated Telegram user IDs (e.g. 123456789,987654321)")
group_id = st.text_input("💬 Group Chat ID (optional)", help="Example: -1001234567890 (leave blank for private chat)")
mode = st.selectbox("⚙️ Choose Mode", ["replyraid", "raid", "spam", "photospam"])

start_bot = st.button("🚀 Start Bot")

# Sample abusive messages
abuse_list = [
    "You’re the reason shampoo has instructions 🤓🧴",
    "Ur face is proof that evolution can go in reverse 🧬↩️",
    "Your brain is under construction 🚧 still not started 🧠❌",
    "You got kicked out of the gene pool 🧬🚫",
    "If stupidity were a sport, you'd be world champion 🥇🧠💩",
]

if start_bot and bot_token and target_ids:
    try:
        target_list = [int(t.strip()) for t in target_ids.split(",") if t.strip()]
        group_chat_id = int(group_id.strip()) if group_id.strip() else None
    except ValueError:
        st.error("⚠️ Invalid ID format. Use only numbers separated by commas.")
        st.stop()

    st.success(f"Bot is starting with {len(target_list)} target(s)...")

    async def main():
        client = TelegramClient("bot_session", int(api_id), api_hash)
        await client.start(bot_token=bot_token)
        st.write("✅ Bot connected. Now go to Telegram and type /start or /help.")

        async def send_abuse_loop():
            for _ in range(5):
                for uid in target_list:
                    abuse = f"[🤮](tg://user?id={uid}) {random.choice(abuse_list)}"
                    chat_target = group_chat_id if group_chat_id else uid
                    await client.send_message(chat_target, abuse, parse_mode="md")
                    await asyncio.sleep(1)

        async def send_spam_loop():
            for i in range(5):
                for uid in target_list:
                    chat_target = group_chat_id if group_chat_id else uid
                    await client.send_message(chat_target, f"Spam #{i+1}")
                    await asyncio.sleep(1)

        @client.on(events.NewMessage(pattern="/start"))
        async def handle_start(event):
            if mode == "replyraid":
                for tid in target_list:
                    await event.reply(f"🎯 Marked [user](tg://user?id={tid}) for reply-based raid!")
            elif mode == "raid":
                await event.reply("💣 Raid starting...")
                await send_abuse_loop()
            elif mode == "spam":
                await event.reply("🔁 Spamming targets...")
                await send_spam_loop()
            elif mode == "photospam":
                await event.reply("📸 Photo spam not supported in this version.")
            else:
                await event.reply("❌ Unknown mode selected.")

        @client.on(events.NewMessage(pattern="/help"))
        async def help_handler(event):
            help_text = (
                "**🤖 Available Commands:**\n\n"
                "*/start* – Trigger the selected mode\n"
                "*/help* – Show this help message\n\n"
                "**Modes:**\n"
                "🔁 *spam* – Sends repeated messages to target(s)\n"
                "💣 *raid* – Sends abusive lines to target(s)\n"
                "🎯 *replyraid* – Marks users for reply-based raid (only works in groups)\n"
                "📸 *photospam* – Not supported in this Streamlit version\n\n"
                "⚠️ Users must have started the bot or be in the same group."
            )
            await event.reply(help_text)

        await client.run_until_disconnected()

    # Launch the async bot
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
