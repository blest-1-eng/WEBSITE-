import io
import re
import aiohttp
from pypdf import PdfReader
from discord.ext import commands
from modules.brain import reply
from discord.config_manager import load


class PDF_AI(commands.Cog):
    """Processes PDFs with pypdf, remembers content, and answers follow-up questions."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.pdf_memory = {}  # channel_id -> {"text": str, "filename": str}

    async def cog_unload(self):
        await self.session.close()

    def _get_relevant_chunks(self, text: str, question: str, chunk_size: int = 4000, top_k: int = 3):
        """Return top_k chunks of text most relevant to the question."""
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        if len(chunks) <= top_k:
            return chunks

        q_words = set(re.findall(r'\w+', question.lower()))
        stop_words = {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'shall', 'you', 'i', 'he', 'she',
            'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your',
            'his', 'its', 'our', 'their', 'this', 'that', 'these', 'those',
            'what', 'which', 'who', 'whom', 'where', 'when', 'how', 'why',
            'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
            'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
            'too', 'very', 'just', 'about', 'above', 'after', 'again', 'against',
            'between', 'into', 'through', 'during', 'before', 'after', 'to', 'from',
            'in', 'out', 'on', 'off', 'over', 'under', 'up', 'down', 'with',
            'at', 'by', 'for', 'of', 'and', 'or', 'but', 'if', 'because', 'as',
            'until', 'while', 'then', 'once', 'here', 'there', 'when', 'where',
            'why', 'how', 'both', 'each', 'every', 'few', 'more', 'most',
            'other', 'some', 'such', 'only', 'own', 'same', 'than', 'too', 'very'
        }
        filtered_q = q_words - stop_words
        if not filtered_q:
            return chunks[:top_k]

        scored = []
        for idx, chunk in enumerate(chunks):
            chunk_lower = chunk.lower()
            score = sum(chunk_lower.count(word) for word in filtered_q)
            scored.append((score, idx))
        scored.sort(key=lambda x: x[0], reverse=True)
        top_indices = sorted([idx for _, idx in scored[:top_k]])
        return [chunks[i] for i in top_indices]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Respect configured AI channel
        try:
            data = load()
            if message.channel.id != data["ai_channel"]:
                return
        except Exception:
            return

        # ---- PDF attachment present ----
        pdf_attachment = None
        for att in message.attachments:
            if att.content_type and "application/pdf" in att.content_type:
                pdf_attachment = att
                break
            if att.filename.lower().endswith('.pdf'):
                pdf_attachment = att
                break

        if pdf_attachment:
            # Download and process
            progress_msg = await message.channel.send("Processing PDF...")
            try:
                # 1. Download
                await progress_msg.edit(content="📥 Downloading PDF...")
                async with self.session.get(pdf_attachment.url) as resp:
                    if resp.status != 200:
                        raise RuntimeError("Download failed")
                    pdf_bytes = await resp.read()

                if len(pdf_bytes) > 25 * 1024 * 1024:
                    await progress_msg.edit(content="❌ File size exceeds 25MB limit.")
                    return

                # 2. Read with pypdf
                await progress_msg.edit(content="📖 Reading PDF...")
                try:
                    reader = PdfReader(io.BytesIO(pdf_bytes))
                except Exception:
                    await progress_msg.edit(content="❌ Unable to read PDF.")
                    return

                extracted_text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        extracted_text += page_text + "\n"

                if not extracted_text.strip():
                    await progress_msg.edit(content="❌ This PDF contains no readable text.")
                    return

                # Store in memory
                self.pdf_memory[message.channel.id] = {
                    "text": extracted_text.strip(),
                    "filename": pdf_attachment.filename
                }

                # 3. Intent detection
                await progress_msg.edit(content="🧠 Understanding document...")
                user_msg = message.content.strip() or "No message"
                intent_prompt = (
                    "Classify the user's request regarding a PDF into one of the following intents: "
                    "short_summary, long_summary, important_points, notes, hindi_explanation, english_explanation. "
                    f"User request: {user_msg}. Only respond with the intent label."
                )
                intent_raw = reply(intent_prompt)
                intent = intent_raw.strip().lower() if intent_raw else "short_summary"

                intent_map = {
                    "short_summary": {
                        "name": "Short Summary",
                        "template": "Provide a short summary of the following document part:"
                    },
                    "long_summary": {
                        "name": "Long Summary",
                        "template": "Provide a detailed long summary of the following document part:"
                    },
                    "important_points": {
                        "name": "Important Points",
                        "template": "Extract key important points from the following document part:"
                    },
                    "notes": {
                        "name": "Notes",
                        "template": "Create concise study notes from the following document part:"
                    },
                    "hindi_explanation": {
                        "name": "Hindi Explanation",
                        "template": "निम्नलिखित दस्तावेज़ भाग की हिंदी में व्याख्या करें:"
                    },
                    "english_explanation": {
                        "name": "English Explanation",
                        "template": "Explain the following document part in English:"
                    }
                }

                if intent not in intent_map:
                    intent = "short_summary"
                output_name = intent_map[intent]["name"]
                prompt_base = intent_map[intent]["template"]

                # 4. Chunk & generate
                max_chunk = 12000
                full_text = extracted_text.strip()
                if len(full_text) > max_chunk:
                    chunks = [full_text[i:i + max_chunk] for i in range(0, len(full_text), max_chunk)]
                else:
                    chunks = [full_text]

                combined = ""
                for idx, chunk in enumerate(chunks):
                    prompt = (
                        f"{prompt_base}\n\n"
                        f"User request: {user_msg}\n\n"
                        f"Document chunk {idx + 1}/{len(chunks)}:\n{chunk}\n\n"
                        f"Generate the {output_name} for this chunk."
                    )
                    await progress_msg.edit(content="✍ Generating response...")
                    chunk_resp = reply(prompt)
                    if chunk_resp:
                        combined += chunk_resp.strip() + "\n\n"

                if not combined.strip():
                    combined = "Could not generate a response."

                # 5. Finalize
                await progress_msg.edit(content="✅ Done")
                await asyncio.sleep(2)
                await progress_msg.delete()

                # Send final answer, split if too long
                if len(combined) > 2000:
                    for i in range(0, len(combined), 2000):
                        await message.channel.send(combined[i:i + 2000])
                else:
                    await message.channel.send(combined)

            except Exception as e:
                await progress_msg.edit(content=f"❌ An error occurred: {e}")
            return  # Stop; do not handle as follow-up

        # ---- No attachment: follow-up Q&A if we have a remembered PDF ----
        if message.channel.id in self.pdf_memory:
            question = message.content.strip()
            if not question:
                return

            pdf_data = self.pdf_memory[message.channel.id]
            pdf_text = pdf_data["text"]

            relevant_chunks = self._get_relevant_chunks(pdf_text, question, chunk_size=4000, top_k=3)

            prompt = (
                "You are an AI assistant that answers questions based SOLELY on the provided document chunks. "
                "If the answer cannot be found in the document, reply that it's not covered in the PDF.\n\n"
            )
            for i, chunk in enumerate(relevant_chunks):
                prompt += f"[DOCUMENT PART {i+1}]:\n{chunk}\n\n"
            prompt += f"USER QUESTION: {question}\nANSWER:"

            async with message.channel.typing():
                answer = reply(prompt)

            if answer:
                if len(answer) > 2000:
                    for i in range(0, len(answer), 2000):
                        await message.channel.send(answer[i:i + 2000])
                else:
                    await message.channel.send(answer)
            else:
                await message.channel.send("⚠️ Could not generate an answer.")
            return

        # ---- Attachments exist but not PDF ----
        if message.attachments:
            await message.channel.send("❌ Please upload a PDF.")


async def setup(bot: commands.Bot):
    await bot.add_cog(PDF_AI(bot))
