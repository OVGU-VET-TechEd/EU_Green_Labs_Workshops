<!--
author:   EduGreenLabs / EU-GREEN University Alliance (OvGU Magdeburg)
email:    workshop@example.org
version:  1.0.0
language: en
narrator: US English Female

comment:  Local AI in Higher Education Teaching — Digital Agency with Offline LLMs,
          LiaScript & Vibe Coding. A 90-minute workshop framed by the UNESCO ICT
          Competency Framework for Teachers and the UNESCO AI Competency Framework
          for Teachers, with a crosswalk from KMK (DE) → DigCompEdu Supplement (EU)
          → UNESCO (global). Works as presentation, self-study tool and workshop toolbox.

logo:     https://raw.githubusercontent.com/LiaScript/docs/master/README/img/logo.png

@style
.lia-slide__content { font-family: system-ui, -apple-system, sans-serif; }
.box { background:#f5f7fa; border-radius:10px; padding:14px 18px; margin:12px 0; border-left:4px solid #2a7ed3; }
.box.warn { border-left-color:#e0832b; background:#fff8f0; }
.box.ok   { border-left-color:#2e9e5b; background:#f1faf4; }
.box.priv { border-left-color:#7c3aed; background:#f7f4fd; }
@end

import: https://raw.githubusercontent.com/liaTemplates/AVOREN/master/README.md

-->

# Local AI in Higher Education Teaching

**Digital Agency with Offline LLMs, LiaScript & Vibe Coding**

> *Which competencies do teachers need to use AI meaningfully and confidently in
> higher education — without cloud dependency, without data-protection concerns,
> without licence barriers?*

                          --{{0}}--
Welcome. Over the next ninety minutes we explore how local AI applications — offline
large language models — work together with LiaScript and the principle of *Vibe Coding*
to let you build Open Educational Resources at a low threshold. We frame all of this
inside two UNESCO reference documents and trace how teacher AI competencies progress
from the German, to the European, to the global level.

                          {{1}}
<section>

**This resource works three ways:**

| Mode | How to use it |
|------|---------------|
| 🎤 **Presentation** | Project full-screen, use arrow keys, speaker notes are spoken aloud |
| 📖 **Self-study** | Read at your own pace, run every interactive element yourself |
| 🧰 **Workshop toolbox** | Copy code blocks, configs and prompts directly into your own setup |

> 🕐 **Duration:** 90 minutes · **Audience:** Students · **Language:** English
> 📜 **Licence:** CC BY-SA 4.0 — remix and reuse freely.

</section>

                          --{{1}}--
Everything you see in a copyable code block is yours to take. The configuration files,
the prompts, the LiaScript snippets — all of it is released under an open licence so you
can carry it straight into your own teaching practice.

## Agenda

      {{|>}}

1. **Why local AI?** — cloud dependency, data protection, licence barriers *(10 min)*
2. **The three frameworks** — KMK → DigCompEdu Supplement → UNESCO *(15 min)*
3. **🔍 Interactive crosswalk** — explore how the competencies map onto each other *(15 min)*
4. **LiaScript & Vibe Coding** — building OER at a low threshold *(15 min)*
5. **🛠 Hands-on** — Ollama + Gemma + Continue in VS Code *(25 min)*
6. **Wrap-up & toolbox** — what you take home *(10 min)*

--{{|>}}--
The middle of the workshop is the heart of it: an interactive tool that lets you click
through the German, European and global competency frameworks and see, side by side,
how the same underlying ideas are expressed at each level. After that we get our hands
dirty with a fully local AI coding assistant.

## 1 · Why Local AI?

Cloud AI tools are powerful — but in a higher-education context they raise three
recurring problems. This workshop is built around solving all three with **offline LLMs**.

      {{1}}
<div class="box warn">

**☁️ Cloud dependency** — your teaching workflow breaks the moment the service changes its
API, raises its price, or goes down. You are renting, not owning, your tools.

</div>

      {{2}}
<div class="box priv">

**🔒 Data protection** — student work, prompts and assessment data leave your machine and
land on servers you do not control. Under the GDPR (Art. 5, 6, 9) this is a genuine legal
risk, not a hypothetical one.

</div>

      {{3}}
<div class="box">

**💸 Licence barriers** — per-seat pricing and closed models exclude students who cannot
pay, undermining equity and the idea of Open Educational Resources.

</div>

      {{4}}
<div class="box ok">

**✅ The local alternative** — a model like **Gemma** running through **Ollama** on your own
laptop. No data leaves the machine, no subscription, no licence wall. That is what
*digital agency* (*digitale Handlungsfähigkeit*) means in practice.

</div>

--{{1}}--
The first problem is dependency. When your entire teaching workflow sits on top of a
commercial cloud API, you are at the mercy of that provider's pricing and uptime.

--{{2}}--
The second is data protection. Every prompt you send to a cloud model contains
information — sometimes student information — and it leaves your control entirely.

--{{3}}--
The third is licence barriers. Closed, paid models create a two-tier classroom.

--{{4}}--
The answer running through this whole workshop is local inference. A capable open model,
on your own hardware, answering only to you.

### Quick check

What is the single strongest argument for **local** AI in a university classroom that
handles student data?

[( )] It always produces better answers than cloud models.
[(X)] Student data never leaves the machine, which directly addresses GDPR obligations.
[( )] It is faster than every cloud API.
[( )] It requires no hardware at all.
*****************
<div class="box ok">
Correct. Local inference is not always *better* or *faster* — but it keeps data on your
own device, which is decisive when GDPR-relevant student data is involved.
</div>
*****************

## 2 · Three Frameworks, One Direction

Teacher AI competencies are described at three levels. They were written independently,
but they point the same way.

| Level | Document | Scope |
|-------|----------|-------|
| 🇩🇪 **National** | **KMK** *Handlungsempfehlung KI* (2024) + *Lehren und Lernen in der digitalen Welt* (2021) | Recommendations for German education administration |
| 🇪🇺 **European** | **Supplement to the DigCompEdu Framework** (AI Pioneers, Erasmus+, 2023) | 6 competence areas × 6 progression stages |
| 🌍 **Global** | **UNESCO AI Competency Framework for Teachers** (2025) | 5 competency areas × 3 progression levels |

--{{0}}--
Three documents, three levels of governance. The German KMK recommendations, the
European DigCompEdu supplement, and the global UNESCO framework. None of them copied the
others, yet as we will see they describe a strikingly similar set of teacher competencies.

                {{1}}
> 💡 **The key insight:** All three move along the *same axis* — from basic literacy, through
> confident pedagogical application, to ethical leadership and the creation of new
> practice. The labels differ; the destination does not.

### The KMK level (Germany) 🇩🇪

The 2024 KMK *Handlungsempfehlung* devotes its **Themenbereich 3** to teacher
professionalisation. Its core demands:

- AI competence is **embedded in all three phases** of teacher education.
- Teachers must not only *apply* AI but **understand its technical foundations** and judge
  its opportunities, limits and risks.
- **Media literacy, media ethics and critical reflection** sit alongside applied and
  computer-science skills.
- Teachers are **continuous learners** who reflect on and change their own role.

> The 2021 KMK paper already framed this as a **progression of competence development** —
> the seed of the staged models the EU and UNESCO would formalise.

--{{0}}--
Germany's contribution is notable for insisting on three things together: hands-on
application, genuine technical understanding, and critical-ethical reflection. It refuses
to separate "using the tool" from "understanding the tool".

### The European level (DigCompEdu Supplement) 🇪🇺

The **AI Pioneers** project extended the established DigCompEdu framework with AI-specific
competencies, keeping its structure intact: **six competence areas** and a **six-stage
progression** from *Newcomer (A1)* to *Pioneer (C2)*.

      {{1}}
The six areas:

1. **Professional Engagement**
2. **Digital Resources**
3. **Teaching and Learning**
4. **Assessment**
5. **Empowering Learners**
6. **Facilitating Learners' Digital Competence**

      {{2}}
Plus **transversal skills**: digital literacy, critical thinking, problem-solving,
ethical awareness, and lifelong learning.

--{{0}}--
The European supplement is the most granular of the three. It did not reinvent anything —
it took the well-known DigCompEdu structure and asked, for each area, what AI changes.

--{{1}}--
Six areas, ranging from the teacher's own professional networks all the way to helping
students build their own digital competence.

--{{2}}--
And cutting across all six, a set of transversal "soft" skills that make the technical
competencies usable in real classrooms.

### The global level (UNESCO 2025) 🌍

UNESCO's framework organises everything into **five competency areas**, each with **three
progression levels**: **Acquire → Deepen → Create**.

| # | Competency area | Acquire → Deepen → Create |
|---|-----------------|---------------------------|
| 1 | **Human-centred mindset** | Human agency → Human accountability → Social responsibility |
| 2 | **Ethics of AI** | Ethical principles → Safe & responsible use → Co-creating ethical rules |
| 3 | **AI foundations & applications** | Basic techniques → Application skills → Creating with AI |
| 4 | **AI pedagogy** | AI-assisted teaching → AI–pedagogy integration → Pedagogical innovation |
| 5 | **AI for professional development** | Continuous PD → Collaborative PD → Leadership in PD |

--{{0}}--
UNESCO's structure is the cleanest to teach with: five areas, three levels each. Notice
that the very first area is not technical at all — it is a *human-centred mindset*. The
framework deliberately begins with agency and ethics before it touches a single tool.

> 📌 Notice the verbs: **Acquire, Deepen, Create**. That is the same arc the KMK calls a
> "progression of competence development" and DigCompEdu calls *Newcomer → Pioneer*.

## 3 · 🔍 Interactive Framework Crosswalk

The tool below is the centrepiece. Pick a **theme** along the top, then move the
**progression slider** to see how each framework expresses that competency at a
*beginner*, *intermediate* or *advanced* level — side by side, German → European → global.

> 🖱️ **How to use it:** click a theme button, drag the slider, and read across the three
> columns. The bottom panel summarises what the three levels share.

<script style="display:block; width:100%; font-family:inherit;">
"HTML"
</script>

``` html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; }
  body { font-family: system-ui, -apple-system, sans-serif; margin:0; padding:0; background:#fff; color:#1f2933; }
  .wrap { max-width: 980px; margin: 0 auto; }
  h4 { margin: 4px 0 10px; }
  .themes { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:16px; }
  .themes button {
    border:2px solid #d9dee5; background:#fff; color:#334; border-radius:8px;
    padding:8px 13px; cursor:pointer; font-size:13px; font-weight:600; transition:all .15s;
  }
  .themes button:hover { border-color:#9bb3cf; }
  .slider-box { background:#f0f4ff; border:1px solid #c8d5f5; border-radius:10px; padding:14px 18px; margin-bottom:18px; }
  .slider-box label { font-size:13px; color:#445; display:block; margin-bottom:8px; }
  .slider-box .stagename { font-size:20px; font-weight:800; }
  input[type=range]{ width:100%; accent-color:#2a7ed3; margin-top:6px; }
  .stage-ticks { display:flex; justify-content:space-between; font-size:11px; color:#778; margin-top:4px; }
  .cols { display:grid; grid-template-columns: 1fr 1fr 1fr; gap:14px; }
  @media (max-width:760px){ .cols { grid-template-columns:1fr; } }
  .col { border-radius:10px; padding:14px; border-top:5px solid; background:#fafbfc; }
  .col .flag { font-size:22px; }
  .col .lvl  { font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.04em; opacity:.7; }
  .col .doc  { font-size:12px; color:#667; margin-bottom:8px; }
  .col .stage{ display:inline-block; font-size:11px; font-weight:700; padding:2px 8px; border-radius:20px; color:#fff; margin-bottom:8px; }
  .col p { font-size:13px; line-height:1.55; margin:6px 0; }
  .col .tag { font-size:11px; color:#556; background:#eef1f5; border-radius:6px; padding:2px 7px; display:inline-block; margin:2px 3px 0 0; }
  .synthesis { margin-top:18px; background:#f1faf4; border:1px solid #b8e3c8; border-left:5px solid #2e9e5b; border-radius:0 10px 10px 0; padding:14px 18px; }
  .synthesis h5 { margin:0 0 6px; color:#1e7a44; font-size:14px; }
  .synthesis p { font-size:13px; line-height:1.6; margin:0; color:#244; }
</style>
</head>
<body>
<div class="wrap">

  <div class="themes" id="themes"></div>

  <div class="slider-box">
    <label>Progression level — drag to compare beginner → advanced</label>
    <div class="stagename" id="stagename">–</div>
    <input type="range" id="stage" min="0" max="2" step="1" value="0">
    <div class="stage-ticks"><span>Beginner</span><span>Intermediate</span><span>Advanced</span></div>
  </div>

  <div class="cols">
    <div class="col" id="col-de" style="border-top-color:#000;"></div>
    <div class="col" id="col-eu" style="border-top-color:#003399;"></div>
    <div class="col" id="col-un" style="border-top-color:#0077c8;"></div>
  </div>

  <div class="synthesis">
    <h5>🔗 What the three levels share</h5>
    <p id="synth">–</p>
  </div>

</div>

<script>
(function(){

  // Stage labels per framework, indexed 0,1,2
  var STAGES = {
    de: ['Phase 1 — Ausbildung', 'Phase 2 — Referendariat', 'Phase 3 — Fort-/Weiterbildung'],
    eu: ['Newcomer / Explorer (A1–A2)', 'Integrator / Expert (B1–B2)', 'Leader / Pioneer (C1–C2)'],
    un: ['Acquire', 'Deepen', 'Create']
  };
  var STAGECOLOR = ['#2a7ed3', '#7c3aed', '#2e9e5b'];
  var STAGENAMES = ['Beginner — first contact', 'Intermediate — confident application', 'Advanced — leadership & creation'];

  // THEMES: each maps a competency idea across all three frameworks, per stage.
  var THEMES = [
    {
      id:'mindset', label:'🧭 Human-centred mindset & agency',
      de:[
        {s:'Awareness that learning is social and human-led; AI must not weaken shared learning.', tags:['Medienkompetenz','digitale Mündigkeit']},
        {s:'Teachers keep the central role in shaping the learning environment; judge chances, limits & risks of AI.', tags:['Lernbegleitung','kritische Reflexion']},
        {s:'Teachers see themselves as learners, continuously reflecting on and changing their own role.', tags:['Selbstreflexion','Rollenwandel']}
      ],
      eu:[
        {s:'Recognise AI is a tool that supports — not replaces — the educator; basic awareness of its influence.', tags:['Professional Engagement']},
        {s:'Critically evaluate AI outputs and the educator\u2019s changing role within professional practice.', tags:['Critical thinking']},
        {s:'Lead and advocate for human-centred, responsible AI use across the institution.', tags:['Leadership','advocacy']}
      ],
      un:[
        {s:'Human agency: understand AI is human-led; corporate decisions affect rights & autonomy.', tags:['1.1 Human Agency']},
        {s:'Human accountability: humans remain legally accountable in human\u2013AI decision loops.', tags:['1.2 Accountability']},
        {s:'Social responsibility: actively build inclusive, just AI societies.', tags:['1.3 Social Responsibility']}
      ],
      synth:'All three insist that the human stays in charge. Germany frames it as the teacher\u2019s irreplaceable central role and digital Mündigkeit; the EU as critical evaluation of AI outputs; UNESCO as an explicit progression from agency, to accountability, to social responsibility. The mindset comes before the tool.'
    },
    {
      id:'ethics', label:'⚖️ Ethics, data protection & responsible use',
      de:[
        {s:'Sensitise teachers to legal frameworks (GDPR, EU AI Act) and possible risks of AI use.', tags:['Datenschutz','Medienethik']},
        {s:'Judge the quality and ethical effects of AI results; protect students\u2019 personality rights.', tags:['informationelle Selbstbestimmung']},
        {s:'Shape regulation and a positive error culture; safeguard data sovereignty institutionally.', tags:['Regulierung','Schulaufsicht']}
      ],
      eu:[
        {s:'Ethical awareness: understand privacy, data security and equity implications of AI.', tags:['Ethical awareness']},
        {s:'Identify algorithmic bias; apply responsible-use practices in teaching contexts.', tags:['bias','responsible use']},
        {s:'Promote a culture of responsible AI use among learners and peers.', tags:['Empowering Learners']}
      ],
      un:[
        {s:'Ethical principles: do-no-harm, proportionality, non-discrimination, transparency.', tags:['2.1 Principles']},
        {s:'Safe & responsible use: data privacy, IP, data sovereignty, "safety by design/use".', tags:['2.2 Safe Use']},
        {s:'Co-create ethical rules; simulate multi-stakeholder debates (e.g. the EU AI Act).', tags:['2.3 Co-creation']}
      ],
      synth:'Data protection is the shared backbone. The KMK names GDPR and the EU AI Act directly and stresses informational self-determination; DigCompEdu lists ethical awareness as a transversal skill; UNESCO devotes an entire area to it — and "data sovereignty" in UNESCO 2.2 is exactly the argument for the local, offline LLMs at the heart of this workshop.'
    },
    {
      id:'foundations', label:'🔧 AI foundations & technical understanding',
      de:[
        {s:'Basic informatics education: understand the technical functioning of AI.', tags:['informatische Grundlagen']},
        {s:'Understand how AI is trained; assess reliability of outputs from a technical view.', tags:['Funktionsweise','Güte der Ergebnisse']},
        {s:'Re-evaluate competence requirements as technology evolves; build evaluation procedures.', tags:['Evaluation','Weiterentwicklung']}
      ],
      eu:[
        {s:'Digital literacy: basic proficiency operating AI tools and platforms.', tags:['Digital literacy']},
        {s:'Develop data literacy and computational thinking; curate resources with AI.', tags:['data literacy']},
        {s:'Innovate technical solutions; adapt AI tools to new scenarios.', tags:['problem-solving']}
      ],
      un:[
        {s:'Basic AI techniques: definitions, data & algorithms; operate validated tools — prefer open-source.', tags:['3.1 Basics']},
        {s:'Application skills: compare symbolic/predictive/generative AI; assess "ethics by design".', tags:['3.2 Application']},
        {s:'Creating with AI: customise or modify tools to build inclusive learning environments.', tags:['3.3 Creating']}
      ],
      synth:'All three reject "black-box" use. The KMK demands genuine informatic understanding of how AI works; DigCompEdu builds data literacy and computational thinking; UNESCO progresses from operating tools, to comparing AI types, to creating with AI. UNESCO 3.1 even explicitly favours open-source tools — the rationale for running Gemma locally.'
    },
    {
      id:'pedagogy', label:'🎓 AI pedagogy & teaching practice',
      de:[
        {s:'Use AI to support lesson design; AI as personal tutor / adaptive learning environment.', tags:['Lehr-Lernsituationen']},
        {s:'Make didactically justified decisions with AND without AI; individualise teaching.', tags:['Individualisierung','Feedback']},
        {s:'Develop pedagogical-didactic repertoire; co-create education-specific AI in pilots.', tags:['Ko-Kreation','Pilotprojekte']}
      ],
      eu:[
        {s:'Teaching & Learning: use AI for adaptive content and intelligent tutoring.', tags:['Teaching & Learning']},
        {s:'Assessment: AI-assisted, adaptive and formative assessment; analyse learning trends.', tags:['Assessment']},
        {s:'Empowering Learners: personalised, inclusive, learner-centred AI strategies.', tags:['Empowering Learners']}
      ],
      un:[
        {s:'AI-assisted teaching: leverage pedagogical benefits while mitigating risks.', tags:['4.1 Assisted']},
        {s:'AI\u2013pedagogy integration: student-centred design, differentiated learning.', tags:['4.2 Integration']},
        {s:'Pedagogical innovation: AI-immersed scenarios, inquiry- & project-based learning.', tags:['4.3 Innovation']}
      ],
      synth:'Pedagogy is where the frameworks are richest and most aligned. Each moves from using AI for basic lesson support, to integrating it into student-centred learning design, to genuine pedagogical innovation. The KMK\u2019s insistence on decisions made "with AND without AI" matches UNESCO\u2019s human-accountable decision loops.'
    },
    {
      id:'profdev', label:'🌱 Professional development & lifelong learning',
      de:[
        {s:'Embed AI skills in all three phases of teacher education; ongoing professionalisation.', tags:['Lehrkräftebildung']},
        {s:'Adapt PD formats as AI evolves; competence centres support training.', tags:['Fortbildung','Kompetenzzentren']},
        {s:'Provide resources & freedom for continuous learning; teachers as lifelong learners.', tags:['Ressourcen','Freiräume']}
      ],
      eu:[
        {s:'Lifelong learning: commit to continuously updating AI knowledge and skills.', tags:['Lifelong learning']},
        {s:'Collaborate via AI tools and networks; share best practice.', tags:['Professional Engagement']},
        {s:'Contribute to AI policy development within the institution.', tags:['policy']}
      ],
      un:[
        {s:'Continuous PD: use AI to manage personal learning and knowledge.', tags:['5.1 Continuous']},
        {s:'Collaborative PD: AI-supported communities of practice and co-creation.', tags:['5.2 Collaborative']},
        {s:'Leadership in PD: design AI-enhanced CPD, mentor peers, shape policy.', tags:['5.3 Leadership']}
      ],
      synth:'The teacher is framed as a permanent learner everywhere. Germany embeds AI across all three training phases and demands time and resources; DigCompEdu names lifelong learning a transversal skill; UNESCO dedicates an area to it, ending in leadership and mentoring. Building OER yourself — as you will do today — is exactly this competency in action.'
    }
  ];

  var current = THEMES[0];
  var stageIdx = 0;

  function flag(which){ return which==='de'?'🇩🇪':which==='eu'?'🇪🇺':'🌍'; }
  function docname(which){
    return which==='de' ? 'KMK (Germany)' : which==='eu' ? 'DigCompEdu Supplement (EU)' : 'UNESCO AI Framework (Global)';
  }

  function renderCol(which){
    var el = document.getElementById('col-'+which);
    var d = current[which][stageIdx];
    var html = '';
    html += '<div class="flag">'+flag(which)+'</div>';
    html += '<div class="lvl">'+docname(which)+'</div>';
    html += '<div class="doc">'+STAGES[which][stageIdx]+'</div>';
    html += '<span class="stage" style="background:'+STAGECOLOR[stageIdx]+'">'+STAGENAMES[stageIdx]+'</span>';
    html += '<p>'+d.s+'</p>';
    html += '<div>'+d.tags.map(function(t){return '<span class="tag">'+t+'</span>';}).join('')+'</div>';
    el.innerHTML = html;
  }

  function update(){
    document.getElementById('stagename').textContent = STAGENAMES[stageIdx];
    renderCol('de'); renderCol('eu'); renderCol('un');
    document.getElementById('synth').textContent = current.synth;
  }

  // Build theme buttons
  var tb = document.getElementById('themes');
  THEMES.forEach(function(t){
    var b = document.createElement('button');
    b.textContent = t.label;
    b.addEventListener('click', function(){
      current = t;
      Array.prototype.forEach.call(tb.children, function(x){ x.style.background='#fff'; x.style.borderColor='#d9dee5'; x.style.color='#334'; });
      b.style.background='#2a7ed3'; b.style.borderColor='#2a7ed3'; b.style.color='#fff';
      update();
    });
    tb.appendChild(b);
  });
  tb.children[0].style.background='#2a7ed3';
  tb.children[0].style.borderColor='#2a7ed3';
  tb.children[0].style.color='#fff';

  document.getElementById('stage').addEventListener('input', function(e){
    stageIdx = parseInt(e.target.value,10);
    update();
  });

  update();
})();
</script>
```

--{{0}}--
Take your time with this. Pick the theme that matters most to your own subject, then walk
the slider from beginner to advanced and read across the three columns. The thing to
notice is how often the German, European and global wording is *almost interchangeable* —
three committees, working separately, converging on the same competencies.

### Reflection

After exploring the crosswalk: which competency theme do *you* feel least prepared in
right now? There is no wrong answer — this is a self-assessment.

[[ Human-centred mindset | Ethics & data protection | AI foundations | AI pedagogy | Professional development ]]

                    {{1}}
> 🎯 Whatever you picked, today's hands-on section touches **AI foundations** (running a
> local model) and **ethics & data protection** (keeping data on your machine) directly —
> and gives you a reusable artefact for **professional development**.

## 4 · LiaScript & Vibe Coding

You are reading this *inside* LiaScript right now. It is a free, open Markdown dialect
that turns a single `.md` file into an interactive course — quizzes, animations, embedded
HTML and code, text-to-speech — all from plain text.

> 📜 **Why it matters for OER:** one human-readable file, version-controllable on GitHub,
> served by any web link, licensable as CC BY-SA. No platform lock-in. That is the
> *low-threshold* path to Open Educational Resources.

      {{1}}
**The same pattern you saw in the crosswalk** — a live HTML block inside Markdown:

      {{1}}
``` markdown
<script style="display:block; width:100%;">
"HTML"
</script>

​``` html
<!DOCTYPE html>
<html><body>
  <button onclick="alert('Hello from local OER!')">Click me</button>
</body></html>
​```
```

--{{0}}--
LiaScript is the engine running this whole presentation. The crucial point for you as a
future educator is that it is just one text file. You can put it on GitHub, share a link,
and anyone can read it, fork it, or remix it — the definition of an Open Educational
Resource.

--{{1}}--
And the embedding trick is always the same: a small script tag that injects an HTML block.
Copy this pattern and you can drop any interactive widget into your own materials.

### What is *Vibe Coding*?

**Vibe Coding** = describing what you want in plain language and letting an AI assistant
draft the code, while *you* stay the accountable author who reviews and decides.

      {{1}}
<div class="box">

It lowers the threshold dramatically: you do not need to memorise syntax to produce a
working interactive OER element. You need **judgement** — exactly the *human accountability*
competency from UNESCO area 1.2.

</div>

      {{2}}
<div class="box priv">

🔒 **The local twist:** if your coding assistant is a **local Gemma model via Ollama**, then
your "vibe coding" prompts — which may contain student examples or unpublished material —
**never leave your laptop.** Vibe Coding + offline LLM = creativity *and* data protection.

</div>

--{{1}}--
Vibe coding does not remove the human — it relocates the human's job from typing syntax to
exercising judgement. You describe, the model drafts, you review and remain accountable.

--{{2}}--
And here is where the two halves of the workshop meet. If the assistant doing your vibe
coding is a local model, your prompts stay private. You get the creativity of AI assistance
without surrendering a single byte of student data.

## 5 · 🛠 Hands-on: Local AI Coding Assistant

Goal: a fully **offline** AI assistant inside VS Code, powered by **Gemma** through
**Ollama**, wired up with **Continue**. Everything below is copy-paste ready.

> ⚠️ **Before the session:** the four programs in the next section must already be installed.
> Ask your workshop's technical support to prepare the lab machines (checklist provided).

### Step 1 — Pull the model

Ollama downloads and runs the model locally. One command:

``` bash
# Pull Google's Gemma (≈ the 8 GB "latest" build used in this workshop)
ollama pull gemma:latest

# Low-RAM fallback for 8 GB machines (~1.4 GB):
ollama pull gemma:2b

# Verify it works — this answer is generated entirely on your machine:
ollama run gemma:latest "Confirm you are running locally."
```

> 💾 Models are cached in `~/.ollama/models` — you download once, then work offline forever.

### Step 2 — Configure Continue

Continue is the VS Code extension that connects your editor to the local model. Create the
file `~/.continue/config.json` (global) or `.continue/config.json` (per project) and paste:

``` json
{
  "$schema": "https://raw.githubusercontent.com/continuedev/continue/main/extensions/vscode/config_schema.json",
  "models": [
    {
      "title": "Gemma (Local — Private)",
      "provider": "ollama",
      "model": "gemma:latest",
      "apiBase": "http://localhost:11434",
      "contextLength": 4096,
      "description": "Default Gemma via local Ollama. No data leaves your machine."
    },
    {
      "title": "Gemma 2B (Low-RAM — Local)",
      "provider": "ollama",
      "model": "gemma:2b",
      "apiBase": "http://localhost:11434",
      "contextLength": 2048,
      "description": "Smallest Gemma (~1.4 GB). Use on 8 GB RAM machines."
    }
  ],
  "tabAutocompleteModel": {
    "title": "Gemma Autocomplete",
    "provider": "ollama",
    "model": "gemma:latest",
    "apiBase": "http://localhost:11434"
  },
  "slashCommands": [
    {
      "name": "oer-review",
      "description": "Check code/content for OER compatibility",
      "prompt": "Review the following for Open Educational Resource (OER) compatibility: (1) open licence (MIT/Apache/CC BY-SA)? (2) proprietary or cloud dependencies — suggest open alternatives. (3) offline-capable? (4) privacy/GDPR risks in a teaching context. (5) reproducible & documented? (6) accessible? For each issue: problem, why it matters, concrete fix.\n\n```\n{{{ input }}}\n```"
    },
    {
      "name": "privacy-check",
      "description": "Audit code for GDPR/privacy issues",
      "prompt": "You are a GDPR privacy auditor. Review this code for: direct identifiers, quasi-identifiers, special-category data (Art. 9), missing pseudonymisation, data-minimisation violations (Art. 5(1)(c)), hardcoded secrets. For each: (a) the problem, (b) the GDPR article, (c) a concrete fix.\n\n```\n{{{ input }}}\n```"
    }
  ]
}
```

### Step 3 — Project rules (`.continuerules`)

A plain-text `.continuerules` file in your project root steers every response. For this
student workshop:

``` text
You are a workshop coding assistant for university students building Open
Educational Resources with LiaScript.

Always:
- Prefer fully local, offline-capable solutions (Ollama + Gemma) over cloud APIs.
- Keep all student data on the local machine; never suggest uploading data to a
  third-party service. Flag any GDPR-relevant data handling (cite Art. 5, 6, 9).
- Produce educational output as Markdown or LiaScript, never plain prose dumps.
- Use open licences (MIT for code, CC BY-SA for content) and add a short licence header.
- Explain the code step by step before writing it — students are learning, not just shipping.
- When a decision is open, present numbered options and ask before assuming.
```

### Step 4 — Use it

| Action | Shortcut / command |
|--------|--------------------|
| Open Continue chat | `Ctrl+L` / `Cmd+L` |
| Highlight code → explain | select → `Ctrl+Shift+L` |
| Inline autocomplete | type, accept with `Tab` |
| Run a slash command | type `/oer-review` or `/privacy-check` in chat |
| Add a file to context | `@file my_lesson.md` |
| Switch model | click the model name at the bottom of the panel |

> 🔒 Every response comes from Gemma on `localhost:11434`. **No data leaves the machine** —
> confirm this with your network adapter switched off.

--{{0}}--
This is the moment the whole workshop has been building toward. Four steps: pull the model,
point Continue at it, set your project rules, and start coding by conversation. And the
headline is the privacy callout — you can literally turn off your wifi and it still works.

### 🧪 Try it yourself

In Continue chat, with your `.continuerules` active, try this Vibe Coding prompt:

``` text
Create a LiaScript multiple-choice quiz with three questions about why local
AI protects student data. Use the LiaScript [(X)] correct-answer syntax and add
a short feedback block. Output as Markdown I can paste into a .md file.
```

Then ask Continue to `/oer-review` its own output. Notice that it runs **completely
offline**.

      {{1}}
**Checkpoint quiz:**

Where does inference happen when you use this setup?

[( )] On Google's servers.
[( )] On Continue's cloud.
[(X)] Locally, on `http://localhost:11434`, via Ollama.
*****************
<div class="box ok">
Right — Ollama serves the model on your own machine's localhost. That is the entire point.
</div>
*****************

## 6 · 🧰 Technical Support Setup Sheet

> **For the technical support member preparing the lab with me.** Every student PC needs the
> following. Listed with purpose, source and rough footprint so you can plan disk and time.

### Required programs (in install order)

| # | Program | Purpose in this workshop | Source / install | Notes |
|---|---------|--------------------------|------------------|-------|
| 1 | **VS Code** | Editor that hosts the AI assistant and the LiaScript files | code.visualstudio.com | Free. Latest stable. |
| 2 | **Ollama** | Runs the local LLM and serves it on `localhost:11434` | ollama.com/download | macOS / Windows / Linux installers. Starts a background service. |
| 3 | **Gemma model** | The actual offline LLM doing the work | `ollama pull gemma:latest` (~8 GB) | Pull **before** the session over wired LAN. Also pull `gemma:2b` (~1.4 GB) as a low-RAM fallback. |
| 4 | **Continue** (VS Code extension) | Wires VS Code to the local Gemma model | VS Code Marketplace → "Continue" | Pre-seed `~/.continue/config.json` from this sheet. |
| 5 | **GitHub Copilot** (VS Code extension) | Optional cloud-based autocomplete, for the *contrast* demo (cloud vs local) | VS Code Marketplace → "GitHub Copilot" | Needs a (student) GitHub account + sign-in. **Optional** — local-first is the workshop's message. |

### Supporting tools

| Tool | Why | Notes |
|------|-----|-------|
| **Git** | Clone the workshop repo; version OER files | git-scm.com — often bundled with VS Code on Windows. |
| **A modern web browser** | Render the LiaScript course (`liascript.github.io/course/?<url>`) | Chrome / Firefox / Edge — any current version. |
| **Python 3.10+** *(optional)* | Run the Ollama API examples (`requests`) if you demo scripting | Add `pip install requests`. Only if you show the API. |

### Hardware & prep checklist

<div class="box warn">

- [ ] **RAM:** 16 GB recommended for `gemma:latest`. On 8 GB machines, switch the config to `gemma:2b`.
- [ ] **Disk:** ≥ 12 GB free per machine (model + tools).
- [ ] **Pre-pull the model** on every PC over wired LAN — do **not** rely on 30 students pulling 8 GB over wifi live.
- [ ] **Verify the service:** `curl http://localhost:11434/api/version` returns a version.
- [ ] **Pre-seed** `~/.continue/config.json` and a project `.continuerules` (copy from Section 5).
- [ ] **Smoke test:** open VS Code → `Ctrl+L` → ask Continue a question → confirm a Gemma reply appears.
- [ ] **Offline test:** disable the network adapter and confirm Continue still answers.
- [ ] **(If using Copilot):** confirm each machine can sign into a GitHub account.

</div>

> 📦 **One-line install reference (Linux/macOS):** the EU Green Labs `install_ollama.sh`
> pattern — install Ollama, start the service, `ollama pull gemma:latest`, drop in the
> Continue config. Windows: run the Ollama `.exe` installer, then the same `ollama pull`.

### Setup verification (run this together)

This shows the model answering locally — no internet required:

``` bash
ollama list                         # gemma:latest should appear
curl http://localhost:11434/api/version
ollama run gemma:latest "Reply with exactly: LOCAL OK"
```

## Wrap-up — What You Take Home

      {{|>}}

- 🧭 A **map** of teacher AI competencies across three levels — and the insight that they
  point the same way: KMK → DigCompEdu → UNESCO, *Acquire → Deepen → Create*.
- 🔒 A working argument for **local AI**: no cloud dependency, GDPR-aligned data protection,
  no licence barriers — UNESCO's *data sovereignty* made concrete.
- 🛠 A **reusable setup**: Ollama + Gemma + Continue, with configs you copied from Section 5.
- 📜 The **LiaScript + Vibe Coding** workflow for building Open Educational Resources at a
  low threshold — and an OER artefact you made yourself.

--{{|>}}--
So what do you walk out with? A mental map of the frameworks, a defensible case for local
AI, a working offline assistant on your own machine, and the skills to build open
educational resources. That last one — building OER yourself — is the professional
development competency from all three frameworks, in action.

                {{1}}
> 🎓 **Digital agency** (*digitale Handlungsfähigkeit*) is not about using the flashiest tool.
> It is about understanding your tools well enough to choose them deliberately — and keeping
> both your data and your pedagogy in your own hands.

### Final reflection

Having built a local AI assistant and seen the frameworks side by side — has your sense of
which competency you're *least* prepared in changed?

[[ Yes, it shifted | No, same as before | I feel more prepared overall ]]

### Further reading

- **UNESCO** — AI Competency Framework for Teachers (2025)
- **AI Pioneers** — Supplement to the DigCompEdu Framework (Erasmus+, 2023)
- **KMK** — *Handlungsempfehlung … Künstliche Intelligenz in schulischen Bildungsprozessen* (2024)
- **LiaScript** — liascript.github.io · **Ollama** — ollama.com · **Continue** — continue.dev
- **EU Green Labs Workshops** — github.com/OVGU-VET-TechEd/EU_Green_Labs_Workshops

> 📜 This resource is released under **CC BY-SA 4.0**. Fork it, translate it, remix it.

**Thank you — now go build something local. 🌿**
