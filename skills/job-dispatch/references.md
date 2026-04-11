# Harvard FAS RC (Cannon / Kempner) — cheat sheet

Cluster-specific facts for `rhakim` on FASRC Cannon. Docs: <https://docs.rc.fas.harvard.edu/>, Kempner handbook <https://handbook.eng.kempnerinstitute.harvard.edu/>.

## Accounts

Pick the partition first, then an account allowed on it. Preference order:

| Account | Allowed partitions | Notes |
|---|---|---|
| `kempner_rhakim_lab` | `kempner`, `kempner_h100`, `kempner_requeue`, `kempner_interactive` | Smaller; prefer for jobs <= 24h total |
| `kempner_bsabatini_lab` | all `kempner*` | Larger lab, more raw shares |
| `kempner_konkle_lab` | all `kempner*` | Larger lab, more raw shares |
| `kempner_ba_lab` | all `kempner*` | Larger lab, more raw shares |
| `rhakim_lab` | `sapphire`, `shared`, `serial_requeue`, `bigmem`, `test`, etc. | CPU-only / non-Kempner |

Fairshare rules of thumb (check with `sshare -U`):
- Default to `kempner_rhakim_lab`.
- Noticeable slowdown below ~0.7; hard to allocate below ~0.5.
- Ask before switching accounts.

## Partitions

### Kempner GPU (require a `kempner_*` account)

| Partition | GPU/node | Cores/node | RAM/node | Max walltime |
|---|---|---|---|---|
| `kempner` | 4× A100 40 GB SXM4 | 64 (Ice Lake) | ~1 TB | 7 days |
| `kempner_h100` | 4× H100 80 GB | 96 (Genoa) | ~1.5 TB | 3 days |
| `kempner_requeue` | H100/H200/A100-40G/A100 MIG (mixed) | varies | varies | 7 days (preemptible) |
| `kempner_interactive` | A100 MIG 3g.20gb | 64 | 1 TB | 8 hours |

Per-GPU policy caps (handbook, scheduler-enforced):
- `kempner` (A100): ≤ 16 cores, ≤ 240 GB / GPU
- `kempner_h100` (H100): ≤ 24 cores, ≤ 375 GB / GPU

No dedicated `kempner_h200` partition — reach H200 via `kempner_requeue` with `--constraint=h200`, or (FASRC-wide) the separate `gpu_h200` partition.

### Non-Kempner (require `rhakim_lab`)

| Partition | Cores/node | RAM/node | Max walltime | Use |
|---|---|---|---|---|
| `sapphire` | 112 (Sapphire Rapids) | ~1 TB | 3 days | Preferred CPU-only |
| `shared` | 48 (Cascade Lake) | ~184 GB | 3 days | General CPU |
| `serial_requeue` | mixed | varies | 3 days | Preemptible, cheap |

## Standard `#SBATCH` blocks

GPU blocks below are one "1 GPU slice" (one GPU + 1/4 of the node's cores and RAM). Scale linearly for 2–4 GPU jobs on the same node. No benefit to requesting less per node.

### `kempner` — 1× A100 40 GB
```bash
#SBATCH --partition=kempner
#SBATCH --account=kempner_rhakim_lab
#SBATCH --gres=gpu:1
#SBATCH -c 16
#SBATCH --mem=249000M
#SBATCH --time=1-00:00:00
```

### `kempner_h100` — 1× H100 80 GB
```bash
#SBATCH --partition=kempner_h100
#SBATCH --account=kempner_rhakim_lab
#SBATCH --gres=gpu:1
#SBATCH -c 24
#SBATCH --mem=374000M
#SBATCH --time=1-00:00:00
```

### `kempner_requeue` — opportunistic, preemptible
Shares hardware with `kempner`, `kempner_h100`, and H200 pools. Use `--constraint` to pin a GPU type if needed. Size `-c`/`--mem` to the underlying hardware (use the `kempner_h100` block for h100/h200, the `kempner` block for a100).

```bash
#SBATCH --partition=kempner_requeue
#SBATCH --account=kempner_rhakim_lab
#SBATCH --constraint=h200        # or: h100, a100
#SBATCH --gres=gpu:1
#SBATCH -c 24
#SBATCH --mem=374000M
#SBATCH --time=1-00:00:00
#SBATCH --requeue
```

### `sapphire` — CPU-only
Full node is `-c 112 --mem=990G`; size to the job.

```bash
#SBATCH --partition=sapphire
#SBATCH --account=rhakim_lab
#SBATCH -c 8
#SBATCH --mem=32G
#SBATCH --time=0-12:00:00
```

## Scheduler limits

- **Observed max active jobs per account: 16.** For kempner_ jobs only, use `--array=0-N%15` to keep a slot free. (FASRC's total public cap is 10,000 pending+running per user; the 16 is a tighter per-account/QoS limit observed on Kempner partitions, only.)
- Array job max index: 10,000.
- Login nodes are cgroup-limited to 1 core / 4 GB.
- `scancel -n <job-name>` cancels a whole named sweep — set `--job-name=<prefix>` consistently in the submitter.

## Docs

- FASRC Running Jobs: <https://docs.rc.fas.harvard.edu/kb/running-jobs/>
- FASRC Fairshare: <https://docs.rc.fas.harvard.edu/kb/fairshare/>
- FASRC Kempner partitions: <https://docs.rc.fas.harvard.edu/kb/kempner-partitions/>
- FASRC GPU computing: <https://docs.rc.fas.harvard.edu/kb/gpgpu-computing-on-the-cluster/>
- Kempner handbook — cluster overview: <https://handbook.eng.kempnerinstitute.harvard.edu/s1_high_performance_computing/kempner_cluster/overview_of_kempner_cluster.html>
- Kempner handbook — responsible use (per-GPU caps): <https://handbook.eng.kempnerinstitute.harvard.edu/s1_high_performance_computing/kempner_cluster/kempner_policies_for_responsible_use.html>
- Kempner handbook — advanced SLURM (`--constraint`): <https://handbook.eng.kempnerinstitute.harvard.edu/s1_high_performance_computing/general_hpc_concepts/advanced_slurm_features.html>
