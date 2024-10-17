# LibreLingo Documentation on Course

A **Course** is the highest element in the course structure. It contains modules, which in turn contain skills. There is usually one course for each language.

To get a better understanding, you can explore the [`courses` directory](https://github.com/LibreLingo/LibreLingo/tree/main/courses) on this repository and read the [course basics](README.md#basics).

---

**Confused?**
[Ask people](https://github.com/LibreLingo/LibreLingo/discussions) on GitHub Discussions.

---

**Table of Contents:**

- [Tree structure](#tree-structure)
- [`course.yaml`](#yaml)
  - [Data breakdown](#data-breakdown)

## Tree structure

A typical tree structure for a course is like this:

```
courses/spanish-from-english/
├── activities
│   ├── module.yaml
│   └── skills
│       ├── continuous.yaml
│       └── ser_estar.yaml
├── basics
│   ├── module.yaml
│   └── skills
│       ├── animals.yaml
│       ├── clothes.yaml
│       ├── food.yaml
│       ├── nature.yaml
│       ├── plurals.yaml
│       ├── professions.yaml
│       ├── verb_plurals.yaml
│       └── verbs.yaml
├── course.yaml
└── introduction
    ├── module.yaml
    └── skills
        ├── adjectives.yaml
        ├── phrases.yaml
        └── preferences.yaml
```

Here, `activities`, `basics`, and `introduction` are [modules](module.md). The `continuous.yaml`, `animals.yaml` etc., are [skills](skill.md). There is also a file called `course.yaml` directly inside the course directory. This file contains information about the course ([see below](#yaml)).

A course directory name should not have spaces and should be written in `slug-form` in plain English.

<a id="yaml"></a>

## `course.yaml`

A `course.yaml` file for the Spanish course looks like this:

```yaml
# This file contains generic meta-data about the course

Course:
  Language:
    Name: Spanish
    IETF BCP 47: es
  For speakers of:
    Name: English
    IETF BCP 47: en
  License:
    Name: Attribution-ShareAlike 4.0 International
    Short name: CC BY-SA 4.0
    Link: https://creativecommons.org/licenses/by-sa/4.0/legalcode
  Special characters:
    - "á"
    - "Á"
    - "é"
    - "É"
    - "í"
    - "Í"
    - "ó"
    - "Ó"
    - "ú"
    - "Ú"
    - "ü"
    - "Ü"
    - "ñ"
    - "Ñ"
    - "¿"
    - "¡"

Modules:
  - basics/
  - introduction/
  - activities/
```

<a id="data-breakdown"></a>

### Data breakdown

**`Course`** has information about the course.

- `Language`
  - `Language > Name`: The name of the language you want to test for or teach.
  - `Language > IETF BCP 47`: The IETF BCP 47 code of the above language. List available [here](http://www.iana.org/assignments/language-subtag-registry).
- `For speakers of`
  - `For speakers of > Name`: The name of the language your target audience already speaks.
  - `For speakers of > IETF BCP 47`: The IETF BCP 47 code of the above language. List available [here](http://www.iana.org/assignments/language-subtag-registry).
- `License`
  - `License > Name`: Full license name under which your course is made available. In most cases, it's ok to keep it as is.
  - `License > Short name`: Short name for the license, e.g., `CC BY-SA 4.0`
  - `License > Link`: URL to reach the full text of the license, e.g., `https://creativecommons.org/licenses/by-sa/4.0/legalcode`
- `Special characters`: An array of special characters that might not be present on a typical English keyboard. Note that this is separate from `New Characters` included inside some skills.

**`Modules`** has a list of module directory names followed by a `/`.

<a id="spell-checker"></a>

#### Automated spell checker

To avoid mistakes, you can enable automatic spell-checking in your course. Automatic spell-checking won't let you export
a course if it has spelling mistakes. This can prevent incorrect changes from being merged into your course.

The spell checker is implemeneted using Hunspell. In order to use it, you need to have Hunspell installed on your
computer.

To install Hunspell, follow the instructions of your operating system. On Ubuntu, you can install Hunspell like so:

```bash
sudo apt-get update -y
sudo apt-get install -y hunspell
```

Don't forget to also install a dictionary for the languages that you use in your course. Here's a list of
dictionary packages available on Ubuntu: https://packages.ubuntu.com/bionic/hunspell-dictionary

In order to enable Hunspell in your course, add the following section to your `course.yaml`:

```yaml
Settings:
  Hunspell:
    German: de # replace with the language code for your language
    English: en-US # replace with the language code for your language
```

Keep in mind that you also need to have the `hunspell` Python package installed. To install it, just run:

```bash
pip install hunspell
```
