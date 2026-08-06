# Data Sources

Track the exact source for every authority here before writing scraper code.

## National baseline (England)
- planning.data.gov.uk API — permitted-development-right dataset
  https://www.planning.data.gov.uk/dataset/permitted-development-right
- planning.data.gov.uk API — article-4-direction dataset
  https://www.planning.data.gov.uk/dataset/article-4-direction (TODO: confirm exact endpoint)
- Planning Portal Interactive House (seed content)
  https://interactive.planningportal.co.uk/explore-house

## National baseline (Wales)
- GOV.WALES — permitted development rights for householders
  https://www.gov.wales/planning-permission-permitted-development-rights-householders
- legislation.gov.uk — Wales GPDO amendments (TODO: pin exact instrument/year)
- Planning Aid Wales guidance library
  https://planningaidwales.org.uk/about-planning/links-2/

## Pilot local authorities

| Authority | Nation | Local data source | Notes |
|---|---|---|---|
| Ealing | England (London) | Planning London Datahub | near-home sanity check |
| TODO | England (London) | Planning London Datahub | pick 1-2 more boroughs |
| Bristol OR Manchester | England | TODO | non-London English authority |
| Cardiff | Wales | TODO | |
| Gwynedd | Wales | TODO | Article 4 second-homes case |

## Schema every source gets normalized into

```json
{
  "id": "string",
  "nation": "england | wales",
  "authority": "national | ealing | gwynedd | ...",
  "level": "national | local",
  "topic": "permitted-development | article-4 | building-regs | local-plan",
  "section_ref": "string",
  "text": "string",
  "source_url": "string"
}
```