# How to contribute?

Thank you for investing your time in contributing to our project! We are focused on making this library developer friendly and easy to use. If you're not on our [Discord Server](https://discord.gg/aQa53fRdXx), please consider joining, we're always active there.

Read our [Code of Conduct](./CODE_OF_CONDUCT.md) to keep our community approachable and respectable.

## Did you find a bug?

- Ensure the bug was not already reported by searching on GitHub under [Issues](https://github.com/Embedia-ai/embedia/issues)
- If you're unable to find an open issue addressing the problem, open a new one using the [Bug report issue template](https://github.com/Embedia-ai/embedia/issues/new/choose). Be sure to include a title and clear description, as much relevant information as possible, and a code sample or an executable test case demonstrating the expected behavior that is not occurring.

## Did you write a patch that fixes a bug?

- Open a new GitHub pull request with the patch (in accordance with the [Coding Guidelines](#coding-guidelines) mentioned below).
- Ensure the PR description clearly describes the problem and solution. Include the relevant github issue link(s) if applicable.

## Do you intend to add a new feature or change an existing one?

- Suggest your change in the [Discord server](https://discord.gg/aQa53fRdXx) and start writing code.
- Do not open an issue (with the [Feature request template](https://github.com/Embedia-ai/embedia/issues/new/choose)) on GitHub until you have collected positive feedback about the change.
- Fork the repo and make your changes in accordance with the [Coding Guidelines](#coding-guidelines) mentioned below.
- Ensure the PR description clearly describes the problem and solution. Include the relevant github issue link(s) if applicable.

## Coding Guidelines

- Use type hints wherever possible
- Use the async version of your code wherever possible. If it has a long running task / thread blocking code, move it to a background task
- Do not catch general exception: `Exception` until absolutely needed, catch specific exceptions
- Test for positive as well as negative test cases
- Keep docstrings for all user facing classes and functions up-to-date
- Before commiting your code, make sure of two things:
    - Make sure that running `./scripts/test.sh` from the root dir does not throw any errors
    - Run `./scripts/format.sh` from the root dir to ensure your code is formatted properly. (It will automatically format before you commit, but it's better to check beforehand)

## How to set up for local development?

- Clone your fork of this repo and navigate to it from the terminal
- Create a virtual enviroment using `python -m venv env` and activate it using `source ./env/bin/activate`. (Note: To deactivate run `deactivate`)
- Make sure you're using the latest version of `pip` using `python -m pip install --upgrade pip`
- Install requirements using `pip install -r requirements.txt`
- Create a `.env` file in the root directory and add the following environment variables:

```
OPENAI_API_KEY=<your-openai-api-key>
```
