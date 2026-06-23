# LiaScript Markdown Cheat Sheet

> Quick reference for reading and editing EduGreenLabs workshop files.  
> LiaScript renders standard `.md` files as interactive presentations in the browser.  
> **Viewer:** [https://liascript.github.io/course/?URL_TO_YOUR_FILE.md](https://liascript.github.io/course/)

---

## Opening a Workshop File

Paste the raw GitHub URL into the LiaScript viewer:

```
https://liascript.github.io/course/?https://raw.githubusercontent.com/
OVGU-VET-TechEd/EU_Green_Labs_Workshops/main/workshop3_ai_implementation_sprint.md
```

Or open locally with the LiaScript DevServer:
```bash
npm install -g @liascript/devserver
liadev workshop3_ai_implementation_sprint.md
# Opens at http://localhost:3000
```

---

## 1 — Slides & Navigation

Each `##` heading starts a **new slide**. `###` creates sub-sections within a slide.

```markdown
# Course Title              ← Title slide (rendered once)

## Slide Title              ← New slide
Content here.

### Sub-section             ← Sub-page within the same slide
More content.

## Next Slide               ← Another new slide
```

Navigate with **arrow keys**, the on-screen buttons, or the sidebar table of contents.

---

## 2 — Text Formatting

```markdown
**bold text**
*italic text*
~~strikethrough~~
`inline code`
> blockquote / callout box
```

| Markdown | Renders as |
|---|---|
| `**bold**` | **bold** |
| `*italic*` | *italic* |
| `` `code` `` | `code` |
| `> note` | indented callout |

---

## 3 — Code Blocks

Fenced code blocks display with syntax highlighting. Add the language name after the opening backticks.

````markdown
```python
def hello():
    print("Hello from Gemma!")
```

```bash
ollama run gemma:latest "Explain GDPR in one sentence."
```

```json
{"model": "gemma:latest", "stream": false}
```
````

> In LiaScript, code blocks can be made **executable** — see Section 9.

---

## 4 — Single-Choice Quiz

```markdown
What is the default quantisation used by Ollama?

[( )] FP32 — full precision
[( )] FP16 — half precision
[(X)] Q4_K_M — 4-bit integer (correct answer marked with X)
[( )] Q2 — 2-bit integer
```

- `[( )]` — unselected option
- `[(X)]` — pre-selected / correct answer (shown after submission)
- Wrap in `[[?]]` to add a hint button

---

## 5 — Multiple-Choice Quiz

```markdown
Which of the following are true about Ollama? Select all that apply.

[[X]] It exposes an OpenAI-compatible REST API
[[ ]] It requires an internet connection during inference
[[X]] It runs models locally on your hardware
[[X]] It supports custom system prompts via Modelfiles
[[ ]] It only works on NVIDIA GPUs
```

- `[[X]]` — correct / pre-checked
- `[[ ]]` — incorrect / unchecked

---

## 6 — Text Input Quiz

Use double square brackets with a sample answer inside:

```markdown
Which command downloads the Gemma model in Ollama?

[[ollama pull gemma:latest]]
```

The learner types their answer; LiaScript checks it against the provided string (case-insensitive by default).

---

## 7 — Tables

```markdown
| Column A | Column B | Column C |
|---|---|---|
| Row 1A | Row 1B | Row 1C |
| Row 2A | Row 2B | Row 2C |
```

Alignment modifiers:
```markdown
| Left | Center | Right |
|:---|:---:|---:|
| L | C | R |
```

---

## 8 — Callout Boxes

LiaScript renders blockquotes as styled callout boxes:

```markdown
> Plain callout (grey box)

> ⚠️ Warning callout — use emoji to signal intent

> 💡 Tip callout

> ✅ Success / completion note

> 📋 Task / to-do instruction
```

---

## 9 — Executable Code Blocks

Add a `<script>` tag below a code block to make it runnable in the browser:

````markdown
```javascript
let x = 6 * 7;
console.log(x);
```
<script>@input</script>
````

For Python (requires Pyodide or a backend):
````markdown
```python
print("Hello from local Python!")
```
<script>
// @input is substituted with the code above at runtime
</script>
````

> Not all code types are executable in LiaScript without a backend. Shell/bash blocks are displayed only — learners run them in their own terminal.

---

## 10 — Timed Blocks (Workshop Agenda)

Use blockquotes with bold headers to mark timed agenda blocks:

```markdown
## Block 3 – Hands-On Setup *(0:32–0:55)*

> **⏱ 8 minutes**  
> Run the exercise in your terminal, then share results in the group.
```

---

## 11 — Task Lists (Deliverables Checklist)

```markdown
- [ ] Add your Green Metric result to the shared log
- [ ] Push your exercise file via fork + PR
- [X] Already completed item
```

Renders as interactive checkboxes in LiaScript.

---

## 12 — Links and Images

```markdown
[Link text](https://url.com)

![Alt text](https://url.com/image.png)

<!-- Local image (relative path): -->
![Diagram](./assets/deployment_spectrum.png)
```

---

## 13 — LiaScript-Specific Front Matter

Every LiaScript file should start with a YAML-style comment block:

```markdown
<!--
author:   Your Name
email:    your@email.de
version:  1.0.0
language: en
narrator: UK English Female
comment:  Short description of this course.
logo:     https://url-to-logo.png
-->

# Course Title
```

The `narrator` field enables **text-to-speech** for each slide — LiaScript will read slide content aloud if enabled.

---

## 14 — Sections with Timing Labels (Workshop Convention)

The EduGreenLabs workshops use this convention for timed blocks:

```markdown
## Block 3 – Hands-On: Ollama + Gemma Setup *(0:32–0:55)*

### 3.1 Installing Ollama

Content...

### ✏️ Hands-On Exercise *(8 minutes)*

> *Run these in your terminal*
```

- Top-level `##` = major block (appears in slide navigation)
- `###` = sub-section within the block
- Italic time in the `##` heading = total block duration
- Italic time in `###` heading = exercise duration

---

## 15 — Embedding Videos and External Resources

```markdown
!?[Video title](https://www.youtube.com/watch?v=VIDEO_ID)

??[Interactive embed title](https://some-external-tool.com)
```

---

## Common LiaScript Gotchas

| Issue | Fix |
|---|---|
| Slide not splitting correctly | Ensure `##` has a blank line before and after |
| Quiz not rendering | No blank line between the question and first option |
| Code not highlighted | Add language name after opening backticks |
| Table looks broken | Each row must have the same number of `\|` separators |
| Front matter ignored | Must be the very first thing in the file, no blank line before `<!--` |
| Text-to-speech reads code | Wrap code in a fenced block — TTS skips fenced blocks automatically |

---

## Quick Reference Card

```
## New slide             →  ## Heading
Sub-section              →  ### Heading
Bold / Italic            →  **bold** / *italic*
Code inline              →  `code`
Code block               →  ``` lang ... ```
Single-choice quiz       →  [( )] / [(X)]
Multiple-choice quiz     →  [[ ]] / [[X]]
Text input quiz          →  [[expected answer]]
Task checklist           →  - [ ] / - [X]
Callout box              →  > text
Link                     →  [text](url)
Image                    →  ![alt](url)
Video embed              →  !?[title](youtube-url)
```

---

*EduGreenLabs · EU-GREEN University Alliance · OvGU Magdeburg · CC BY-SA 4.0*
