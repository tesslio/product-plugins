---
name: review-public-exposure
description: Review a change to a public repository for content written for an internal audience, or content a reader outside the company should not have. Use as one lens in a code review run.
---

# Review lens: Public Exposure

Everything committed here is world-readable, including its history, and a commit
cannot be recalled once pushed. Review the change for content that assumes a
reader inside the company.

## Scope

- **An internal audience** Text addressed to a colleague rather than a user: a review request, a working note, an instruction naming an individual, or a rationale recorded for people who already share context the reader does not.
- **Internal references** A link, identifier, or path that resolves only inside the company — an issue tracker, chat workspace, wiki, or shared drive — or a ticket identifier carried into a file.
- **Unreleased and commercial detail** Roadmap, pricing, customer names, or a capability described before it ships.
- **Credentials and coordinates** A token, key, or internal hostname, including one appearing as an example value.

## Method

Read every added line as a reader outside the company would: someone evaluating
the product, a competitor, a search engine.

Prose is not the only surface. Check example values, fixture and eval inputs,
configuration fields, commented-out lines, and file and directory names, and read
an added file's reason for existing as well as its contents — a file whose purpose
is to brief a colleague does not belong here whatever it says.

## Threshold

Report content that only makes sense to a reader inside the company, or that a
reader outside it should not have.

Do not report a public product name, a public documentation link, the company's
own registry, or a public repository. Do not report a ticket identifier in a
commit message, which is out of scope for a lens that reviews file contents. Do
not accept, or propose, an exclusion from the published bundle as the fix: an
ignore rule controls what is uploaded to the registry and leaves the file in this
public repository.

## Reporting

- Name the file and line, and say who the content is addressed to, or what it exposes.
- State the fix as one of: remove the content, move the file to an internal repository, or rewrite it for a reader outside the company.
