# YAML

Guide for how to write YAML, especially in the context of Ansible. Because not all of us have time to read the YAML spec front-to-back just to know if you have to quote a string that has a colon in it.

**DISCLAIMER: This style guide is not a substitute for the YAML spec. YAML that follows this style guide to the letter may still fail to parse. This document merely attempts to summarize the most important, practical details of the spec for a human YAML writer.**

## When to Quote Strings

Knowing when you have to quote strings is probably the most difficult part of writing complex YAML documents. A good reference is [spec v1.2 section 7.3.3](http://yaml.org/spec/1.2/spec.html#id2788859). Here's what that section says:

> The plain (unquoted) style has no identifying indicators and provides no form of escaping. It is therefore the most readable, most limited and most context sensitive style. In addition to a restricted character set, a plain scalar must not be empty, or contain leading or trailing white space characters. It is only possible to break a long plain line where a space character is surrounded by non-spaces.

> Plain scalars must not begin with most indicators, as this would cause ambiguity with other YAML constructs. However, the `:`, `?` and `-` indicators may be used as the first character if followed by a non-space “safe” character, as this causes no ambiguity.

> ...

> Plain scalars must never contain the `: ` and ` #` character combinations. Such combinations would cause ambiguity with mapping key: value pairs and comments. In addition, inside flow collections, or when used as implicit keys, plain scalars must not contain the `[`, `]`, `{`, `}` and `,` characters. These characters would cause ambiguity with flow collection structures.

Some notes to go along with, or maybe summarize, the spec:

- if a string starts with one of these characters, it must be quoted: [`|`](http://yaml.org/spec/1.2/spec.html#id2795688), [`>`](http://yaml.org/spec/1.2/spec.html#id2796251), [``@` ``](http://yaml.org/spec/1.2/spec.html#c-reserved), [`&`](http://yaml.org/spec/1.2/spec.html#id2785586), [`*`](http://yaml.org/spec/1.2/spec.html#id2786196), [`!`](http://yaml.org/spec/1.2/spec.html#id2784064), [`%`](http://yaml.org/spec/1.2/spec.html#id2781147), [`[]`](http://yaml.org/spec/1.2/spec.html#id2790320), [`{}`](http://yaml.org/spec/1.2/spec.html#id2790832), [`,`](http://yaml.org/spec/1.2/spec.html#id2790088), [`#`](http://yaml.org/spec/1.2/spec.html#id2780069). These are most of the YAML [indicators](http://yaml.org/spec/1.2/spec.html#id2772075). As the spec notes, there are three indicators ([`-`](http://yaml.org/spec/1.2/spec.html#id2797382), [`?`](http://yaml.org/spec/1.2/spec.html#id2798057) and [`:`](http://yaml.org/spec/1.2/spec.html#id2798057)) that can be used at the start of a string under certain conditions.
- the following words are not strings in YAML unless quoted: `true`, `false`, `y`, `n`, `yes`, `no`, `on`, `off`, `null`, `~`, `.inf`, `-.inf`, `.nan` and various case permutations thereof. See [spec v1.2 section 10.3.2](http://yaml.org/spec/1.2/spec.html#id2805071).
- floating point, octal and hexadecimal numbers should be treated as strings if possible (by quoting them). This ensures they are reproduced exactly as printed.

When quoting strings, generally prefer double quotes. If a string contains a lot of double quotes and does not contain any single quotes, only then use single quotes instead. If the string contains a few quotes, but otherwise does not need to be quoted, just escape the individual quotes one by one with backslashes.

Don't be afraid of the YAML multi-line string forms, `|` and `>`, but make sure you know how they work before you use them, especially with respect to indentation. A good example of the `>` folded style is in the nginx default variables. You shouldn't need the `|` literal style very often.

## Other

Do not forget the `---` at the top of a YAML document.

Do not use YAML's JSON-like `[]` and `{}` forms (flow collections), except to specify an empty list/map. In all other cases, use the block syntax with `key: value` and `- item` forms.

Spaces and line feeds (`\n`) are the only forms of whitespace allowed. Hard tabs (`\t`) are prohibited *everywhere*, even in the places where the YAML spec says they are allowed (exception: you can use hard tabs if you are populating a template that is tab-sensitive, eg a Makefile, but you should try to handle the hard tabs in the template instead). Do not use any other non printing characters unless you have a really good reason.

The only boolean forms permitted are `true` and `false` (and they must be lower case). Do not use any of the other boolean forms: `y`, `n`, `yes`, `no`, `on`, `off`, or their case permutations. (Exception: you can use `on` and `off` for templates where the native boolean values are on/off, eg in nginx configuration - but only if the template supports the use of raw boolean values there. Otherwise they would be printed as `True` and `False`, therefore you must not use unquoted `on` and `off`.) If you ever use `true` or `false` as strings, add a comment to make it clear that the typing is intentional.

YAML should be indented with a width of two spaces. Remember, tabs are illegal for YAML indentation, and they are technically a parse error.

# Ansible Module Use

Various points about what modules to use and how to use them.

- When using the file module, always use `path`, never `dest`. The exception is for `state: link` in which case you should use `dest` instead of `path`.
- Avoid the use of the inline `key=value` form for specifying arguments to modules. Use the alternative form where the arguments are keys in a YAML map. For the `command` and `shell` modules, bind the arguments to the `args` map, as seen in the Ansible documentation (and various examples throughout this playbook).
- Always prefer the use of `command` to `shell`. Anywhere that you need to use `shell`, try to refactor it into a `command` (unless this would force you to add tasks). If you need to set environment variables, use the `environment` map on the task, instead of using the shell module and preceding the command string with the `VAR=value` shell syntax.
- Whenever using the `command` or `shell` modules, be sure to specify a `creates` or `removes` argument to make the behavior idempotent. Any command that manipulates files should have this argument. If that's not an option, register the result of the task and inspect its stdout/stderr to determine if the task failed, changed or was a no-op. Get creative. **Every task should be idempotent.**
- Prefer the use of version control modules (eg `git`, `hg`, `subversion`), rather than downloading tarballs and using the `unarchive` module. Always explicitly specify the version that will be downloaded, and always specify a stable target (eg a tag or a release branch). Avoid checking out master/trunk/tip since these are moving targets. Prefer HTTPS to SSH when specifying the repository URL, but never use HTTP.
- do not include trailing slashes on directory names unless they have semantic effect.
