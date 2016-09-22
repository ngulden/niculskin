# Contribute to Niculskin

Thank you for your interest in contributing to Niculskin. This guide details how
to contribute in a way that is efficient for everyone.

## Issue tracker

If you face issues with the skin, please look for a similar issues first in this projects issue tracker. 

If you face issues concerning weewx, please jump to the [weewx project page on GitHub](https://github.com/weewx/weewx).

### Bugs

If the problem, you encounter is not already described, simply create a new
issue. Please submit bugs using the following template in the issue description
area. The text in the parenthesis is there to help you with what to include.
Omit it when submitting the actual issue. You can copy-paste it and then edit
as you see fit.

```
## Summary

(Summarize your issue in one sentence - what goes wrong, what did you expect to happen?)

## Steps to reproduce

(How one can reproduce the issue - this is very important?)

## Expected behavior

(What you should see instead?)

## Relevant logs and/or screenshots

(Paste any relevant logs - please use code blocks (```) to format console output,
logs, and code as it's very hard to read otherwise.)

## Versions

(Which version of Niculskin and weewx are you using?)

## Possible fixes

(If you can, link to the line of code that might be responsible for the problem)

```

### Feature proposals

To create a feature proposal open an issue on the
[issue tracker of Niculskin][tracker].

You are encouraged to use the template below for feature proposals.

```
## Description
Include problem, use cases, benefits, and/or goals

## Proposal

## Links / references
```

## Merge requests

We welcome merge requests with fixes and improvements to Niculskin.

### Merge request guidelines

If you can, please submit a merge request with the fix or improvements. The
workflow to make a merge request is as follows:

1. Fork the project into your personal space on GitLab.com.
1. Create a feature branch, branch away from `master`.
1. Add your changes to the [CHANGELOG](CHANGELOG).
1. Push the commit(s) to your fork.
1. Submit a merge request (MR) to the `master` branch.
1. The MR title should describe the change you want to make.
1. The MR description should give a motive for your change and the method you.
   used to achieve it, see the [merge request description format]
   (#merge-request-description-format)
1. Link any relevant [issues][tracker] in the merge request description and
   leave a comment on them with a link back to the MR.
1. Be prepared to answer questions and incorporate feedback even if requests
   for this arrive weeks or months after your MR submission.
1. When writing commit messages please follow [these](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html) [guidelines](http://chris.beams.io/posts/git-commit/).

### Merge request description format

Please submit merge requests using the following template in the merge request
description area. Copy-paste it to retain the markdown format.

```
## What does this MR do?

## Are there points in the code the reviewer needs to double check?

## Why was this MR needed?

## What are the relevant issue numbers?

## Screenshots (if relevant)
```

## Code of conduct

As contributors and maintainers of this project, we pledge to respect all
people who contribute through reporting issues, posting feature requests,
updating documentation, submitting pull requests or patches, and other
activities.

We are committed to making participation in this project a harassment-free
experience for everyone, regardless of level of experience, gender, gender
identity and expression, sexual orientation, disability, personal appearance,
body size, race, ethnicity, age, or religion.

Examples of unacceptable behavior by participants include the use of sexual
language or imagery, derogatory comments or personal attacks, trolling, public
or private harassment, insults, or other unprofessional conduct.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct. Project maintainers who do not
follow the Code of Conduct may be removed from the project team.

This code of conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community.

This Code of Conduct is adapted from the [Contributor Covenant][contributor-covenant], version 1.1.0,
available at [http://contributor-covenant.org/version/1/1/0/](http://contributor-covenant.org/version/1/1/0/).

[tracker]: https://gitlab.com/ngulden/niculskin/issues
[contributor-covenant]: http://contributor-covenant.org
