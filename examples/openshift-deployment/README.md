# Example — OpenShift discoverable integration

[`deployment.yaml`](deployment.yaml) is a copy-and-edit reference: an OpenShift
`Project` annotated so Confida Integra discovers it as an integration, plus a
sample `Deployment` for realism.

## Use

1. Replace the `ict.example.org/` prefix with the label prefix your deployment
   is configured with (Settings → label prefix).
2. Make sure the `team` value matches your configured team name (default
   `integration`).
3. Apply:

   ```bash
   oc apply -f deployment.yaml
   ```

The integration appears on the next collector cycle. See
[`../../spec/ocp-label-convention.md`](../../spec/ocp-label-convention.md) for
the full field reference.
