# Experiment report template

Status: Planned / Fixture-validated / Real-validated / Blocked

## Question and hypothesis

## Dataset and protocol

Provenance, version, subset, template-family split, sample count, gold labels.

## Conditions

Baseline/variant; runtime/machine/region; embedding/index/prompt/model versions; cold/warm cache; concurrency; repeats; budget limit.

## Expected and actual results

Include raw JSONL/CSV, metric definitions, attempted/success/timeout counts, latency, usage and cost assumptions.

## Failures and interpretation

Separate ingestion/retrieval/generation/citation/permission/recovery failures. Do not tune on holdout without reclassifying it or replacing it.

## Decision and limits

Record remaining uncertainty and the next experiment, not a fictional successful measurement.
