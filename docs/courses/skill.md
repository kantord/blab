# LibreLingo Documentation on Skill

A **Skill** resides below a Module within the course structure. It's the lowest element in the course hierarchy. It contains a set of words and phrases to be taught to the user.

A skill is usually centered around a specific theme. This could be introducing a new grammar concept or just vocabulary to talk about a certain topic.

The words and phrases that make up a skill are taught to the user using [automatically generated questions and tasks](#how-skills-are-taught-to-the-user).

---

**Confused?**
[Ask people](https://github.com/LibreLingo/LibreLingo/discussions) on GitHub Discussions.

---

**Table of Contents:**

- [Tree structure](#tree-structure)
- [`(skill_name).yaml`](#yaml)
- [Data breakdown](#data-breakdown)
- [How skills are taught to the user](#how-skills-are-taught-to-the-user)
- [Creating new skills](#creating-new)
- [Examples of editing a skill](#example-edit)
- [Tips for creating good skills](#tips)
- [`(skill_name).md`](#markdown)

## Tree structure

A typical tree structure for skills under a module is as follows:

```
courses/spanish-from-english/basics/skills/
├── animals.yaml
├── clothes.yaml
├── food.yaml
├── nature.yaml
├── plurals.yaml
├── professions.yaml
├── verb_plurals.yaml
└── verbs.yaml
```

Here, `animals.yaml`, `clothes.yaml`, and `food.yaml` are skills. These skill files are kept inside a `skills` folder. The YAML files contain information about the skill (see below).

Skill yaml filenames should not have spaces and should be written in `slug-form`. The human-friendly `Name` in the yaml, however, can contain uppercase and spaces.

<a id="yaml"></a>

## `(skill_name).yaml`

As an example, let's look into the `courses/french-from-english/basics/skills/hello.yaml` file, which looks like this:

```yaml
Skill:
  Id: 33bfee7d-de74-4362-bf15-ce165add2dc8
  Name: Hello
  Thumbnails:
    - people1
    - woman1
    - man1

New words:
  - Word: l'homme
    Translation: the man
    Images:
      - man1
      - man2
      - man3

  - Word: la femme
    Synonyms:
      - la dame
    Translation: the woman
    Also accepted:
      - the female

Phrases:
  - Phrase: La femme dit bonjour
    Alternative versions:
      - la femme dit salut
    Translation: The woman says hello
    Alternative translations:
      - The woman says hi

  - Phrase: L'homme dit bonjour
    Alternative versions:
      - L'homme dit salut
    Translation: The man says hello
    Alternative translations:
      - The man says hi

Mini-dictionary:
  French:
    - dit: says
    - bonjour:
        - hello
        - hi
    - L'homme: the man

  English:
    - says: dit
    - hello:
        - bonjour
        - salut

Two-way-dictionary:
  - hello: bonjour
  - hello: salut
  - says: dit
  - the man: L'homme
```

Additionally, characters which are unfamiliar to the person learning the new language can be included in skills. These are typically put above `New Words` in a `(skill_name).yaml` file.

```yaml
New Characters:

  - Character: ç
    Transliteration: s
    IPA: /ç/
```

### Data breakdown

**`Skill`** has information about the skill.

- `Skill > Name`: The human-friendly name of the skill.
- `Skill > Id`: The ID of the course. **NOTE:** This should be unchanged if you're translating or editing an existing course. Only if you're creating a new course should this have a unique [UUID v4](https://www.uuidgenerator.net/version4) string. Details for which you can find [here](creating-courses.md).
- `Skill > Thumbnails`: A list of filenames of the thumbnails to be used on the course page to give an idea of the skill. A list of available files can be found on [`apps/web/static/images/`](https://github.com/LibreLingo/LibreLingo/tree/main/apps/web/static/images). The names should be used without extension and without `_tiny` or `_tinier` parts, e.g., `banana2_tinier.jpg` should be written as `banana2`.

**`New Characters`** has a list of new characters that the lesson teaches. This is only used for languages which use different characters than what the learner already knows. A character in LibreLingo can be a single character or a sound blend. These are currently not implemented in the web app.

- `Character`: The new character. Ensure it has the correct unicode value so it displays correctly.
- `Transliteration`: A list of transliterations of this character in the source language's script. The first one will be taught.
- `IPA`: A list of pronounciations in IPA (Internation Phonetic Language) format. (optional)

**`New words`** has a list of new words that the lesson teaches.

- `Word`: The word in the target language, i.e., the language the user is learning.
- `Synonyms`: A list of synonyms of the above word. (optional)
- `Translation`: Translation of the word in the source language, i.e., the language the user already knows.
- `Also accepted`: A list of alternative translations to the source language, which will _not_ be taught but will be accepted as correct translations of the `Word` field if supplied by the user. Currently has no effect, but may be used by future challenge types. (optional)
- `Images`: A list of images for the word that is defined under `Word` or `Translation` above. The image names have to be without extension and without `_tiny` or `_tinier` parts.

**`Phrases`** has a list of sentences or phrases that the lesson teaches.

- `Phrase`: The phrase in the target language.
- `Alternative versions`: A list of alternative versions of the phrase in the target language. These will _not_ be taught but will be accepted as correct translations of the `Translation` field if supplied by the user. (optional)
- `Translation`: Translation of the phrase to the source language.
- `Alternative translations`: A list of alternative translations to the source language, which will _not_ be taught but will be accepted as correct translations of the `Phrase` field if supplied by the user. (optional)

**`Mini-dictionary`** has a list of terms and meanings the user can view as a sort of "hint" if they are stuck. Entries are accessed by mousing over terms in an exercise, which brings up a tooltip with the corresponding term(s) in the other language. An entry is required for every term used in a skill.

Note that all `New words` are automatically added to the `Mini-dictionary`, in both translation directions, using the `Word` and `Translation` fields (`Synonyms` and `Also accepted` are ignored).

`Mini-dictionary` entries do not only apply to this skill; the meanings will apply course-wide and be merged with the same term in other skills, if applicable. This means that entries can be omitted when they are already present in other skills.

`Mini-dictionary` entries can define a term that spans multiple words, for example, a phrase like "post office". For this to work, "post office" will need to be enclosed in curly braces -- `{post office}` -- wherever it appears in the skill. (Due to YAML, strings containing braces will need to be quoted.)

- `<destination language>`: A list of terms in the destination language as key and meaning in the target audience's language.
- `<target audience's language>`: A list of terms in the target audience's language as key and meaning in the destination language.

**`Two-way-dictionary`** has a list of terms translating from the source language to the target language. This is a newer form of the `Mini-dictionary` in which we only need to write down pairs of words once, and they will
be included in the dictionary in both directions. Unlike the Mini-dictionary, here each word has exactly one translation (so no list), but the same word can appear multiple times.

```
Two-way-dictionary:
  - eat: como
  - eat: comer
```

Is the same as:

```
Mini-dictionary:
  English:
    - eat:
      - como
      - comer
  Spanish:
    - como: eat
    - comer: eat
```

The Two-way-dictionary also disregards any parentheses on the original side but includes them on the translation side:

```
Two-way-dictionary:
  - (I) eat: (yo) como
```

Is the same as writing

```
Mini-dictionary:
  English:
    - eat: (yo) como
  Spanish
    - como: (I) eat
```

## How skills are taught to the user

As the course author, you have to specify the words and phrases you want to teach. LibreLingo will know how to present skills as a series of individual questions and tasks -- LibreLingo calls these "challenges." It is useful to understand what challenges will be generated.

For each vocabulary word (that is, each `New words` entry) in a skill, LibreLingo generates:

- A [cards challenge](challenge.md#cards-challenge) -- multiple-choice translation from the source language to the target language, with a visual clue
- A [short input challenge](challenge.md#short-input-challenge) -- free-form translation from the source language to the target language
- A [listening challenge](challenge.md#listening-challenge) -- transcription from target language audio to the target language text

For each phrase in a skill, LibreLingo generates:

- An [options challenge](challenge.md#options-challenge) -- multiple-choice translation from target language to source language
- Two [chips challenges](challenge.md#chips-challenge) -- translation using provided words, one in each translation direction, unless the phrase is one word
- A [listening challenge](challenge.md#listening-challenge) -- transcription from target language audio to the target language text

<a id="creating-new"></a>

## Creating new skills

Creating new skills is a matter of creating their corresponding YAML file.
That being said, there are a couple of things to keep in mind:

- Skill yaml file should be inside a [module](module.md)'s `skills` directory.
- Skills should have a unique `Id`. Such identifiers can be generated using
  [this website](https://www.uuidgenerator.net/version4).
- Before skills will actually show up in the web app, they need to be added to
  a [`module.yaml`](module.md#yaml).

<a id="example-edit"></a>

## Examples of editing a skill

This is how you'd add a new alternative version to the
phrase "La femme dit bonjour":

```diff
Phrases:
  - Phrase: La femme dit bonjour
    Alternative versions:
      - La femme dit salut
+     - La madame dit salut
    Translation: The woman says hello
    Alternative translations:
      - The woman says hi
```

Keep in mind that when you add a new phrase or a new version or translation
to a phrase, it's not automatically updating to the mini-dictionary. So you need to
add any new words there:

```diff
Mini-dictionary:
  French:
    - dit: says
+   - madame: lady
    - bonjour:
      - hello
      - hi
    - L'homme: the man
```

Also, note that the new words from each phrase listed under the `Phrases` key need to be added for both the source and the target language in the `Mini-dictionary`. For example:

```yaml
Mini-dictionary:
  French:
    - dit: says
    - bonjour:
        - hello
        - hi
---
English:
  - says: dit
  - hello:
      - bonjour
      - salut
```

<a id="tips"></a>

## Tips for creating good skills

- When it comes to teaching grammar, your main tool is to teach by example.
- Use words to teach nouns that can be demonstrated easily with pictures, such as "dog", "car", "tree", and "city".
- Do not try to teach verbs, adjectives, etc., using words. Instead, use them in phrases.

<a id="markdown"></a>

## `(skill_name).md`

In order to create an introduction page for your skill, you need to create a [Markdown](https://en.wikipedia.org/wiki/Markdown)
file with the same name as your .yaml file but with the .md extension.

Place this .md file next to the .yaml file in your skills folder like so

```
courses/spanish-from-english/basics/skills
├── animals.md
├── animals.yaml
├── clothes.yaml
├── food.yaml
├── nature.yaml
├── plurals.yaml
├── professions.yaml
├── verb_plurals.yaml
└── verbs.yaml
```

You can use this Markdown file to create a short article about the skill the user is about to learn or practice.
This can be useful for explaining grammatical concepts, gotchas, and learning tips about the specific skill.
