# My Tiny Gen

## Description

Baby gen! 🐣

## Live UI

Visit the UI at https://tinygen-christinewang.b4a.run!

## Limitations
- Cannot handle large repos b/c it does a single GPT query with a 3000 token limit
- Cannot handle long prompts b/c it does a single GPT query with a 3000 token limit
- Code generation only covers code files.
- Code vs non code files are filtered using a simple algorithm that checks the file extension.
- Does not handle code changes that rename files
- Does not show diffs that are whitespace only

## Features
- UI! 📺
- Writes data (user input + generated output) to Supabase DB
- CI/CD through Back4App
- Remote container metrics + logs through Back4App
- Encrypted envvar secrets through Back4App
- Configurable number of reflection rounds

## Interested in contributing?

Check-out the [contributing](CONTRIBUTING.md) docs!
