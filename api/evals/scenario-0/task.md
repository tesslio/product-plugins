# Document Install Source Variant Schemas

## Problem/Feature Description

Your team is writing onboarding documentation for engineers who need to add packages to a Tessl workspace. Packages can come from several different source types — for example, a registry, a Git repository, or a local file path — and each source type requires a different set of fields in the API request body. The existing internal wiki has only a vague, one-line mention that "multiple source types are supported," which isn't enough for engineers to actually write correct API requests.

You've been asked to produce a reference document that spells out every install source variant: what type it represents and which fields are required for each variant shape. The Tessl platform exposes an endpoint that deals with install policy evaluation and uses these source types in its request body. You need to dig into its schema to extract the full picture — a thorough, field-level breakdown for each variant, detailed enough to write a correct API request.

## Output Specification

Produce a file named `install-source-variants.md` that contains:

1. **The commands you ran** to discover and inspect the relevant endpoint(s), listed in order (so the documentation is reproducible).
2. **The complete list of install source variant types** supported by the request body, with the required fields for each variant clearly identified.

The document should be detailed enough that an engineer can use it as a reference to construct a valid API request for any of the supported source types.
