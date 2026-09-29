# Ingestion instructions (how the model writes wiki notes)

**Planning a source into notes.** Group the numbered sections of one source into wiki notes. Each note covers ONE
subject. Titles are 2 to 5 natural words in Title Case that a person would search for, and they name the project when
the subject belongs to one project. No file names, no numbers at the start, no punctuation.

**Writing a note.** Use ONLY the source text. Keep numbers exactly as written. Do not add facts, opinions or advice.
A note has a summary of two or three sentences and four to seven key details, one fact per line.

**Linking notes.** A link needs a reason. For each candidate note, say in one short sentence how it connects to the
current note, or skip it if it does not.

The harness adds the title, the source references, the links and the properties. The model never writes file names.
A human reviews every note against the original before it is marked `reviewed: true`.
