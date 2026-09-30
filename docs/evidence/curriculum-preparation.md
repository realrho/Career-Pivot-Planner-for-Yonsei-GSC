# Curriculum preparation validation — 2026-10-01

## Scope

This record covers the curriculum and workspace organization, not completion of the eight-week application project.

## Checks

- Eight course chapters; four concept lessons each (32 total).
- Three explained quiz questions each (24 total), eight lab/code sections and eight detailed implementation recipes.
- Four ordered build tasks/week, 5/6/6/5h = 22h/week, 176h total planning assumption.
- 32 Jira subtasks SCRUM-14–45, linked to the original eight weekly stories SCRUM-6–13.
- Seven native week-to-week Blocks links; W2 correctly shows blocked by W1 and blocks W3.
- Existing Notion weekly pages read back without truncation or unknown blocks after the core update; concept/build/quiz sections present in all eight.
- Existing Notion tracker and Internal Transfer rows retained; weekly implementation statuses not completed by documentation edits.
- Python syntax parsed for all eight educational snippets. Seven standard-library examples executed successfully. W1 FastAPI contract example was not executed in this local QA environment because FastAPI is not installed.
- Local Markdown links checked; no missing local file references.

## Evidence boundaries

No application behavior was changed by this curriculum commit. Existing source was inspected and preserved: three intake/lookup/health routes, in-memory case state, four baseline tests. Those API tests were not run by this document QA. Real embedding/Milvus/LLM/HITL/cache/deployment/cloud/GPU measurements remain future implementation work and require their own evidence.

Each chapter includes complexity/bottleneck notes for its educational code. Provider pricing examples are fictional. Policy datasets and customer scenarios are synthetic planning materials.
