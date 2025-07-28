import streamlit as st
import asyncio
import random
from telethon import TelegramClient, events

# --- UI ---
st.set_page_config(page_title="Telegram Bot Controller")
st.title("🤖 Telegram Bot Controller")
st.markdown("Enter your **Bot Token**, **Target IDs**, and choose a mode to control your bot.")

# User Inputs
bot_token = st.text_input("🤖 Bot Token", type="password")
api_id = st.text_input("API ID", value="2728292")
api_hash = "18ab225e7244bfc9a1119e6b2f065a48"  # Your fixed API hash

target_ids = st.text_area("🎯 Target User IDs", help="Enter multiple Telegram numeric user IDs, separated by commas (e.g., 123456789,987654321)")
group_id = st.text_input("🧵 Group Chat ID (optional)", help="Example: -1001234567890", value="")  # Optional
mode = st.selectbox("🚀 Choose Mode", ["replyraid", "raid", "spam", "photospam"])

start_bot = st.button("Start Bot")

# Sample abuse messages
abuse_list = [
    "You’re the reason shampoo has instructions 🤓🧴",
    "Ur face is proof that evolution can go in reverse 🧬↩️",
    "Your brain is under construction 🚧 still not started 🧠❌",
    "You got kicked out of the gene pool 🧬🚫",
    "No one asked, no one cares 🙄",
    "If stupidity were a sport, you’d be gold medalist 🏅🧠💩"
]

# Run bot when Start is pressed
if start_bot and bot_token and target_ids:
    try:
        target_list = [int(t.strip()) for t in target_ids.split(",") if t.strip()]
        group_chat_id = int(group_id.strip()) if group_id.strip() else None
    except ValueError:
        st.error("⚠️ Invalid ID format. Only use numeric values for users/groups.")
        st.stop()

    st.success(f"Bot starting with {len(target_list)} targets...")

    async def main():
        client = TelegramClient("bot_session", int(api_id), api_hash)
        await client.start(bot_token=bot_token)
        st.write("✅ Bot connected and running...")

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
                await event.reply("❌ Unknown mode.")

        @client.on(events.NewMessage(pattern="/help"))
        async def help_handler(event):
            help_text = (
                "**🤖 Available Commands:**\n\n"
                "*/start* – Trigger selected mode\n"
                "*/help* – Show this help message\n\n"
                "**Modes:**\n"
                "🔁 *spam* – Sends repeated text to users or group\n"
                "💣 *raid* – Sends abuse spam to users or group\n"
                "🎯 *replyraid* – Marks users for reply-based raid (requires group context)\n"
                "📸 *photospam* – Not supported in this Streamlit version\n\n"
                "⚠️ Users must have started the bot OR be in the same group."
            )
            await event.reply(help_text)

        await client.run_until_disconnected()

    # Run the async bot
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())is 
