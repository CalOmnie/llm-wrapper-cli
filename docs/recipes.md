# Recipes
Here is a non exhaustive list of tips and tricks to make the most of `llmc`.

## Pasting your clipboard selection in the input

There are several ways to safely paste the content of your clipboard to `llmc`,
the most obvious one is to simply plaste the content around quote e.g. `llmc "PRESS C-v here"`,
but this has several downsides, mainly the fact that if your clipboard selection contains quotes,
it can mess your whole invocation.

A safe and cleaner way to achieve that to top use a tool for it, these are different
for every platform, but their usage remains the same:

```
# WSL2
$ llmc $(clippaste)

# OSX
$ llmc $(pbpaste)

# Linux
$ llmc $(xsel -b -o)
```

## Passing a list of files

The easiest way to pass a list of files to `llmc` is to use the `find` command e.g.:

```
# Pass all python source files
$ llmc -i $(find src -name "*.py")

# Pass all python source files and associated tests
$ llmc -i $(find src -name "*.py") $(find tests -name "*.py")
```